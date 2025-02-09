from flask import Flask
from app.config import configurer_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
mongo = None

def create_app():
    app = Flask(__name__)
    configurer_app(app)
    CORS(app)
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    # @app.before_first_request
    # def create_database():
    #     db.create_all()
    
    with app.app_context():
        db.create_all()
        
    api = Api(app)
    
    global mongo
    mongo_client = MongoClient(app.config['MONGO_URI'])
    mongo = mongo_client[app.config['MONGO_DB']]
    
    from app.routes import initialize_routes
    initialize_routes(api)
    
    return app