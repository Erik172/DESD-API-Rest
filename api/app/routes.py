from flask_restful import Api
from app.resources import *

def initialize_routes(api: Api) -> None:
    api.add_resource(WorkerResource, '/api/v1/worker', endpoint='worker')
    api.add_resource(TaskResource, '/api/v1/task', '/api/v1/task/<string:task_id>', endpoint='task')
    api.add_resource(UserResource, '/api/v1/user', endpoint='user')
    api.add_resource(AuthResource, '/api/v1/auth', endpoint='auth')
    api.add_resource(ExportResource, '/api/v1/export/<string:task_id>', endpoint='export')
    
    # Admin resources
    api.add_resource(UserAdminResource, '/api/v1/admin/user', '/api/v1/admin/user/<int:user_id>', endpoint='admin_user')
    api.add_resource(AllowedIPsAdminResource, '/api/v1/admin/allowed_ips', '/api/v1/admin/allowed_ips/<int:allowed_ip_id>', endpoint='admin_allowed_ips')
    api.add_resource(TaskAdminResource, '/api/v1/admin/task', '/api/v1/admin/task/<string:task_id>', endpoint='admin_task')