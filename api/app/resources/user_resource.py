from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask import request, abort
from marshmallow import ValidationError
from app.models import User
from app.schema import UserSchema
from app import db

class UserResource(Resource):
    def post(self):
        user_schema = UserSchema()
        
        try:
            user = user_schema.load(request.json)
        except ValidationError as e:
            abort(400, str(e))
            
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, "User not found")
            
        user_schema = UserSchema()
        return user_schema.dump(user)
    
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, "User not found")
            
        user_schema = UserSchema()
        try:
            user = user_schema.load(request.json, instance=user, partial=True)
        except ValidationError as e:
            abort(400, str(e))
            
        db.session.commit()
        return user_schema.dump(user)
    
    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, "User not found")
            
        db.session.delete(user)
        db.session.commit()
        
        return '', 204