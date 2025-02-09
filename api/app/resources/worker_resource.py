from flask import request, abort
from flask_restful import Resource
from app.models import Result, ResultStatus, ResultStatusEnum
from app import db
from app.services.grpc import convert_file_grpc
from app.services.rabbitmq import enqueue_task
from app.services.database import update_result_status
from app.utils import generate_name
import time

VALID_MODELS = {'rode', 'cude', 'tilde'}

class WorkerResource(Resource):
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
            
        result = Result(collection_id=task_id, user_id=1)
        db.session.add(result)
        db.session.commit()
        
        result_status = ResultStatus(
            result_id=result.id,
            status=ResultStatusEnum.PENDING,
            total_files=len(files),
            models=','.join(models)
        )
        db.session.add(result_status)
        db.session.commit()
        
        for i, file in enumerate(files):
            file_bytes = file.read()
            filename = file.filename.lower()
            
            start_time = time.time()
            images = convert_file_grpc(file_bytes, filename)
            print(f'File {filename} converted in {time.time() - start_time} seconds')
            
            for j, image_bytes in enumerate(images):
                image_path = f'/shared-data/{filename}_page_{j+1}.jpg'
                with open(image_path, 'wb') as img_f:
                    img_f.write(image_bytes)
                for model in models:
                    task_data = {
                        'filename': filename,
                        'file_path': image_path,
                        'task_id': task_id,
                        'model_name': model,
                        'page': j+1,
                        'file_index': i+1
                    }
                    
                    enqueue_task(task_data, f'queue_{model}')
                    
        update_result_status(result_status.id, status=ResultStatusEnum.PENDING)    
                    
        return {"task_id": task_id}, 202