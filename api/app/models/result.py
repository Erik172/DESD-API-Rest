from app import db
import pytz
from datetime import datetime

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.String(250), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('America/Bogota')))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('America/Bogota')), onupdate=lambda: datetime.now(pytz.timezone('America/Bogota')))
    status = db.relationship('ResultStatus', backref='result', uselist=False)
    
    def __repr__(self):
        return f'<Result {self.id} - {self.collection_id}>'