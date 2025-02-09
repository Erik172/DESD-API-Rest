from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models import Result, ResultStatus
from app.schema import ResultSchema
from app import db

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id=None):
        result_schema = ResultSchema()
        
        if task_id:
            result = Result.query.filter_by(collection_id=task_id).first()
            if not result:
                abort(404, "Task ID not found")
                
            return result_schema.dump(result)
        else:
            results = Result.query.all()
            return result_schema.dump(results, many=True)
    
    @jwt_required()
    def delete(self, task_id):
        result = Result.query.filter_by(collection_id=task_id).first()
        if not result:
            abort(404, "Task ID not found")
            
        result_status = ResultStatus.query.filter_by(result_id=result.id).first()
        db.session.delete(result_status)
        db.session.delete(result)
        db.session.commit()
        
        return '', 204