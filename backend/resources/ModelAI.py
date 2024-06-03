from ultralytics import YOLO
from datetime import datetime
from src import parse_result_yolov8
import yaml

class ModelAI:
    def __init__(self, model_name: str) -> None:
        with open('models.yml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.model = config[model_name]
        self.results = {}

    def predict(self, image_path: str) -> dict:
        """
        Predicts the objects in the given image using the YOLO model.

        Args:
            image_path (str): The path to the image file.

        Returns:
            dict: A dictionary containing the predicted objects and additional information.
                - 'objects': A list of predicted objects.
                - 'time': The execution time in seconds.
                - 'model': The name of the model used for prediction.
        """
        start_time = datetime.now()
        model = YOLO(self.model, verbose=True)
        response = parse_result_yolov8(model(image_path)[0])
        response['time'] = (datetime.now() - start_time).total_seconds()
        response['model'] = self.model
        self.results = response
        return response
    
    def get_results(self) -> dict:
        return parse_result_yolov8(self.results)
