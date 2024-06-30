from pdf2image import convert_from_path
from PIL import Image, ImageSequence
from flask_restful import Resource
from database import get_database
from services import DuDeBase
from datetime import datetime
from flask import request
import re
import os
    
class DuDe(Resource):
    db = get_database()

    def post(self, dir_name: str) -> dict:
        file = request.files['file']
        if not os.path.exists(f'temp/{dir_name}'):
            os.makedirs(f'temp/{dir_name}')

        if file.filename.lower().endswith('.pdf'):
            file.save(f'temp/{dir_name}/{file.filename}')
            images = convert_from_path(f'temp/{dir_name}/{file.filename}')
            for i, image in enumerate(images):
                image.save(f'temp/{dir_name}/{file.filename}__pagina_{i + 1}.png')
            os.remove(f'temp/{dir_name}/{file.filename}')

        elif file.filename.lower().endswith(('.tiff', '.tif')):
            tiff_image = Image.open(file)
            for i, page in enumerate(ImageSequence.Iterator(tiff_image)):
                jpg_file_path = f"temp/{dir_name}/{file.filename}__pagina_{i + 1}.jpg"
                page.save(jpg_file_path, "JPEG")
        else:
            file.save(f'temp/{dir_name}/{file.filename}')

        return {"message": f"Archivo {file.filename} guardado exitosamente."}, 200
    
    def get(self, dir_name: str) -> dict:
        start_time = datetime.now()
        dude = DuDeBase(f'temp/{dir_name}')
        dude.find_duplicates()
        stop_time = datetime.now()

        for key, value in dude.get_duplicates().items():
            num_of_duplicates = len(value)
            page_number = self._extract_page_number(key)
            if page_number is not None:
                filename = key.replace(f'__pagina_{page_number}.png', '').replace(f'__pagina_{page_number}.jpg', '')
            else:
                filename = key

            document = {
                "archivo": filename,
                "duplicados": num_of_duplicates
            }

            if page_number is not None:
                document["pagina"] = page_number
            else:
                document["pagina"] = None

            for i, duplicate in enumerate(value):
                pege_number = self._extract_page_number(duplicate)
                if page_number is not None:
                    filename = duplicate.replace(f'__pagina_{pege_number}.png', '').replace(f'__pagina_{pege_number}.jpg', '')
                    document[f"duplicado[{i + 1}]"] = filename
                    document[f"duplicado[{i + 1}]_pagina"] = pege_number
                else:
                    document[f"duplicado[{i + 1}]"] = duplicate

            try:
                collection = self.db[dir_name]
                collection.insert_one(document)
            except Exception as e:
                print(f"Error al insertar en la base de datos: {e}")
        
        return {"duplicados": dude.get_duplicates(), "tiempo(s)": f"{(stop_time - start_time).total_seconds()}"}
    
    def delete(self, dir_name: str) -> dict:
        if os.path.exists(f'temp/{dir_name}'):
            try:
                for file in os.listdir(f'temp/{dir_name}'):
                    os.remove(f'temp/{dir_name}/{file}')
                os.rmdir(f'temp/{dir_name}')
            except Exception as e:
                return {"message": f"Error al eliminar archivos: {e}"}, 500

            return {"message": "Archivos eliminados exitosamente."}, 200

        return {"message": "No se encontraron archivos para eliminar."}, 404

    def _extract_page_number(self, filename: str) -> int:
        match = re.search(r'__pagina_(\d+)', filename)
        return int(match.group(1)) if match else None