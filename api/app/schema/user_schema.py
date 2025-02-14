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
    username = fields.String(required=True)
    password = fields.String(required=True)
    is_admin = fields.Boolean(required=False, default=False)
    is_active = fields.Boolean(required=False, default=True)
    results = fields.Nested('ResultSchema', many=True, exclude=('user_id',))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('username')
    def validate_username(self, value):
        if User.query.filter_by(username=value).first():
            raise ValidationError('Username already exists.')
        
    @validates('is_admin')
    def validate_is_admin(self, value):
        if not self.context.get('is_admin'):
            raise ValidationError('Permission denied.')