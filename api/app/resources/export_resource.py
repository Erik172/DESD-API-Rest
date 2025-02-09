from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import send_file, abort
from app.services import ExportService

class ExportResource(Resource):
    @jwt_required()
    def get(self, task_id: str):
        export_service = ExportService()
        filename = export_service.export_collection(task_id)
        
        if not filename:
            abort(404, "Task ID not found")
            
        return send_file(filename, as_attachment=True, mimetype='text/csv', download_name=filename)