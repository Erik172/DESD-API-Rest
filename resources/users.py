from database import sql_db, User
from flask_restful import Resource
from flask import request

class Users(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        name = data.get('name')

        if not username or not password or not email or not name:
            return {"message": "Missing required fields"}, 400
        
        user = User.query.filter_by(username=username).first()
        if user:
            return {"message": "Username already exists"}, 400
        
        user = User(username=username, password=password, email=email, name=name)
        sql_db.session.add(user)
        sql_db.session.commit()

        return {"message": "User created successfully"}, 201
    
    def get(self):
        username = request.args.get('username')
        password = request.args.get('password')

        if not username or not password:
            return {"message": "Missing required fields"}, 400
        
        user = User.query.filter_by(username=username, password=password).first()

        if not user:
            return {"message": "Invalid credentials"}, 401
        
        return {"message": "Login successful", "role": user.role}, 200