from flask_restful import Resource
from flask import send_file
from app.services import ResultService

class ExportResultResource(Resource):
    def get(self, collection_name: str):
        result_service = ResultService()
        filename = result_service.export_result(collection_name)
        if not filename:
            return {"message": "No data found"}, 404
        
        file_path = f"exports/{filename}"
        return send_file(file_path, as_attachment=True, mimetype='csv')