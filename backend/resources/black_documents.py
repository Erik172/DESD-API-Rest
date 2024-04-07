from dotenv import load_dotenv
import os
import base64
from flask import request, jsonify
from flask_restful import Resource
from inference_sdk import InferenceHTTPClient

load_dotenv()

class BlackDocumentsDetectorModel(Resource):
    """
    A Flask RESTful resource for detecting black documents using a pre-trained model.

    This resource accepts a POST request with an image file and returns the inference results.

    Attributes:
        CLIENT (InferenceHTTPClient): An instance of the InferenceHTTPClient class for making API requests.
    """

    def post(self):
        """
        Handles the POST request for detecting black documents.

        Returns:
            A JSON response containing the inference results.
        """
        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=os.getenv("ROBOFLOW_API_KEY")
        )

        print(request.files)
        if "image" not in request.files:
            return jsonify({"error": "No file uploaded"})

        image = request.files["image"]
        image = image.read()
        image = base64.b64encode(image)  # Convert image to base64

        response = CLIENT.infer(image.decode(), model_id=os.getenv("ROBOFLOW_MODEL_ID"))

        return jsonify(response)