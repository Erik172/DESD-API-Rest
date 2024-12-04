from PIL import Image
from app import db
import pytesseract
import hashlib
import os

class DuDeBase:
    def __init__(self, data_dir: str):
        self.duplicates = {}
        self.hash_map = {}
        self.work_status = None
        self.data_dir = data_dir
        self.list_of_files = os.listdir(data_dir)
             
    def find_duplicates(self):
        for file in self.list_of_files:
            file_path = os.path.join(self.data_dir, file)
            text = pytesseract.image_to_string(Image.open(file_path))
            
            if not text:
                self.duplicates.setdefault("texto_no_identificado", []).append(file)
                continue
            
            text_hash = hashlib.md5(text.encode()).hexdigest()
            
            if text_hash in self.hash_map:
                self.duplicates.setdefault(self.hash_map[text_hash], []).append(file)
            else:
                self.hash_map[text_hash] = file
                
                
            