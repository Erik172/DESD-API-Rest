from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

from app.src import download_customOCR
from app.config import configurer_app

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    configurer_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.status import Status
    
    @app.before_request
    def create_tables():
        db.create_all()
        
    if not os.path.exists("models/customTrOCR/"):
        download_customOCR()
        
    api = Api(app)
    
    from app.resources import (
        Resultados,
        Export,
        Status,
        DuDe,
        Desd,
        Folio
    )
    
    api.add_resource(Resultados, "/v1/resultados", "/v1/resultados/<string:collection_name>")
    api.add_resource(Export, "/v2/export/<string:resultado_id>")
    api.add_resource(Status, "/v2/status", "/v2/status/<string:result_id>")
    api.add_resource(DuDe, "/v2/dude")
    api.add_resource(Desd, "/v2/desd")
    api.add_resource(Folio, "/v1/folio")
    
    @app.route("/v2/generate_id")
    def generate_id():
        from src import generate_id
        return {"random_id": generate_id()}, 200
    
    return app