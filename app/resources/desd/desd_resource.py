from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource
from flask import request
from app.services import ModelAIService
from app.models import Result, ResultStatusEnum, ResultStatus
from app import db, mongo
from datetime import datetime
import os
import zipfile
import tempfile
from .desd_processing import DESDProcessing

class DESDResource(Resource):
    #TODO: Dejar de manejar los modelos en un archivo de configuración a base de datos
    # FIXME: Actualizar modelos para evitar FP en imagenes pequeñas
    @jwt_required()
    def post(self):
        required_fields = ['result_id', 'models']
        missing_fields = [field for field in required_fields if field not in request.form]

        if missing_fields:
            print(f"Missing fields: {missing_fields}")
            return {"message": f"No {', '.join(missing_fields)} provided"}, 400
        
        if 'files' not in request.files:
            print("No file part in the request")
            return {"message": "No file part in the request"}, 400

        model_names = request.form.get('models').split(',')
        files = request.files.getlist('files')
        result_id = request.form.get('result_id')
        
        # Verificar y crear el resultado si es necesario
        result = Result.query.filter_by(collection_id=result_id).first()
        if result:            
            result_status = ResultStatus.query.filter_by(result_id=result.id).first()
            
            if result_status.status in [ResultStatusEnum.RUNNING]:
                return {"message": f"The result has status {result_status.status}"}, 400
            
            if result_status.status == ResultStatusEnum.COMPLETED:
                result_status.models = ','.join(model_names)
                result_status.status = ResultStatusEnum.PENDING
                result_status.created_at = db.func.now()
                result_status.last_updated_at = db.func.now()
                db.session.commit()
        else:
            result = Result(
                collection_id=result_id, 
                user_id=current_user.id,
                created_at=db.func.now(),
                updated_at=db.func.now()
            )
            db.session.add(result)
            db.session.commit()

            result_status = ResultStatus(
                result_id=result.id,
                status=ResultStatusEnum.PENDING,
                total_files=len(files),
                total_files_processed=0,
                model_names=','.join(model_names),
                last_updated_at=db.func.now()
            )
            db.session.add(result_status)
            db.session.commit()

        models = {model: ModelAIService(model) for model in model_names if model in ['inclinacion', 'rotacion', 'corte informacion']}

        processed_files = 0
        temp_dir = tempfile.mkdtemp()

        try:
            for file in files:
                filename = secure_filename(file.filename)
                temp_path = os.path.join(temp_dir, filename)
                
                # Streaming: escribir el archivo mientras se lee en trozos
                with open(temp_path, 'wb') as f:
                    while chunk := file.stream.read(2 * 1024 * 1024): 
                        print(f"Writing chunk of {len(chunk)} bytes")
                        f.write(chunk)
                
                if filename.lower().endswith('.zip'):
                    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    os.remove(temp_path)  # Eliminar el archivo ZIP después de extraerlo
                    
            result_status.total_files = len(os.listdir(temp_dir))
            result_status.last_updated_at = db.func.now()
            db.session.commit()

            # Procesar todos los archivos extraídos
            for root, _, extracted_files in os.walk(temp_dir):
                for extracted_file in extracted_files:
                    file_path = os.path.join(root, extracted_file)
                    results = {extracted_file: {}}

                    # Procesa el archivo según su extensión
                    try:
                        processed_files += 1
                        result_status.current_file = extracted_file
                        result_status.status = ResultStatusEnum.RUNNING
                        result_status.total_files_processed = processed_files
                        result_status.last_updated_at = db.func.now()
                        db.session.commit()
                        
                        if extracted_file.lower().endswith('.pdf'):
                            DESDProcessing().process_pdf(models, results, extracted_file, file_path)
                        elif extracted_file.lower().endswith(('.tiff', '.tif')):
                            DESDProcessing().process_tiff(models, results, extracted_file, file_path)
                        else:
                            DESDProcessing().process_image(models, results, extracted_file, file_path)

                        # Guardar resultados en la base de datos después de procesar cada archivo
                        for model_name in results[extracted_file]:
                            for i in results[extracted_file][model_name]:
                                data = {
                                    'archivo ': extracted_file,
                                    'pagina': int(i) + 1,
                                    'modelo': model_name,
                                    'prediccion': results[extracted_file][model_name][i]['prediccion'],
                                    'confianza': results[extracted_file][model_name][i]['confianza'],
                                    'tiempo(s)': results[extracted_file][model_name][i]['tiempo(s)'],
                                    'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }
                                mongo[result_id].insert_one(data)

                    except Exception as e:
                        print(f"Error processing {extracted_file}: {e}")
                        result.status = ResultStatusEnum.FAILED
                        db.session.commit()
                        return {"message": "An error occurred during processing"}, 500
                    finally:
                        # Eliminar archivo temporal
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        
            result_status.status = ResultStatusEnum.COMPLETED
            db.session.commit()

            return {"message": "Processing completed", "results": processed_files}, 200
        
        except Exception as e:
            print(f"Error processing files: {e}")
            result.status = ResultStatusEnum.FAILED
            db.session.commit()
            return {"message": "An error occurred during processing"}, 500

        finally:
            # Eliminar el directorio temporal
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
