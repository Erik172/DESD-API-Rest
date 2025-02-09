from app import db
from datetime import datetime
import pytz

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True, index=True)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    results = db.relationship('Result', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('America/Bogota')))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone('America/Bogota')), onupdate=lambda: datetime.now(pytz.timezone('America/Bogota')))

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'