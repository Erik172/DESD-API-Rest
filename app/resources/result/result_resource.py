from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from flask import request
from app.models import Result
from app.schemas import ResultSchema

class ResultResource(Resource):
    @jwt_required()
    def get(self, result_id: str = None):
        if result_id:
            result = Result.query.filter_by(result_id=result_id).first()
            if not result:
                return {'message': 'Result not found'}, 404
            
            if not current_user.is_admin and result.user_id != current_user.id:
                return {'message': 'Unauthorized'}, 401
            
            schema = ResultSchema()
            return schema.dump(result)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Result.query
        
        if request.args.get('user_id'):
            query = query.filter_by(user_id=request.args.get('user_id'))
            
        result_query = query.paginate(page=page, per_page=per_page, error_out=False)
        result = result_query.items
        
        schema = ResultSchema(many=True)
        
        return {
            'total': result_query.total,
            'page': result_query.page,
            'per_page': result_query.per_page,
            'results': schema.dump(result)
        }, 200
            
    