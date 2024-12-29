from flask_restful import Resource
from flask import send_file
from app.services import ResultService
import os

class ExportResultResource(Resource):
    """
    Recurso para exportar resultados de una colección específica.
    Métodos:
    -------
    get(collection_name: str)
        Exporta los datos de la colección especificada y devuelve el archivo exportado.
    Parámetros:
    ----------
    collection_name : str
        El nombre de la colección a exportar.
    Respuestas:
    ----------
    200 OK:
        Devuelve el archivo exportado como una descarga adjunta.
    404 Not Found:
        Si no se encuentran datos en la colección especificada.
    """
    def get(self, collection_name: str):
        result_service = ResultService()
        filename = result_service.export_collection(collection_name)
        if not filename:
            return {"message": "No data found"}, 404
        
        if os.name == 'posix':
            file_path = f"../exports/{filename}"
        else:
            file_path = f"..\\exports\\{filename}"
            
        return send_file(file_path, as_attachment=True, mimetype='csv')