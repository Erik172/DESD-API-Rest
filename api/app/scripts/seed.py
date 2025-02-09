import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(name='Admin', username='admin', password=bcrypt.generate_password_hash('admin', 10).decode('utf-8'), is_admin=True)
        db.session.add(admin)
        db.session.commit()
        
    print('Admin user created successfully')
    
    db.session.close()
    db.engine.dispose()
    sys.exit(0)