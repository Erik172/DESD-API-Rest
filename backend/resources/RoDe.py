import base64
import sentry_sdk
from flask import request, jsonify
from flask_restful import Resource
import sentry_sdk.metrics
from ultralytics import YOLO
from datetime import datetime

from src import parse_result_yolov8


class RoDeV1(Resource):
    def post(self):
        with sentry_sdk.start_span(op="RoDeV1", description="Rotation Detection"):
            start_time = datetime.now()
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
            response = parse_result_yolov8(response[0])
            response['time'] = (datetime.now() - start_time).total_seconds()

            sentry_sdk.metrics.distribution(
                key="RoDeV1",
                value=response['time'],
                unit="seconds",
                tags={"model": "RoDeV1"}
            )

            return jsonify(response)