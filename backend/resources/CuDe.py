from dotenv import load_dotenv
import base64
from flask import request, jsonify
from flask_restful import Resource
from ultralytics import YOLO

from src import parse_result_yolov8

load_dotenv()

class CuDeV1(Resource):
    def post(self):
        model_path = 'models/cude_v1.pt'
        
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