from abc import ABC, abstractmethod
from io import BytesIO
import requests

class Proccesing(ABC):
    @abstractmethod
    def process_file(self, file, version):
        pass
        
class ImageProccesing(Proccesing):
    def __init__(self, model):
        self.model = model
        
    def process_file(self, file: dict) -> dict:
        API_URL = f'http://localhost:5000/{self.model}'
        if file.get("type") == "application/pdf":
            response = requests.post(API_URL, files={"image": BytesIO(file.get("data"))}, data=file)
        else:
            response = requests.post(API_URL, files={"image": BytesIO(file.get("data").read())}, data=file)
        response = response.json()

        return response
    
def UploadFile2dict(file):
    """
    Converts a file object to a dictionary.

    Args:
        file (File): The file object to convert.

    Returns:
        dict: A dictionary containing the file's name, type, size, and data.

    """
    return {
        "name": file.name,
        "type": file.type,
        "size": file.size,
        "data": BytesIO(file.read())
    }