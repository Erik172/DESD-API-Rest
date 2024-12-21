from marshmallow import validates, ValidationError, fields
from app.models import ResultStatus, ResultStatusEnum, Result
from app import ma

class ResultStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResultStatus
        include_fk = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    result_id = fields.Integer(required=True)
    status = fields.Enum(ResultStatusEnum, required=True, default=ResultStatusEnum.PENDING)
    total_files = fields.Integer()
    total_files_processed = fields.Integer()
    models = fields.String()
    current_file = fields.String()
    last_updated_at = fields.DateTime(dump_only=True)
    
    @validates('status')
    def validate_status(self, value):
        if value not in ResultStatusEnum.__members__:
            raise ValidationError(f"Invalid status: {value}")
        
    @validates('result_id')
    def validate_result_id(self, value):
        result = Result.query.get(value)
        if not result:
            raise ValidationError(f"Result {value} not found")