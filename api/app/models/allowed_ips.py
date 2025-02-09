from app import db

class AllowedIPs(db.Model):
    __tablename__ = 'allowed_ips'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(250), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<AllowedIPs {self.id} - {self.ip}>'