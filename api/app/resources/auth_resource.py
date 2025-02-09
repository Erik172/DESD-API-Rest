from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request, abort
from app.models import User

class AuthResource(Resource):
    def post(self):
        if 'username' not in request.json or 'password' not in request.json:
            abort(400, "Username or password not provided")
        
        username = request.json['username']
        password = request.json['password']
        
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            abort(401, "Invalid credentials")
        
        access_token = create_access_token(identity=user)
        return {'access_token': access_token}, 200