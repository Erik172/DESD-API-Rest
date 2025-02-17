import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db, bcrypt
from app.models import User, AllowedIPs

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    users = [
        User(username='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'), is_admin=True),
    ]
    
    db.session.add_all(users)
    db.session.commit()
        
    print('Admin user created successfully')
    
    ips = [
        AllowedIPs(ip='127.0.0.1'),
        AllowedIPs(ip='172.19.0.1'),
        AllowedIPs(ip='172.18.0.1')
    ]
    
    db.session.add_all(ips)
    db.session.commit()
        
    print('Allowed IP created successfully')
    
    db.session.close()
    sys.exit(0)