from flask_restful import Api
from app.resources import *

def initialize_routes(api: Api) -> None:
    api.add_resource(WorkerResource, '/api/v1/worker', endpoint='worker')
    api.add_resource(TaskResource, '/api/v1/task', '/api/v1/task/<string:task_id>', endpoint='task')