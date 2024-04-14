import os
import re
import cv2
import requests
import base64
from flask import request, jsonify
from flask_restful import Resource
from inference_sdk import InferenceHTTPClient
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

class TilDeV1(Resource):
    def post(self):
        model_path = 'models/tilde_v1.pt'
        
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

class TilDeV1Remote(Resource):
    def post(self):
        url = "https://api.ultralytics.com/v1/predict/N6gB0vZtjIvrbLqT7s9j"
        headers = {'x-api-key': os.getenv('ULTRALYTICS_API_KEY')}
        data = {"size": 640, "confidence": 0.25, "iou": 0.45}
        image = request.files["image"]
        image = image.read()

        try:
            response = requests.post(url, headers=headers, data=data, files={"image": image})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(response.text)
            return {"error": str(e)}
        
class TilDeV2(Resource):
    def post(self):
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=os.getenv('ROBOFLOW_API_KEY')
        )

        if "image" not in request.files:
            return {"error": "No file uploaded"}
        
        image = request.files["image"]
        image = image.read()
        image = base64.b64encode(image)
        
        response = CLIENT.infer(image.decode(), model_id=os.getenv('ROBOFLOW_MODEL_ID_TILTED_V2'))

        return jsonify(response)