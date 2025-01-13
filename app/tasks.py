from app import db, create_app
from app.models import Result, ResultStatus, ResultStatusEnum
from app.services import ModelAIService
from app.resources.desd.desd_processing import DESDProcessing
from datetime import datetime
from pymongo import MongoClient
import os
import zipfile
import tempfile
from werkzeug.utils import secure_filename
import shutil

def process_desd_task(result_id, model_names, file_contents):
    app = create_app()
    with app.app_context():
        mongo_client = MongoClient(app.config['MONGO_URI'])
        mongo = mongo_client['desd']
        
        result = Result.query.filter_by(collection_id=result_id).first()
        if not result:
            return {"message": "Result not found"}, 404

        result_status = ResultStatus.query.filter_by(result_id=result.id).first()
        if not result_status:
            return {"message": "Result status not found"}, 404

        models = {model: ModelAIService(model) for model in model_names if model in ['inclinacion', 'rotacion', 'corte informacion']}

        processed_files = 0
        temp_dir = tempfile.mkdtemp()

        try:
            for filename, content in file_contents:
                temp_path = os.path.join(temp_dir, secure_filename(filename))
                
                with open(temp_path, 'wb') as f:
                    f.write(content)
                
                if filename.lower().endswith('.zip'):
                    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    os.remove(temp_path)
                    
            result_status.total_files = len(os.listdir(temp_dir))
            result_status.last_updated_at = db.func.now()
            db.session.commit()

            for root, _, extracted_files in os.walk(temp_dir):
                for extracted_file in extracted_files:
                    file_path = os.path.join(root, extracted_file)
                    results = {extracted_file: {}}

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
                        result_status.status = ResultStatusEnum.FAILED
                        db.session.commit()
                        print(e)
                        return {"message": f"An error occurred during processing: {e}"}, 500
                    finally:
                        print(f"Processed {extracted_file}")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        
            result_status.status = ResultStatusEnum.COMPLETED
            db.session.commit()

            return {"message": "Processing completed", "results": processed_files}, 200
        
        except Exception as e:
            result_status.status = ResultStatusEnum.FAILED
            db.session.commit()
            print(e)
            return {"message": f"An error occurred during processing: {e}"}, 500

        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)