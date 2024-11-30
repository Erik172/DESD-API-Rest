from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity, current_user
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from app.models import User
from app.schemas import UserSchema
from app import db, bcrypt

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id: int = None) -> tuple:
        """
        Obtiene la información de un usuario específico o de todos los usuarios.
        Requiere autenticación JWT.
        Args:
            user_id (int, opcional): ID del usuario a obtener. Si no se proporciona, se obtienen todos los usuarios.
        Returns:
            tuple: Un diccionario con la información del usuario o usuarios y un código de estado HTTP.
                - Si se proporciona `user_id`:
                    - 200: Información del usuario en formato JSON.
                    - 403: Si el usuario actual no es administrador y `user_id` no coincide con el ID del usuario actual.
                    - 404: Si el usuario con `user_id` no se encuentra.
                - Si no se proporciona `user_id`:
                    - 200: Información de todos los usuarios en formato JSON.
                    - 403: Si el usuario actual no es administrador.
        """
        if user_id:
            if not current_user.is_admin and user_id != current_user.id:
                return {'message': 'Admin access required'}, 403
            
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            
            user_schema = UserSchema(exclude=['password'])
            return user_schema.dump(user), 200
        
        if not current_user.is_admin:
            return {'message': 'Admin access required'}, 403
        
        users = User.query.all()
        user_schema = UserSchema(many=True, exclude=['password'])
        return user_schema.dump(users), 200
        
    @jwt_required()
    def post(self):
        """
        Crea un nuevo usuario en la base de datos.
        Retorna un mensaje de error si el usuario actual no es administrador.
        Valida los datos del usuario proporcionados en el cuerpo de la solicitud.
        Si hay errores de validación, retorna un mensaje de error con los detalles.
        Encripta la contraseña del usuario antes de guardarlo en la base de datos.
        Guarda el nuevo usuario en la base de datos y retorna los datos del usuario creado.
        Returns:
            dict: Mensaje de error si el usuario actual no es administrador o si hay errores de validación.
            tuple: Datos del usuario creado y el código de estado HTTP 201 si la operación es exitosa.
        """
        if not current_user.is_admin:
            return {'message': 'Admin access required'}, 403
        
        user_schema = UserSchema()
        
        try:
            user = user_schema.load(request.json)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, 400
        
        user.password = bcrypt.generate_password_hash(user.password, 10).decode('utf-8')
        
        db.session.add(user)
        db.session.commit()
        
        return user_schema.dump(user), 201
    
    @jwt_required()
    def put(self, user_id: int) -> tuple:
        if not current_user.is_admin and user_id != current_user.id:
            return {'message': 'Admin access required'}, 403
        
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        user_schema = UserSchema()
        
        try:
            user = user_schema.load(request.json, instance=user, partial=True)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, 400
        
        db.session.commit()
        
        return user_schema.dump(user), 200