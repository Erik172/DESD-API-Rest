from ultralytics import YOLO
from datetime import datetime
from src import parse_result_yolov8
from pathlib import Path

import yaml

class ModelAIService:
    """
    A service class for handling AI model predictions.
    """

    def __init__(self, model_name: str, task: str = 'classify') -> None:
        """
        Initializes the ModelAIService with the specified model name and task.

        Args:
            model_name (str): The name of the model to load.
            task (str): The task for the model (default is 'classify').
        """
        config_file = Path('models.yml')
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

        with config_file.open() as file:
            config = yaml.safe_load(file)

        self.model_path = config.get(model_name)
        if not self.model_path:
            raise ValueError(f"Model '{model_name}' not found in configuration.")
        
        self.model = YOLO(self.model_path, verbose=True, task=task)
        self.results = {}

    def predict(self, image_path: str) -> dict:
        """
        Predicts the output for the given image path using the model.

        Args:
            image_path (str): The path to the input image.

        Returns:
            dict: A dictionary containing the prediction results, including the parsed result,
                  execution time, and model path.
        """
        try:
            start_time = datetime.now()
            result = self.model(image_path)[0]
            self.results = {
                **parse_result_yolov8(result),
                'time': (datetime.now() - start_time).total_seconds(),
                'model': self.model_path
            }
            return self.results
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
