import os
import requests
import base64
from flask import request, jsonify
from flask_restful import Resource
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv

load_dotenv()

class TilDeV1(Resource):
    """
    Represents the TilDeV1 resource.

    This resource handles the POST request for TilDeV1 API endpoint.
    """

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