from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.models import User
from app.schemas import UserSchema

class MeResource(Resource):
    @jwt_required()
    def get(self):
        """
        Obtiene la información del usuario autenticado.
        Requiere autenticación JWT.
        Returns:
            dict: Información del usuario autenticado en formato JSON.
        """
        user = User.query.get(current_user.id)
        user_schema = UserSchema(exclude=['password'])
        
        return user_schema.dump(user), 200
