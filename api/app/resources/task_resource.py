from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Result, ResultStatus, ResultStatusEnum
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
                
            # if result.user_id != get_jwt_identity():
            #     abort(403, "Permission denied")
                
            return result_schema.dump(result)
        else:
            order_by = request.args.get('order_by', 'desc')
            order_type = request.args.get('order_type', 'created_at')
            status = request.args.get('status', None)
            
            query = Result.query.filter_by(user_id=get_jwt_identity())
            
            if status:
                if status in ResultStatusEnum.__members__:
                    query = query.join(ResultStatus, ResultStatus.result_id == Result.id).filter(ResultStatus.status == status)
                    
            if order_by == 'asc':
                query = query.order_by(getattr(Result, order_type).asc())
            else:
                query = query.order_by(getattr(Result, order_type).desc())
                
            results = query.all()
            total_results = len(results)
            
            return {
                "total_results": total_results,
                "results": result_schema.dump(results, many=True)
            }
    
    @jwt_required()
    def delete(self, task_id):
        result = Result.query.filter_by(collection_id=task_id).first()
        if not result:
            abort(404, "Task ID not found")
            
        if int(result.user_id) != int(get_jwt_identity()):
            abort(403, "Permission denied")
            
        result_status = ResultStatus.query.filter_by(result_id=result.id).first()
        db.session.delete(result_status)
        db.session.delete(result)
        db.session.commit()
        
        return '', 204
