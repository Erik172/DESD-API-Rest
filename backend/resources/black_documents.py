from flask import request, jsonify
from flask_restful import Resource
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv
import base64
import os

load_dotenv()

class BlackDocumentsDetectorModel(Resource):
    def post(self):
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key= os.getenv("ROBOFLOW_API_KEY")
        )

        print(request.files)
        if "image" not in request.files:
            return jsonify({"error": "No file uploaded"})

        image = request.files["image"]
        image = image.read()
        image = base64.b64encode(image)  # Convert image to base64

        response = CLIENT.infer(image.decode(), model_id=os.getenv("ROBOFLOW_MODEL_ID"))

        return jsonify(response)