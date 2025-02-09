from app import db
import datetime
import enum
import pytz
from sqlalchemy import event

class ResultStatusEnum(enum.Enum):
    UPLOADING = 'UPLOADING'
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    
class ResultStatus(db.Model):
    __tablename__ = 'result_status'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)
    status = db.Column(db.Enum(ResultStatusEnum), nullable=False, default=ResultStatusEnum.UPLOADING)
    total_files = db.Column(db.Integer, nullable=True)
    total_files_processed = db.Column(db.Integer, nullable=True, default=0)
    models = db.Column(db.String(250), nullable=True)
    current_file = db.Column(db.String(250), nullable=True)
    last_updated = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now(pytz.timezone('America/Bogota')))
    
    def __repr__(self):
        return f'<ResultStatus {self.id} - {self.status}>'

@event.listens_for(ResultStatus, 'before_update')
def receive_before_update(mapper, connection, target):
    target.last_updated = datetime.datetime.now(pytz.timezone('America/Bogota'))