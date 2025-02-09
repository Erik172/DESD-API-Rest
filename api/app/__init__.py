from flask import Flask, request, abort
from app.config import configurer_app
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient
from app.utils import is_ip_allowed

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()
mongo = None

def create_app():
    from app.models import User
    
    app = Flask(__name__)
    configurer_app(app)
    CORS(app)
    
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    @app.before_request
    def check_ip():
        client_ip = request.remote_addr  # Obtener la IP del cliente
        if 'X-Forwarded-For' in request.headers:
            # Si hay un proxy, usar la primera IP en la lista
            client_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()

        if not is_ip_allowed(client_ip):
            abort(403, description="Acceso denegado: IP no permitida.")
        
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
    mongo = mongo_client[app.config['MONGO_DB']]
    
    from app.routes import initialize_routes
    initialize_routes(api)
    
    return app