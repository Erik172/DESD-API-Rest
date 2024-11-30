from app import db

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __repr__(self):
        return f'<Result {self.id}>'