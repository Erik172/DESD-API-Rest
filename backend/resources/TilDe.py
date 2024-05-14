import os
import base64
import sentry_sdk
import random
from flask import request, jsonify
from flask_restful import Resource
import sentry_sdk.metrics
from ultralytics import YOLO
from datetime import datetime

from src import parse_result_yolov8
from src.filters import apply_filters
from db import Work

class TilDe(Resource):
    def post(self):
        with sentry_sdk.metrics.timing(key="TilDeV1", tags={"model": "TilDeV1"}):
            start_time = datetime.now()
            model_path = 'models/tilde_v1.pt'
            
            model = YOLO(model_path, verbose=True)

            if "image" not in request.files:
                return {"error": "No image found in request"}, 400
            
            request.form = request.form.to_dict()

            if not request.form.get("work_id"):
                request.form["work_id"] = "tilde_test"

            work = Work(request.form["work_id"])
            
            file_name = f'temp/{"".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))}.jpg'
            request.files["image"].save(file_name)

            response = model(file_name)
            response = parse_result_yolov8(response[0])
            response['time'] = (datetime.now() - start_time).total_seconds()
            response['model'] = "TilDeV1"

            response = apply_filters(file_name=file_name, requests=request.form, response=response)

            if request.form.get("filtros"):
                request.form.pop("filtros")
            # unir response y request.form
            documento = request.form | response
            documento['prediccion'] = response['data'][0]['name']
            documento['confianza'] = response['data'][0]['confidence']
            documento.pop("data")
            doc_id = work.save(documento)
            response["_id"] = str(doc_id)

            sentry_sdk.metrics.incr(
                key="TilDeV1Count",
                tags={"model": "TilDeV1"}
            )

            os.remove(file_name)
            return jsonify(response)