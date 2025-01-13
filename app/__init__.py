from flask import Flask
from app.config import configurer_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from redis import Redis
from rq import Queue

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()
mongo = None
redis = None
queue = None

def create_app():
    from app.models import User
    
    app = Flask(__name__)
    configurer_app(app)
    CORS(app)
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    global redis, queue
    redis = Redis.from_url(app.config['RQ_REDIS_URL'])
    queue = Queue(connection=redis)
    
    @app.before_request
    def create_database():
        db.create_all()
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user.id)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = int(jwt_data['sub'])
        return User.query.filter_by(id=identity).one_or_none()

    api = Api(app)
    
    global mongo
    mongo_client = MongoClient(app.config['MONGO_URI'])
    mongo = mongo_client['desd']
    
    from app.routes import initialize_routes
    initialize_routes(api)
    
    return app