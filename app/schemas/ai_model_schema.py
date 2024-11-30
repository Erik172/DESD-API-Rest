from marshmallow import validates, ValidationError, fields
from models.ai_model import AIModel
from app import ma

class AIModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AIModel
        load_instance = True
        include_fk = True
        ordered = True
        
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    version = fields.String(required=False, default='1.0')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('version')
    def validate_version(self, value):
        if AIModel.query.filter_by(name=self.name, version=value).first():
            raise ValidationError('Model version already exists.')

    @validates('name')
    def validate_name(self, value):
        if AIModel.query.filter_by(name=value).first():
            raise ValidationError('Model name already exists.')
        