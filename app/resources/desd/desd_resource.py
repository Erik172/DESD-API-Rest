from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from flask import request
from app.services import ModelAIService
from app.models import Result, ResultStatusEnum, ResultStatus
from app import db, mongo
from datetime import datetime
import os
from .desd_processing import DESDProcessing

class DESDResource(Resource):
    #TODO: Dejar de manejar los modelos en un archivo de configuración a base de datos
    @jwt_required()
    def post(self):
        required_fields = ['result_id', 'models']
        missing_fields = [field for field in required_fields if field not in request.form]

        if missing_fields:
            return {"message": f"No {', '.join(missing_fields)} provided"}, 400
        
        if 'files' not in request.files:
            return {"message": "No file part in the request"}, 400

        model_names = request.form.get('models').split(',')
        files = request.files.getlist('files')
        result_id = request.form.get('result_id')
        
        # Verificar y crear el resultado si es necesario
        result = Result.query.filter_by(collection_id=result_id).first()
        if result:
            if result.status in [ResultStatusEnum.PROCESSING, ResultStatusEnum.COMPLETED, ResultStatusEnum.ERROR]:
                return {"message": f"The result has status {result.status}"}, 400
        else:
            result = Result(collection_id=result_id, user_id=current_user.id)
            db.session.add(result)
            db.session.commit()

            result_status = ResultStatus(
                result_id=result.id,
                status=ResultStatusEnum.PENDING,
                total_files=len(files),
                total_files_processed=0
            )
            db.session.add(result_status)
            db.session.commit()

        models = {model: ModelAIService(model) for model in model_names if model in ['inclinacion', 'rotacion', 'corte informacion']}

        processed_files = 0
        for file in files:
            filename = secure_filename(file.filename)
            temp_path = os.path.join('temp', filename)
            
            # Streaming: escribir el archivo mientras se lee en trozos
            with open(temp_path, 'wb') as f:
                while chunk := file.stream.read(1024 * 1024):  # Leer en bloques de 1 MB
                    f.write(chunk)
            
            results = {filename: {}}

            # Procesa el archivo según su extensión
            try:
                if filename.lower().endswith('.pdf'):
                    DESDProcessing().process_pdf(models, results, filename, temp_path)
                elif filename.lower().endswith(('.tiff', '.tif')):
                    DESDProcessing().process_tiff(models, results, filename, temp_path)
                else:
                    DESDProcessing().process_image(models, results, filename, temp_path)

                processed_files += 1
                result_status.status = ResultStatusEnum.RUNNING
                result_status.total_files_processed = processed_files
                result_status.last_updated_at = db.func.now()
                db.session.commit()

                # Guardar resultados en la base de datos después de procesar cada archivo
                for model_name in results[filename]:
                    for i in results[filename][model_name]:
                        data = {
                            'archivo ': filename,
                            'pagina': int(i) + 1,
                            'modelo': model_name,
                            'prediccion': results[filename][model_name][i]['prediccion'],
                            'confianza': results[filename][model_name][i]['confianza'],
                            'tiempo(s)': results[filename][model_name][i]['tiempo(s)'],
                            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        mongo[result_id].insert_one(data)

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                result.status = ResultStatusEnum.FAILED
                db.session.commit()
                return {"message": "An error occurred during processing"}, 500
            finally:
                # Eliminar archivo temporal
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        result_status.status = ResultStatusEnum.COMPLETED
        db.session.commit()

        return {"message": "Processing completed", "results": processed_files}, 200
