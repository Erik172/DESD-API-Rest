import re
import base64
from flask import request, jsonify
from flask_restful import Resource
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

class RoDeV1(Resource):
    def post(self):
        model_path = 'models/rode_v1.pt'
        
        model = YOLO(model_path, verbose=True)

        if "image" not in request.files:
            return {"error": "No file uploaded"}
        
        image = request.files["image"]
        image = image.read()
        image = base64.b64encode(image)
        with open('temp.png', 'wb') as f:
            f.write(base64.b64decode(image))

        response = model('temp.png')
        response = self.parse_result(response[0])

        return jsonify(response)

    def parse_result(self, result):
        verbose = result.verbose()

        verbose = verbose.split(',')
        verbose = [v.strip() for v in verbose]
        result_dict = {'data': []}
        for i in verbose:
            try:
                r = re.split(r'(\d+\.\d+)', i)
                class_name = r[0].strip()
                confidence = float(r[1])

                result_dict['data'].append({
                    'name': class_name,
                    'confidence': confidence
                })
            except:
                pass

        return result_dict