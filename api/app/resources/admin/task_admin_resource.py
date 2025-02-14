from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.models import Result, ResultStatus
from app.schema import ResultSchema
from app import db

class TaskAdminResource(Resource):
    def __init__(self):
        self.result_schema = ResultSchema()
        
    @jwt_required()
    def get(self, task_id=None):
        if not current_user.is_admin:
            abort(403, "Permission denied")
        
        if task_id:
            result = Result.query.filter_by(collection_id=task_id).first()
            if not result:
                abort(404, "Task ID not found")
            
            return self.result_schema.dump(result)
        else:
            results = Result.query.all()
            return self.result_schema.dump(results, many=True)
    
    @jwt_required()
    def delete(self, task_id):
        if not current_user.is_admin:
            abort(403, "Permission denied")
        
        result = Result.query.filter_by(collection_id=task_id).first()
        if not result:
            abort(404, "Task ID not found")
        
        result_status = ResultStatus.query.filter_by(result_id=result.id).first()
        db.session.delete(result_status)
        db.session.delete(result)
        db.session.commit()
        
        return '', 204