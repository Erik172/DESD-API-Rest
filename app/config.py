from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

def configurer_app(app) -> None:
    app.config['DEBUG'] = os.getenv('DEBUG', False)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=5)
    
    # MongoDB
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    
    # Redis
    app.config['RQ_REDIS_URL'] = os.getenv('RQ_REDIS_URL', 'redis://localhost:6379/0')
    app.config['RQ_QUEUES'] = ['default']