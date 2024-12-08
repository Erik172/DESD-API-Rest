from flask_restful import Api
from app.resources import *

def initialize_routes(api: Api) -> None:
    api.add_resource(LoginResource, '/api/v1/auth/login', endpoint='login')
    api.add_resource(MeResource, '/api/v1/auth/me', '/api/v1/users/me', endpoint='me')
    
    api.add_resource(UserResource, '/api/v1/users', '/api/v1/users/<int:user_id>', endpoint='users')
    
    api.add_resource(AIModelResource, '/api/v1/models', '/api/v1/models/<int:model_id>', endpoint='models')
    
    api.add_resource(DESDResource, '/api/v1/desd', endpoint='desd')
    
    api.add_resource(ResultResource, '/api/v1/results', '/api/v1/results/<string:result_id>', endpoint='results')
    api.add_resource(ExportResultResource, '/api/v1/results/<string:collection_name>/export', endpoint='export_result')
