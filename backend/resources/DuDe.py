from PIL import Image
from flask import request
from flask_restful import Resource
import pytesseract
import os

class DuDe:
    def __init__(self, data_dir):
        self.hash_map = {}
        self.duplicates = {}
        self.data_dir = data_dir
        self.list_of_files = os.listdir(data_dir)

    def ocr_core(self, filename):
        text = pytesseract.image_to_string(Image.open(filename))
        return text

    def find_duplicates(self, num_initial_chars=2):
        for file in self.list_of_files:
            file_path = os.path.join(self.data_dir, file)
            text = self.ocr_core(file_path)
            initial = text[:num_initial_chars]

            if initial in self.hash_map:
                for files_same_initial in self.hash_map[initial]:
                    file_text = self.ocr_core(os.path.join(self.data_dir, files_same_initial))
                    if file_text[:50] == text[:50]:
                        self.duplicates.setdefault(files_same_initial, []).append(file)
                self.hash_map[initial].append(file)
            else:
                self.hash_map[initial] = [file]

    def get_duplicates(self) -> dict:
            return self.duplicates

    def get_hash_map(self) -> dict:
            return self.hash_map
    
class DuDeV1(Resource):
    def post(self, dir_name: str):
        file = request.files['file']
        if not os.path.exists(f'temp/{dir_name}'):
            os.makedirs(f'temp/{dir_name}')

        file.save(f'temp/{dir_name}/{file.filename}')
        return {"message": f"Archivo {file.filename} guardado exitosamente."}
    
    def get(self, dir_name: str):
        dude = DuDe(f'temp/{dir_name}')
        dude.find_duplicates()
        return dude.get_duplicates()
    
    def delete(self, dir_name: str):
        if os.path.exists(f'temp/{dir_name}'):
            os.remove(f'temp/{dir_name}')

            return {"message": "Archivos eliminados exitosamente."}

        return {"message": "No se encontraron archivos para eliminar."}