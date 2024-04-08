import os
import requests
from flask import request, jsonify
from flask_restful import Resource
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv

load_dotenv()

class TilDeV1(Resource):
    def post(self):
        url = "https://api.ultralytics.com/v1/predict/N6gB0vZtjIvrbLqT7s9j"
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': os.getenv('ULTRALYTICS_API_KEY')
        }
        data = {
            "size": 640,
            "confidence": 0.25,
            "iou": 0.45
        }
        files = {
            'image': request.files['image']
        }

        try:
            response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
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
        
        response = CLIENT.infer(image, model_id=os.getenv('ROBOFLOW_MODEL_ID_TILTED_V2'))

        return jsonify(response)