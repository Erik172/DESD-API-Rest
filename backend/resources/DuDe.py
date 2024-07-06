from pdf2image import convert_from_path
from PIL import Image, ImageSequence
from flask_restful import Resource
from database import get_database, WorkStatus, sql_db
from services import DuDeBase
from flask import request
import os
    
class DuDe(Resource):
    db = get_database()

    def post(self):
        required_fields = ['result_id', 'files']
        for field in required_fields:
            if field not in request.form and field != 'files':
                return {"message": f"No {field} provided"}, 400
            elif field == 'files' and not request.files:
                return {"message": "No files provided"}, 400
            
        result_id = request.form['result_id']
        files = request.files.getlist('files')

        work_status = WorkStatus(
            result_id=result_id, 
            total_files=len(files), 
            status="in_progress", 
            duplicate=True
        )
        sql_db.session.add(work_status)
        sql_db.session.commit()

        if not os.path.exists(f'temp/{result_id}'):
            os.makedirs(f'temp/{result_id}')

        for file in files:
            if file.filename.lower().endswith('.pdf'):
                file.save(f'temp/{result_id}/{file.filename}')
                images = convert_from_path(f'temp/{result_id}/{file.filename}', thread_count=os.cpu_count())
                for i, image in enumerate(images):
                    image.save(f'temp/{result_id}/{file.filename}__pagina_{i + 1}.png')
                os.remove(f'temp/{result_id}/{file.filename}')

            elif file.filename.lower().endswith(('.tiff', '.tif')):
                tiff_image = Image.open(file)
                for i, page in enumerate(ImageSequence.Iterator(tiff_image)):
                    jpg_file_path = f"temp/{result_id}/{file.filename}__pagina_{i + 1}.jpg"
                    page.save(jpg_file_path, "JPEG")
            else:
                file.save(f'temp/{result_id}/{file.filename}')

        dude = DuDeBase(f'temp/{result_id}')
        dude.find_duplicates()
        report = dude.generate_report()

        try:
            collection = self.db[result_id]
            collection.insert_many(report)
        except Exception as e:
            work_status.status = "failed"
            print(f"Error al insertar en la base de datos: {e}")

        # delete all files
        for file in os.listdir(f'temp/{result_id}'):
            os.remove(f'temp/{result_id}/{file}')
        os.rmdir(f'temp/{result_id}')

        work_status.status = "completed" if work_status.status != "failed" else "failed"
        work_status.total_files = len(files)
        sql_db.session.commit()

        return {"duplicados": dude.get_duplicates()}, 200
    
    