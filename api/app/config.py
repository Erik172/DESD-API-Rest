from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

def configurer_app(app) -> None:
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'my_precious')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://user:password@postgres:5432/desd')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://root:example@mongodb:27017')
    app.config['MONGO_DB'] = os.getenv('MONGO_DB', 'results')