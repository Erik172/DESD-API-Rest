from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from src import save_results
import os

from resources import ModelAI

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

    def post(self):
        """
        Handles the POST request for file upload, prediction, and result saving.

        This method expects a file to be uploaded along with the request. It checks if the file exists,
        saves it temporarily, performs predictions using specified models, and saves the results.
        The results are returned as a dictionary.

        Args:
            None

        Returns:
            A dictionary containing the prediction results.

        Raises:
            None

        """

        if 'file' not in request.files:
            return {"message": "No file part in the request"}, 400
        
        file = request.files['file']
        model_names = request.form.getlist('model_names')
        resultado_id = request.form.get('result_id')

        if file.filename == '':
            return {"message": "No file selected"}, 400
        
        results = {}
        if file:
            filename = secure_filename(file.filename)
            file.save('temp/' + filename)
            results[filename] = {}

            if filename.endswith('.pdf'):
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

            os.remove('temp/' + filename)

            if save_results(results, resultado_id) == False:
                return {"message": "Error saving results"}, 500

            return results, 200
        
        return {"message": "Something went wrong"}, 500
        