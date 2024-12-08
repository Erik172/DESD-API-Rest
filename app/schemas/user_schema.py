from marshmallow import validates, ValidationError, fields
from app.models import User, Result
from app import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        ordered = True
        
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.Email(required=True, unique=True)
    password = fields.String(required=True)
    is_admin = fields.Boolean(required=False, default=False)
    results = fields.Method('get_results', dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('email')
    def validate_email(self, value):
        if '@' not in value:
            raise ValidationError('Invalid email address.')
        elif User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists.')
        
    @validates('is_admin')
    def validate_is_admin(self, value):
        if value and not self.context.get('user').is_admin:
            raise ValidationError('Only admins can create admin users.')
        
    def get_results(self, obj):
        from app.schemas import ResultSchema
        results = Result.query.filter_by(user_id=obj.id).all()
        schema = ResultSchema(many=True)
        return schema.dump(results)
