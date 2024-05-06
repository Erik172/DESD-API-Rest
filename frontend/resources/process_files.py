from abc import ABC, abstractmethod
import requests

class Proccesing(ABC):
    """
    Abstract base class for processing files.
    """

    @abstractmethod
    def process_file(self, file, version):
        """
        Abstract method to process a file.

        Args:
            file (str): The file to be processed.
            version (str): The version of the file.

        Returns:
            None
        """
        pass
        
class ImageProccesing(Proccesing):
    """
    A class for image processing.

    Args:
        model (str): The model to be used for processing.

    Attributes:
        model (str): The model to be used for processing.

    Methods:
        process_file: Process a file using the specified model and version.

    """

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