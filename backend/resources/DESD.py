from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from PIL import Image, ImageSequence
from flask_restful import Resource
from flask import request
from src import save_results
import yaml
import os

from services import ModelAI
from database import WorkStatus, sql_db


class DESD(Resource):
    def get(self):
            with open('models.yml') as file:
                models = list(yaml.safe_load(file).keys())

            return models, 200

    def post(self):
        required_fields = ['result_id', 'models', 'files']
        for field in required_fields:
            if field not in request.form and field != 'files':
                return {"message": f"No {field} provided"}, 400
            elif field == 'files' and field not in request.files:
                return {"message": "No file part in the request"}, 400

        model_names = request.form.getlist('models')
        files = request.files.getlist('files')
        result_id = request.form.get('result_id')

        work_status = self._create_work_status(result_id, len(files), model_names)

        models = {model: ModelAI(model) for model in model_names if model in ['inclinacion', 'rotacion', 'corte_informacion']}

        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join('temp', filename)
            file.save(file_path)

            results = {filename: {}}

            if filename.lower().endswith('.pdf'):
                self._pdf_process(models, results, filename, file_path)
            elif filename.lower().endswith(('.tiff', '.tif')):
                self._tiff_process(models, results, filename, file_path)
            else:
                self._process_image(models, results, filename, file_path)

            self._cleanup_file(file_path)

            if not save_results(results, result_id):
                work_status.status = 'failed'
                sql_db.session.commit()
                return {"message": "Failed to save results"}, 500

            self._update_work_status(work_status)

        work_status.status = 'completed'
        sql_db.session.commit()

        return {"message": "Processing completed successfully"}, 200

    def _create_work_status(self, result_id, total_files, model_names):
        work_status = WorkStatus(
            result_id=result_id,
            status='in_progress',
            files_processed=0,
            total_files=total_files,
            percentage=0,
            tilted='inclinacion' in model_names,
            rotation='rotacion' in model_names,
            cut_information='corte_informacion' in model_names
        )
        sql_db.session.add(work_status)
        sql_db.session.commit()
        return work_status

    def _update_work_status(self, work_status):
        work_status.files_processed += 1
        work_status.percentage = (work_status.files_processed / work_status.total_files) * 100
        sql_db.session.commit()

    def _tiff_process(self, models, results, filename, file_path):
        tiff_image = Image.open(file_path)
        for model_name, model in models.items():
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
                self._cleanup_file(jpg_file_path)

    def _pdf_process(self, models, results, filename, file_path):
        images = convert_from_path(file_path, thread_count=os.cpu_count())
        for model_name, model in models.items():
            results[filename][model_name] = {}
            for i, image in enumerate(images):
                image.save(f'temp/{filename}_{i}.png')
                model_results = model.predict(f'temp/{filename}_{i}.png')
                results[filename][model_name][str(i)] = {
                    'prediccion': model_results['data'][0]['name'],
                    'confianza': model_results['data'][0]['confidence'],
                    'tiempo(s)': model_results['time']
                }
                self._cleanup_file(f'temp/{filename}_{i}.png')

    def _process_image(self, models, results, filename, file_path):
        for model_name, model in models.items():
            model_results = model.predict(file_path)
            results[filename][model_name] = {
                '0': {
                    'prediccion': model_results['data'][0]['name'],
                    'confianza': model_results['data'][0]['confidence'],
                    'tiempo(s)': model_results['time']
                }
            }

    def _cleanup_file(self, file_path):
        try:
            os.remove(file_path)
        except PermissionError:
            print(f"Unable to remove file: {file_path}")