from app import db

class ResultAiModel(db.Model):
    __tablename__ = 'result_ai_models'
    
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'), nullable=False)
    ai_model_id = db.Column(db.Integer, db.ForeignKey('ai_models.id'), nullable=False)
    
    __table_args__ = (
        db.PrimaryKeyConstraint('result_id', 'ai_model_id', name='result_ai_models_pk'),
    )
    
    def __repr__(self):
        return f'<ResultAiModel {self.result_id} - {self.ai_model_id}>'