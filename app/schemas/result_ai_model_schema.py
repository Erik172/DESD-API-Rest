from marshmallow import validates, ValidationError, fields
from app.models import ResultAiModel, Result, AiModel
from app import ma

class ResultAIModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResultAiModel
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
        if not AiModel.query.get(value):
            raise ValidationError('AI Model does not exist.')