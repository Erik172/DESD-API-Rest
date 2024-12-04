from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from app.models import AiModel
from app.schemas import AIModelSchema
from app import db

class AIModelResource(Resource):
    def get(self, model_id: int = None):
        """
        Obtiene uno o todos los modelos de IA.
        Args:
            model_id (int, opcional): El ID del modelo de IA a obtener. 
                                      Si no se proporciona, se obtendrán todos los modelos.
        Returns:
            dict: Un diccionario con los datos del modelo de IA si se encuentra.
            tuple: Una tupla con una lista de todos los modelos de IA y un código de estado 200.
            tuple: Una tupla con un mensaje de error y un código de estado 404 si el modelo no se encuentra.
        """
        if model_id:
            ai_model = AiModel.query.get(model_id)
            if not ai_model:
                return {'message': 'Model not found'}, 404
            
            return AIModelSchema().dump(ai_model)
        
        ai_models = AiModel.query.all()
        return AIModelSchema(many=True).dump(ai_models), 200

    @jwt_required()
    def post(self):
        """
        Maneja la solicitud POST para crear un nuevo modelo de IA.
        Utiliza el esquema AIModelSchema para validar y cargar los datos del modelo de IA
        desde el cuerpo de la solicitud JSON. Si la validación falla, devuelve un mensaje
        de error con el código de estado 400. Si la validación es exitosa, agrega el modelo
        de IA a la sesión de la base de datos y lo guarda.
        Retorna:
            tuple: Una tupla que contiene el modelo de IA serializado y el código de estado 201.
        """
        ai_model_schema = AIModelSchema()
        try:
            ai_model = ai_model_schema.load(request.json)
        except ValidationError as e:
            return e.messages, 400
        
        db.session.add(ai_model)
        db.session.commit()
        
        return ai_model_schema.dump(ai_model), 201