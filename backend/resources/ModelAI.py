from ultralytics import YOLO
from datetime import datetime
from src import parse_result_yolov8

class ModelAI:
    def __init__(self, model_name: str) -> None:
        self.model = model_name
        self.results = {}

    def predict(self, image_path: str) -> dict:
        start_time = datetime.now()
        model = YOLO(self.model, verbose=True)
        response = parse_result_yolov8(model(image_path)[0])
        response['time'] = (datetime.now() - start_time).total_seconds()
        response['model'] = self.model
        self.results = response
        return response
    
    def get_results(self) -> dict:
        return parse_result_yolov8(self.results)
    

rode = ModelAI('models/rode_v2.5.pt')
print(rode.predict('temp/imagen.jpg'))

