import csv
import os
from app import mongo

class ResultService:
    def export_collection(self, collection_name: str) -> str:
        """
        Exporta una colección de MongoDB a un archivo CSV.
        Args:
            collection_name (str): El nombre de la colección a exportar.
        Returns:
            str: El nombre del archivo CSV exportado, o None si la colección está vacía.
        """
        collection = mongo[collection_name]
        if collection.count_documents({}) == 0:
            return None
        
        cursor = collection.find()
        file_name = f"{collection_name}.csv"
        file_path = os.path.join('exports', file_name)
        
        # Crear la carpeta 'exports' si no existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cursor[0].keys())
            writer.writeheader()
            for document in cursor:
                writer.writerow(document)
                
        return file_name