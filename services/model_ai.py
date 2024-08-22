from ultralytics import YOLO
from datetime import datetime
from src import parse_result_yolov8
import platform
import yaml

class ModelAI:
    def __init__(self, model_name: str, task: str = 'classify') -> None:
        config_file = 'models.yml' if self._is_intel() else 'models.yml'
        try:
            with open(config_file) as file:
                config = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

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
        start_time = datetime.now()
        result = self.model(image_path)[0]
        self.results = {
            **parse_result_yolov8(result),
            'time': (datetime.now() - start_time).total_seconds(),
            'model': self.model_path
        }
        return self.results

    @staticmethod
    def _is_intel() -> bool:
        """
        Check if the current processor is from Intel.

        Returns:
            bool: True if the processor is from Intel, False otherwise.
        """
        return 'intel' in platform.processor().lower()
