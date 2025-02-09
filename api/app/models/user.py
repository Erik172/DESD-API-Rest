from app import db, bcrypt
from datetime import datetime
from sqlalchemy import event
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
    
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password, 10).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
@event.listens_for(User, 'before_insert')
def receive_before_insert(mapper, connection, target):
    target.password = User.hash_password(target.password)
    
@event.listens_for(User, 'before_update')
def receive_before_update(mapper, connection, target):
    if target.password != User.query.get(target.id).password:
        target.password = User.hash_password(target.password)