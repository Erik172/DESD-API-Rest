from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
from ultralytics import YOLO
import random
import os

from src import parse_result_yolov8
from src.filters import apply_filters

from db import Work


class RoDe(Resource):
    def get(self):
        return {"message": "RoDeV1"}, 200
    
    def post(self):
        start_time = datetime.now()
        model_path = 'models/rode_v2.5.pt'
            
        model = YOLO(model_path, verbose=True)

        if "image" not in request.files:
            return {"error": "No image found in request"}, 400

        request.form = request.form.to_dict()         

        if not request.form.get("work_id"):
            request.form["work_id"] = "rode_test"

        work = Work(request.form["work_id"])
            
        file_name = f'temp/{"".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))}.jpg'
        request.files["image"].save(file_name)

        response = parse_result_yolov8(model(file_name)[0])
        response['time'] = (datetime.now() - start_time).total_seconds()
        response['model'] = "RoDeV2.5"

        if request.form.get("filtros"):
            response = apply_filters(file_name=file_name, requests=request.form, response=response)
            request.form.pop("filtros")

        documento = request.form | response
        documento.pop("data")
        documento['prediccion'] = response['data'][0]['name']
        documento['confianza'] = response['data'][0]['confidence']
        doc_id = work.save(documento)
        response["_id"] = str(doc_id)

        try:
            os.remove(file_name)
        except PermissionError:
            print(f"Error al eliminar el archivo {file_name}")

        return jsonify(response)
