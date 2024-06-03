from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from resources.ModelAI import ModelAI

class DESD(Resource): # DESD (Detection Error on Scan Documents)
    def get(self):
        return {"message": "This is the DESD endpoint"}, 200
    
    def post(self):
        print(request.files)
        if 'file' not in request.files:
            return {"message": "No file part in the request"}, 400
        
        file = request.files['file']
        model_names = request.form.getlist('model_names')

        if file.filename == '':
            return {"message": "No file selected"}, 400
        print(file.filename)
        
        if file:
            filename = secure_filename(file.filename)
            file.save('temp/' + filename)

            results = {}
            for model_name in model_names:
                model = ModelAI(model_name)
                results[model_name] = model.predict('temp/' + filename)

            return results, 200