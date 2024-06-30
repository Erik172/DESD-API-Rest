from ultralytics import YOLO
from datetime import datetime
from src import parse_result_yolov8
import platform
import yaml

class ModelAI:
    """
    Represents a ModelAI object that can be used for prediction tasks.

    Attributes:
        model (str): The name of the model being used.
        results (dict): A dictionary containing the predicted output, execution time, and model information.

    Methods:
        __init__(self, model_name: str) -> None: Initializes a ModelAI object.
        predict(self, image_path: str, task: str = 'classify') -> dict: Predicts the output for the given image.
        _is_intel(self) -> bool: Checks if the processor is from Intel.
    """

    def __init__(self, model_name: str) -> None:
        """
        Initializes a ModelAI object.

        Args:
            model_name (str): The name of the model to be used.

        Raises:
            FileNotFoundError: If the configuration file is not found.
        """
        if self._is_intel():
            with open('models_openvino.yml') as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
        else:
            with open('models.yml') as file:
                config = yaml.load(file, Loader=yaml.FullLoader)

        self.model = config[model_name]
        self.results = {}

    def predict(self, image_path: str, task: str = 'classify') -> dict:
        """
        Predicts the output for the given image using the YOLO model.

        Args:
            image_path (str): The path to the input image.
            task (str, optional): The task to perform. Defaults to 'classify'.

        Returns:
            dict: A dictionary containing the predicted output, execution time, and model information.
        """
        start_time = datetime.now()
        model = YOLO(self.model, verbose=True, task=task)
        response = parse_result_yolov8(model(image_path)[0])
        response['time'] = (datetime.now() - start_time).total_seconds()
        response['model'] = self.model
        self.results = response
        return response

    def _is_intel(self) -> bool:
        if 'intel' in platform.processor().lower():
            return True
        return False
