import base64
import sentry_sdk
from flask import request, jsonify
from flask_restful import Resource
from ultralytics import YOLO
from datetime import datetime

from src import parse_result_yolov8

class TilDeV1(Resource):
    def post(self):
        with sentry_sdk.start_span(op="TilDeV1", description="Tilted Detection"):
            start_time = datetime.now()
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
            response['time'] = (datetime.now() - start_time).total_seconds()

            sentry_sdk.metrics.distribution(
                key="TilDeV1",
                value=response['time'],
                unit="seconds",
                tags={"model": "TilDeV1"}
            )

            return jsonify(response)