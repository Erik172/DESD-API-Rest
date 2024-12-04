from ultralytics import YOLO
from datetime import datetime
from app.utils import parse_result_yolov8
from pathlib import Path

import yaml

class ModelAIService:
    """
    Clase ModelAIService para cargar y utilizar un modelo de IA YOLO para realizar predicciones en imágenes.
    Métodos:
        __init__(model_name: str, task: str = 'classify') -> None:
        predict(image_path: str) -> dict:
    """
    
    def __init__(self, model_name: str, task: str = 'classify') -> None:
        """
        Inicializa una instancia del servicio de modelo AI.
        Args:
            model_name (str): El nombre del modelo a cargar desde el archivo de configuración.
            task (str, opcional): La tarea que realizará el modelo. Por defecto es 'classify'.
        Raises:
            FileNotFoundError: Si el archivo de configuración 'models.yml' no se encuentra.
            ValueError: Si el modelo especificado no se encuentra en el archivo de configuración.
        Atributos:
            model_path (str): La ruta del modelo cargado desde el archivo de configuración.
            model (YOLO): La instancia del modelo YOLO cargado.
            results (dict): Un diccionario para almacenar los resultados del modelo.
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
        Realiza una predicción utilizando el modelo de IA en la imagen especificada.

        Args:
            image_path (str): La ruta de la imagen en la que se realizará la predicción.

        Returns:
            dict: Un diccionario que contiene los resultados de la predicción, incluyendo el tiempo de procesamiento y el modelo utilizado.

        Raises:
            RuntimeError: Si la predicción falla, se lanza una excepción con el mensaje de error correspondiente.
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
