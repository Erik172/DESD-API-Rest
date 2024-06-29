from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from PIL import Image, ImageSequence
from flask_restful import Resource
from flask import request
from src import save_results
from datetime import datetime
import os

from services import ModelAI
from database import WorkStatus, sql_db


class DESD(Resource):
    """
    DESD (Detection Error on Scan Documents) class for handling document scanning and prediction.

    This class provides a POST method to handle file uploads, perform predictions using specified models,
    and save the results.

    Attributes:
        None

    Methods:
        post: Handles the POST request for file upload, prediction, and result saving.

    """
    def get(self):
            """
            Retrieves a list of models from the 'models.yml' file.

            Returns:
                A tuple containing the list of models and the HTTP status code 200.
            """
            import yaml

            with open('models.yml') as file:
                models = yaml.full_load(file)

            models = list(models.keys())

            return models, 200

    def post(self):
        if 'result_id' not in request.form:
             return {"message": "No result_id selected"}, 400
        
        if 'models' not in request.form:
            return {"message": "No models selected"}, 400

        if 'files' not in request.files:
            return {"message": "No file part in the request"}, 400
        
        model_names = request.form.getlist('models')
        files = request.files.getlist('files')
        result_id = request.form.get('result_id')

        work_status = WorkStatus(
            result_id=result_id,
            status='in_progress',
            files_processed=0,
            total_files=len(files),
            percentage=0
        )

        if 'inclinacion' in model_names:
            work_status.tilted = True
        if 'rotacion' in model_names:
            work_status.rotation = True
        if 'corte_informacion' in model_names:
            work_status.cut_information = True

        sql_db.session.add(work_status)
        sql_db.session.commit()
    
        for file in files:
            results = {}
            filename = secure_filename(file.filename)
            file.save('temp/' + filename)
            results[filename] = {}

            ### PDF
            if filename.lower().endswith('.pdf'):
                self._pdf_process(model_names, results, filename)

            ### TIFF
            elif filename.lower().endswith('.tiff') or filename.lower().endswith('.tif'):
                self._tiff_process(model_names, results, filename)
            
            ### Image
            else:
                for model_name in model_names:
                    model = ModelAI(model_name)
                    model_results = model.predict('temp/' + filename)
                    results[filename][model_name] = {
                        '0': {
                            'prediccion': model_results['data'][0]['name'],
                            'confianza': model_results['data'][0]['confidence'],
                            'tiempo(s)': model_results['time']
                        }
                    }

            try:
                os.remove('temp/' + filename)
            except PermissionError:
                pass

            if save_results(results, result_id) == False:
                work_status.status = 'failed'
                sql_db.session.commit()

            work_status.files_processed += 1
            work_status.percentage = (work_status.files_processed / work_status.total_files) * 100
            sql_db.session.commit()
        
        work_status.status = 'completed'
        sql_db.session.commit()

        return {"message": "Results saved successfully", "result_id": result_id}, 200

    def _tiff_process(self, model_names: list, results: dict, filename: str):
        """
        Process a TIFF image by converting each page to JPEG and making predictions using the specified models.

        Args:
            model_names (list): A list of model names to use for prediction.
            results (dict): A dictionary to store the prediction results.
            filename (str): The name of the TIFF file to process.

        Returns:
            None
        """
        tiff_image = Image.open('temp/' + filename)
        for model_name in model_names:
            model = ModelAI(model_name)
            results[filename][model_name] = {}
            for i, page in enumerate(ImageSequence.Iterator(tiff_image)):
                jpg_file_path = f"temp/{filename}_{i}.jpg"
                page.save(jpg_file_path, "JPEG")
                model_results = model.predict(jpg_file_path)
                results[filename][model_name][str(i)] = {
                    'prediccion': model_results['data'][0]['name'],
                    'confianza': model_results['data'][0]['confidence'],
                    'tiempo(s)': model_results['time']
                }
                try:
                    os.remove(jpg_file_path)
                except PermissionError:
                    pass

    def _pdf_process(self, model_names, results, filename):
        images = convert_from_path('temp/' + filename)
        for model_name in model_names:
            model = ModelAI(model_name)
            results[filename][model_name] = {}
            for i, image in enumerate(images):
                image.save('temp/' + filename + f'_{i}.png')
                model_results = model.predict('temp/' + filename + f'_{i}.png')
                results[filename][model_name][str(i)] = {
                            'prediccion': model_results['data'][0]['name'],
                            'confianza': model_results['data'][0]['confidence'],
                            'tiempo(s)': model_results['time']
                        }
                os.remove('temp/' + filename + f'_{i}.png')

class DESDStatus(Resource):
    def get(self, result_id: str):
        work_status = WorkStatus.query.filter_by(result_id=result_id).first()
        if work_status is None:
            return {"message": "Result not found"}, 404
        
        print(work_status.start_time)

        return {
            "result_id": work_status.result_id,
            "status": work_status.status,
            "files_processed": work_status.files_processed,
            "total_files": work_status.total_files,
            "percentage": work_status.percentage,
            "tilted": work_status.tilted,
            "rotation": work_status.rotation,
            "cut_information": work_status.cut_information,
            "start_time": datetime.strftime(work_status.start_time, "%Y-%m-%d %H:%M:%S"),
            "last_updated": datetime.strftime(work_status.last_updated, "%Y-%m-%d %H:%M:%S")
        }, 200
    
    def delete(self, result_id: str):
        work_status = WorkStatus.query.filter_by(result_id=result_id).first()
        if work_status is None:
            return {"message": "Result not found"}, 404

        sql_db.session.delete(work_status)
        sql_db.session.commit()

        return {"message": "Result deleted successfully"}, 200