from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Result, ResultStatus, ResultStatusEnum
from app.services.grpc import convert_file_grpc
from app.services.rabbitmq import enqueue_task
from app.services.database import update_result_status
from app.utils import generate_name
from app import db
from datetime import datetime
import zipfile
import tempfile
import time
import os

VALID_MODELS = {'rode', 'cude', 'tilde', 'legibility'}
VALID_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
VALID_DOCUMENT_EXTENSIONS = {'pdf', 'tif', 'tiff'}

class FileWithFilename:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename

    def read(self, *args, **kwargs):
        return self.file.read(*args, **kwargs)

    def close(self):
        return self.file.close()

class WorkerResource(Resource):
    @jwt_required()
    def post(self):
        if 'files' not in request.files:
            abort(400, "No file part")
            
        files = request.files.getlist('files')
        
        if 'task_id' not in request.form:
            task_id = generate_name(3)
        else:
            task_id = request.form['task_id']
            
        if 'models' not in request.form:
            abort(400, "No models provided")
            
        models = request.form.get('models').split(',') 
        invalid_models = set(models) - VALID_MODELS
        if invalid_models:
            abort(400, f"Invalid models: {', '.join(invalid_models)}")
        
        result = Result.query.filter_by(collection_id=task_id).first()
        if result:
            abort(409, "Task ID already exists")
            
        result = Result(collection_id=task_id, user_id=get_jwt_identity(), created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(result)
        db.session.commit()
        
        result_status = ResultStatus(
            result_id=result.id,
            status=ResultStatusEnum.UPLOADING,
            total_files=len(files),
            models=','.join(models)
            
        )
        db.session.add(result_status)
        db.session.commit()
        
        if len(files) == 1 and files[0].filename.endswith('.zip'):
            files = self._extract_zip_file(files[0])
            update_result_status(result_status.id, total_files=len(files), status=ResultStatusEnum.PENDING, last_updated=datetime.now())
        
        for i, file in enumerate(files):
            file_bytes = file.read()
            filename = file.filename.lower()
            file_extension = os.path.splitext(filename)[1][1:].lower()
            
            if not os.path.exists(f'/shared-data/{task_id}'):
                os.makedirs(f'/shared-data/{task_id}')
            
            if file_extension in VALID_DOCUMENT_EXTENSIONS:
                start_time = time.time()
                images = convert_file_grpc(file_bytes, filename)
                print(f'File {filename} converted in {time.time() - start_time} seconds')
                
                for j, image_bytes in enumerate(images):  
                    image_path = f'/shared-data/{task_id}/{filename}_page_{j+1}.jpg'
                    with open(image_path, 'wb') as img_f:
                        img_f.write(image_bytes)
                    self._enqueue_tasks(image_path, filename, task_id, models, i+1, j+1)
                    
            elif file_extension in VALID_IMAGE_EXTENSIONS:
                image_path = f'/shared-data/{task_id}/{filename}'
                with open(image_path, 'wb') as img_f:
                    img_f.write(file_bytes)
                self._enqueue_tasks(image_path, filename, task_id, models, i+1, 1)
                    
        update_result_status(result_status.id, status=ResultStatusEnum.PENDING, total_files=len(files), last_updated=datetime.now())
                    
        return {"task_id": task_id}, 202
    

    def _extract_zip_file(self, zip_file):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            tmp_dir = tempfile.mkdtemp()
            zip_ref.extractall(tmp_dir)
            return [FileWithFilename(open(os.path.join(tmp_dir, name), 'rb'), name) for name in zip_ref.namelist()]
        
    def _enqueue_tasks(self, image_path, filename, task_id, models, file_index, page_number):
        for model in models:
            task_data = {
                'filename': filename,
                'file_path': image_path,
                'task_id': task_id,
                'model_name': model,
                'page': page_number,
                'file_index': file_index
            }
            enqueue_task(task_data, f'queue_{model}')