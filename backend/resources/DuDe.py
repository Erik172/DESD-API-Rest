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
        """
        Saves the uploaded file to the specified directory.

        Args:
            dir_name (str): The name of the directory to save the file in.

        Returns:
            dict: A dictionary containing a success message.

        Raises:
            None
        """
        file = request.files['file']
        if not os.path.exists(f'temp/{dir_name}'):
            os.makedirs(f'temp/{dir_name}')

        if file.filename.lower().endswith('.pdf'):
            file.save(f'temp/{dir_name}/{file.filename}')
            images = convert_from_path(f'temp/{dir_name}/{file.filename}')
            for i, image in enumerate(images):
                image.save(f'temp/{dir_name}/{file.filename}__pagina_{i}.png')
            os.remove(f'temp/{dir_name}/{file.filename}')

        elif file.filename.lower().endswith(('.tiff', '.tif')):
            tiff_image = Image.open(file)
            for i, page in enumerate(ImageSequence.Iterator(tiff_image)):
                jpg_file_path = f"temp/{dir_name}/{file.filename}__pagina_{i}.jpg"
                page.save(jpg_file_path, "JPEG")
        else:
            file.save(f'temp/{dir_name}/{file.filename}')

        return {"message": f"Archivo {file.filename} guardado exitosamente."}, 200
    
    def get(self, dir_name: str) -> dict:
        collection = self.db[dir_name]
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

            collection.insert_one(document)
        
        return {"duplicados": dude.get_duplicates(), "tiempo(s)": f"{(stop_time - start_time).total_seconds()}"}
    
    def delete(self, dir_name: str) -> dict:
        """
        Deletes a directory and its contents.

        Args:
            dir_name (str): The name of the directory to delete.

        Returns:
            dict: A dictionary containing a message indicating the result of the deletion.

        Raises:
            OSError: If an error occurs while deleting the directory.

        """
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
        """
        Extracts the page number from a filename.

        Args:
            filename (str): The filename from which to extract the page number.

        Returns:
            int: The extracted page number, or None if no match is found.
        """
        match = re.search(r'__pagina_(\d+)', filename)
        return int(match.group(1)) if match else None