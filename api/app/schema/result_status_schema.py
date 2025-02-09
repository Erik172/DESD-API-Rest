from marshmallow import validates, ValidationError, fields
from app.models import ResultStatus, ResultStatusEnum
from app import ma

class ResultStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResultStatus
        load_instance = True
        include_fk = True
        ordered = True
        
    id = fields.Integer(dump_only=True)
    result_id = fields.Integer(required=True)
    status = fields.Enum(ResultStatusEnum, required=True, default=ResultStatusEnum.UPLOADING)
    total_files = fields.Integer()
    total_files_processed = fields.Integer()
    models = fields.String()
    current_file = fields.String()
    last_updated = fields.DateTime(dump_only=True)
    
    @validates('result_id')
    def validate_result_id(self, value):
        from app.models import Result
        result = Result.query.get(value)
        if not result:
            raise ValidationError('Result not found')
        
    @validates('status')
    def validate_status(self, value):
        if value not in ResultStatusEnum:
            raise ValidationError('Invalid status')