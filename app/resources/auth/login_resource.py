from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request
from app.models import User
from app import bcrypt

class LoginResource(Resource):
    def post(self):
        """
        Maneja la solicitud POST para el inicio de sesión de usuario.
        Obtiene los datos JSON de la solicitud, verifica las credenciales del usuario
        y genera un token de acceso si las credenciales son válidas.
        Returns:
            dict: Un diccionario con el token de acceso si las credenciales son válidas.
            tuple: Una tupla con un mensaje de error y el código de estado 401 si las credenciales no son válidas.
        """
        data = request.get_json()
        
        user = User.query.filter_by(email=data.get('email')).first()
        
        if not user or not bcrypt.check_password_hash(user.password, data.get('password')):
            return {'message': 'Invalid credentials'}, 401
        
        access_token = create_access_token(identity=user)
        
        return {'access_token': access_token}, 200