from app import db
import enum

class ResultStatusEnum(enum.Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

class ResultStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'), nullable=False)
    status = db.Column(db.Enum(ResultStatusEnum), nullable=False, default=ResultStatusEnum.PENDING)
    total_files = db.Column(db.Integer, nullable=True)
    total_files_processed = db.Column(db.Integer, nullable=True)
    current_file = db.Column(db.String(250), nullable=True)
    last_updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __repr__(self):
        return f'<ResultStatus {self.id} - {self.status}>'