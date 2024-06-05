from PIL import Image
from flask import request
from flask_restful import Resource
from datetime import datetime
import pytesseract
import os

#TODO: Separar esto en un archivo aparte
class DuDeBase:
    def __init__(self, data_dir):
        self.hash_map = {}
        self.duplicates = {}
        self.data_dir = data_dir
        self.list_of_files = os.listdir(data_dir)

    def ocr_core(self, filename):
        text = pytesseract.image_to_string(Image.open(filename))
        return text

    def find_duplicates(self, num_initial_chars=3):
        for file in self.list_of_files:
            file_path = os.path.join(self.data_dir, file)
            text = self.ocr_core(file_path)
            initial = text[:num_initial_chars]

            if len(text) == 0:
                if not "texto_no_identificado" in self.duplicates:
                    self.duplicates["texto_no_identificado"] = [file]
                else:
                    self.duplicates["texto_no_identificado"].append(file)
                    
                continue

            if initial in self.hash_map:
                for files_same_initial in self.hash_map[initial]:
                    file_text = self.ocr_core(os.path.join(self.data_dir, files_same_initial))
                    if file_text[:100] == text[:100]:
                        if files_same_initial in self.duplicates:
                            if file not in self.duplicates[files_same_initial]:  # Evitar duplicados
                                self.duplicates[files_same_initial].append(file)
                        else:
                            self.duplicates[files_same_initial] = [file]
                        break  # Detener la búsqueda después de encontrar un duplicado
                self.hash_map[initial].append(file)
            else:
                self.hash_map[initial] = [file]


    def get_duplicates(self) -> dict:
            return self.duplicates

    def get_hash_map(self) -> dict:
            return self.hash_map

#FIXME: Permitir PDF
class DuDe(Resource):
    def post(self, dir_name: str):
        file = request.files['file']
        if not os.path.exists(f'temp/{dir_name}'):
            os.makedirs(f'temp/{dir_name}')

        file.save(f'temp/{dir_name}/{file.filename}')
        return {"message": f"Archivo {file.filename} guardado exitosamente."}
    
    def get(self, dir_name: str):
        start_time = datetime.now()
        dude = DuDeBase(f'temp/{dir_name}')
        dude.find_duplicates()
            
        return  {
            "duplicates": dude.get_duplicates(),
            # "hash_map": dude.get_hash_map(),
            "time(s)": f"{(datetime.now() - start_time).total_seconds()}"
        }
    
    def delete(self, dir_name: str):
        if os.path.exists(f'temp/{dir_name}'):
            try:
                for file in os.listdir(f'temp/{dir_name}'):
                    os.remove(f'temp/{dir_name}/{file}')
                os.rmdir(f'temp/{dir_name}')
            except Exception as e:
                return {"message": f"Error al eliminar archivos: {e}"}

            return {"message": "Archivos eliminados exitosamente."}

        return {"message": "No se encontraron archivos para eliminar."}