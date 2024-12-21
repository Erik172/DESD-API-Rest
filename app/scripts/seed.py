from dotenv import load_dotenv
import sys
import os

from app import create_app, db, bcrypt
from app.models import User

load_dotenv()

database_url = os.getenv('SQLALCHEMY_DATABASE_URI')

if not database_url:
    print('No database url found in .env file')
    sys.exit(1)
    
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        users = [
            User(
                name='Admin',
                email=os.getenv('ADMIN_EMAIL'),
                password=bcrypt.generate_password_hash(os.getenv('ADMIN_PASSWORD')).decode('utf-8'),
                is_admin=True
            ),
        ]
        
        db.session.add_all(users)
        db.session.commit()
        
        print('Database seeded successfully')
        
        db.session.close()
        sys.exit(0)