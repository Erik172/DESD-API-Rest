from marshmallow import validates, ValidationError, fields
from app.models import Result
from app import ma

class ResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Result
        load_instance = True
        include_fk = True
        ordered = True
        
    id = fields.Integer(dump_only=True)
    collection_id = fields.String(required=True)
    user_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    status = fields.Nested('ResultStatusSchema')
    
    @validates('user_id')
    def validate_user_id(self, value):
        from app.models import User
        user = User.query.get(value)
        if not user:
            raise ValidationError('User not found')