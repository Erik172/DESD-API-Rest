from marshmallow import validates, ValidationError, fields
from app.models import Result, ResultStatus, User
from app import ma

class ResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Result
        load_instance = True
        include_fk = True
        ordered = True
        
    id = fields.Integer(dump_only=True)
    collection_id = fields.String(required=True)
    alias = fields.String()
    user_id = fields.Integer(required=True)
    user = fields.Method('get_user', dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    status = fields.Method('get_status', dump_only=True)
    
    def get_user(self, obj):
        from app.schemas import UserSchema
        user = User.query.get(obj.user_id)
        schema = UserSchema(only=('id', 'name', 'email'))
        return schema.dump(user)
    
    def get_status(self, obj):
        from app.schemas import ResultStatusSchema
        result_status = ResultStatus.query.filter_by(result_id=obj.id).first()
        schema = ResultStatusSchema()
        return schema.dump(result_status)
        
    @validates('user_id')
    def validate_user_id(self, value):
        from app.models import User
        if not User.query.get(value):
            raise ValidationError('User does not exist.')