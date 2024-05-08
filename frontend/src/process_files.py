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
        """
        Process a file using the specified model and version.

        Args:
            file: The file to be processed.
            version (str): The version of the model to be used.
            data (dict): Additional data to be sent along with the file.

        Returns:
            dict: The response from the API.

        """
        API_URL = f'http://localhost:5000/{self.model}/{version}'

        response = requests.post(API_URL, files={"image": file}, data=data)
        response = response.json()

        return response