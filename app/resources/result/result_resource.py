from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from flask import request
from app import db, mongo
from app.models import Result, ResultStatus
from app.schemas import ResultSchema
import os

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
        order_by = request.args.get('order_by', 'created_at')
        order_type = request.args.get('order_type', 'desc')
        
        query = Result.query
        
        if request.args.get('user_id'):
            query = query.filter_by(user_id=request.args.get('user_id'))
            
        if order_type == 'desc':
            query = query.order_by(getattr(Result, order_by).desc())
        else:
            query = query.order_by(getattr(Result, order_by))
            
        result_query = query.paginate(page=page, per_page=per_page, error_out=False)
        result = result_query.items
        
        schema = ResultSchema(many=True)
        
        return {
            'total': result_query.total,
            'page': result_query.page,
            'pages': result_query.pages,
            'per_page': result_query.per_page,
            'results': schema.dump(result)
        }, 200
    
    @jwt_required()
    def delete(self, result_id: str):
        result = Result.query.filter_by(collection_id=result_id).first()
        result_status = ResultStatus.query.filter_by(result_id=result.id).first()
        if not result:
            return {'message': 'Result not found'}, 404
        
        if not current_user.is_admin and result.user_id != current_user.id:
            return {'message': 'Unauthorized'}, 401
        
        try:
            os.remove(f'exports/{result_id}.csv')
        except FileNotFoundError:
            pass
        
        db.session.delete(result)
        db.session.delete(result_status)
        db.session.commit()
        
        mongo[result_id].drop()
        
        return {'message': 'Result deleted'}, 200
            
    