from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Status(db.Model):
    __tablename__ = "status"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result_id = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(100), nullable=True, default="in_progress")
    files_processed = db.Column(db.Integer, nullable=True, default=0)
    total_files = db.Column(db.Integer, nullable=True, default=0)
    percentage = db.Column(db.Integer, nullable=True, default=0)
    tilted = db.Column(db.Boolean, nullable=True, default=False)
    rotation = db.Column(db.Boolean, nullable=True, default=False)
    cut_information = db.Column(db.Boolean, nullable=True, default=False)
    duplicate = db.Column(db.Boolean, nullable=True, default=False)
    folio = db.Column(db.Boolean, nullable=True, default=False)
    summary = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True, default=db.func.now())
    last_updated = db.Column(db.DateTime, nullable=True, default=db.func.now(), onupdate=db.func.now())
    
    def __repr__(self):
        return f"<Status {self.result_id}>"