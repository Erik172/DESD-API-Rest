import os
import base64
import random
import sentry_sdk
from flask import request, jsonify
from flask_restful import Resource
import sentry_sdk.metrics
from ultralytics import YOLO
from datetime import datetime

from src import parse_result_yolov8, data_file_validation
from src.filters import apply_filters

from db import Work

class CuDeV1(Resource):
    def post(self):
        with sentry_sdk.metrics.timing(key="CuDeV1", tags={"model": "CuDeV1"}):
            start_time = datetime.now()
            model_path = 'models/cude_v1.pt'
            
            model = YOLO(model_path, verbose=True)

            if "image" not in request.files:
                return {"error": "No file uploaded"}
            
            request.form = data_file_validation(request)

            work = Work(request.form["work_id"])

            image = request.files["image"]
            image = image.read()
            image = base64.b64encode(image)
            file_name = f'temp/{"".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))}.jpg'
            with open(file_name, 'wb') as f:
                f.write(base64.b64decode(image))

            response = model(file_name)
            response = parse_result_yolov8(response[0])
            response['time'] = (datetime.now() - start_time).total_seconds()
            response['model'] = "CuDeV1"

            response = apply_filters(file_name=file_name, requests=request.form, response=response)

            if request.form.get("filtros"):
                request.form.pop("filtros")
            # unir response y request.form
            documento = request.form | response
            documento['prediccion'] = response['data'][0]['name']
            documento['tiempo'] = response['time']
            documento.pop("data")
            doc_id = work.save(documento)
            response['_id'] = str(doc_id)

            sentry_sdk.metrics.incr(
                key="CuDeV1Count",
                tags={"model": "CuDeV1"}
            )

            os.remove(file_name)
            return jsonify(response)