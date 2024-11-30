from marshmallow import validates, ValidationError, fields
from app.models import ResultAIModels, Result, AIModel
from app import ma

class ResultAiModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResultAIModels
        load_instance = True
        include_fk = True
        ordered = True
        
    result_id = fields.Integer(required=True)
    ai_model_id = fields.Integer(required=True)
    
    @validates('result_id')
    def validate_result_id(self, value):
        if not Result.query.get(value):
            raise ValidationError('Result does not exist.')
    
    @validates('ai_model_id')
    def validate_ai_model_id(self, value):
        if not AIModel.query.get(value):
            raise ValidationError('AI Model does not exist.')