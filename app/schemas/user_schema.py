from marshmallow import validates, ValidationError, fields
from app.models import User
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
    results = fields.Nested('ResultSchema', many=True, exclude=['user'])
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
