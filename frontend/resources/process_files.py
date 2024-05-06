from abc import ABC, abstractmethod
import requests

class Proccesing(ABC):
    @abstractmethod
    def process_file(self, file, version):
        pass    
        
class ImageProccesing(Proccesing):
    def __init__(self, model):
        self.model = model
        
    def process_file(self, file, version, data: dict):
        API_URL = f'http://localhost:5000/{self.model}/{version}'

        response = requests.post(API_URL, files={"image": file}, data=data)
        response = response.json()

        return response