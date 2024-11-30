from app import db

class AiModel(db.Model):
    __tablename__ = 'ai_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False)
    version = db.Column(db.String(250), nullable=True, default='1.0')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __repr__(self):
        return f'<AiModel {self.name} - {self.version}>'