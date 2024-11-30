from flask import Flask
from app.config import configurer_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mongo = PyMongo()

def create_app() -> Flask:
    from app.models import User
    
    app = Flask(__name__)
    configurer_app(app)
    CORS(app)
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mongo.init_app(app)
    
    @app.before_request
    def create_database():
        db.create_all()
        
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(id=identity).one_or_none()
    
    api = Api(app)
    
    from app.routes import initialize_routes
    initialize_routes(api)
    
    return app
    