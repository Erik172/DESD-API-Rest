from PIL import Image
import pytesseract
import os

class DuDeBase:
    """
    The DuDeBase class represents a base class for performing operations on data files.

    Attributes:
        hash_map (dict): A dictionary that stores the initial characters of the text as keys and the corresponding file names as values.
        duplicates (dict): A dictionary that stores the duplicate files found.
        data_dir (str): The directory path where the data files are located.
        list_of_files (list): A list of file names in the data directory.

    Methods:
        __init__(self, data_dir: str): Initializes an instance of the DudeBase class.
        _ocr_core(self, filename: str) -> str: Performs OCR (Optical Character Recognition) on the given image file.
        find_duplicates(self, num_initial_chars: int = 3) -> None: Finds and identifies duplicate files based on their initial characters.
        get_duplicates(self) -> dict: Returns a dictionary containing the duplicates found.
        get_hash_map(self) -> dict: Returns the hash map associated with the DudeBase object.
    """

    def __init__(self, data_dir: str):
        """
        Initializes an instance of the DudeBase class.

        Args:
            data_dir (str): The directory path where the data files are located.
        """
        self.hash_map = {}
        self.duplicates = {}
        self.data_dir = data_dir
        self.list_of_files = os.listdir(data_dir)

    def _ocr_core(self, filename: str) -> str:
        """
        Perform OCR (Optical Character Recognition) on the given image file.

        Args:
            filename (str): The path to the image file.

        Returns:
            str: The extracted text from the image.
        """
        text = pytesseract.image_to_string(Image.open(filename))
        return text
    
    def find_duplicates(self, num_initial_chars: int = 10) -> None:
        """
        Finds and identifies duplicate files based on their initial characters.

        Args:
            num_initial_chars (int): The number of initial characters to consider for the key in the hash map.

        Returns:
            None
        """
        for file in self.list_of_files:
            file_path = os.path.join(self.data_dir, file)
            text = self._ocr_core(file_path)
            if len(text) < num_initial_chars:
                initial = text
            initial = text[:num_initial_chars]

            if len(text) == 0:
                if "texto_no_identificado" not in self.duplicates:
                    self.duplicates["texto_no_identificado"] = [file]
                else:
                    self.duplicates["texto_no_identificado"].append(file)
                continue

            if initial in self.hash_map:
                for files_same_initial in self.hash_map[initial]:
                    file_text = self._ocr_core(os.path.join(self.data_dir, files_same_initial))
                    if file_text[:1000] == text[:1000]:
                        if files_same_initial in self.duplicates and file not in self.duplicates[files_same_initial]:
                            self.duplicates[files_same_initial].append(file)
                        elif files_same_initial not in self.duplicates:
                            self.duplicates[files_same_initial] = [file]
                        break
                self.hash_map[initial].append(file)
            else:
                self.hash_map[initial] = [file]


    def get_duplicates(self) -> dict:
        """
        Returns a dictionary containing the duplicates found.
        
        Returns:
            dict: A dictionary containing the duplicates found.
        """
        return self.duplicates

    def get_hash_map(self) -> dict:
        """
        Returns the hash map associated with the DudeBase object.

        Returns:
            dict: The hash map containing the data.
        """
        return self.hash_map
