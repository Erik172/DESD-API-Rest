from flask import request, jsonify
from flask_restful import Resource
from ultralytics import YOLO
import base64
import re

from src import parse_result_yolov8

models = {
    "tilde_v1": "models/tilde_v1.pt",
    "rode_v1": "models/rode_v1.pt"
}

class Audit(Resource):
    def post(self):
        results = {}
        if "image" not in request.files:
            return {"error": "No file uploaded"}
        
        image = request.files["image"]
        image = image.read()
        image = base64.b64encode(image)
        with open('temp.png', 'wb') as f:
            f.write(base64.b64decode(image))

        tilde_model = YOLO(models["tilde_v1"])
        rode_model = YOLO(models["rode_v1"])

        tilde_results = tilde_model("temp.png")
        tilde_results = parse_result_yolov8(tilde_results[0])

        rode_results = rode_model("temp.png")
        rode_results = parse_result_yolov8(rode_results[0])

        results["tilde"] = tilde_results['data'][0]
        results["rode"] = rode_results['data'][0]

        return jsonify(results)