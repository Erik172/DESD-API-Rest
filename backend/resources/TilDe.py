import os
import requests
import base64
from flask import request, jsonify
from flask_restful import Resource
from ultralytics import YOLO
from dotenv import load_dotenv

from src import parse_result_yolov8

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
        response = parse_result_yolov8(response[0])

        return jsonify(response)

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