from flask_restful import Api
from app.resources import *

def initialize_routes(api: Api) -> None:
    api.add_resource(LoginResource, '/api/v1/login', endpoint='login')