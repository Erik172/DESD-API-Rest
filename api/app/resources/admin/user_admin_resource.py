from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.models import User
from app.schema import UserSchema
from app import db

class UserAdminResource(Resource):
    @jwt_required()
    def get(self, user_id=None):        
        if not current_user.is_admin:
            abort(403, "Permission denied")
            
        user_schema = UserSchema()
        
        if user_id:
            user = User.query.get(user_id)
            if not user:
                abort(404, "User not found")
                
            return user_schema.dump(user)
        else:
            users = User.query.all()
            return user_schema.dump(users, many=True)
        
    @jwt_required()
    def post(self):
        if not current_user.is_admin:
            abort(403, "Permission denied")
        
        user_schema = UserSchema()
        user = user_schema.load(request.json)
        user.password = User.generate_hash(user.password)
        
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201
    
    @jwt_required()
    def delete(self, user_id):
        if not current_user.is_admin:
            abort(403, "Permission denied")
        
        user = User.query.get(user_id)
        if not user:
            abort(404, "User not found")
        
        db.session.delete(user)
        db.session.commit()
        
        return '', 204