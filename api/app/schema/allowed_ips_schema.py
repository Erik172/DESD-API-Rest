from marshmallow import validates, ValidationError, fields
from app.models import AllowedIPs
from app import ma

class AllowedIPsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AllowedIPs
        load_instance = True
        include_fk = True
        ordered = True
        
    id = fields.Integer(dump_only=True)
    ip = fields.String(required=True)
    is_active = fields.Boolean(required=False, default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('ip')
    def validate_ip(self, value):
        if AllowedIPs.query.filter_by(ip=value).first():
            raise ValidationError('IP already exists.')