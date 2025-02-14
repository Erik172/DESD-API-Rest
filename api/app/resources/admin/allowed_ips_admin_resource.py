from flask import request, abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user
from app.models import AllowedIPs
from app.schema import AllowedIPsSchema
from app import db

class AllowedIPsAdminResource(Resource):
    def __init__(self):
        self.allowed_ips_schema = AllowedIPsSchema()
        
    @jwt_required()
    def get(self, allowed_ip_id=None):
        if not current_user.is_admin:
            abort(403, "Permission denied")
            
        if allowed_ip_id:
            allowed_ip = AllowedIPs.query.get(allowed_ip_id)
            if not allowed_ip:
                abort(404, "Allowed IP not found")
                
            return self.allowed_ips_schema.dump(allowed_ip)
        
        allowed_ips = AllowedIPs.query.all()
        
        return self.allowed_ips_schema.dump(allowed_ips, many=True)
    
    @jwt_required()
    def post(self):
        if not current_user.is_admin:
            abort(403, "Permission denied")
        
        allowed_ip = self.allowed_ips_schema.load(request.json)
        
        db.session.add(allowed_ip)
        db.session.commit()
        
        return self.allowed_ips_schema.dump(allowed_ip), 201
    
    @jwt_required()
    def put(self, allowed_ip_id):
        if not current_user.is_admin:
            abort(403, "Permission denied")
        
        allowed_ip = AllowedIPs.query.get(allowed_ip_id)
        if not allowed_ip:
            abort(404, "Allowed IP not found")
        
        allowed_ip = self.allowed_ips_schema.load(request.json, instance=allowed_ip, partial=True)
        
        db.session.commit()
        
        return self.allowed_ips_schema.dump(allowed_ip)
    
    @jwt_required()
    def delete(self, allowed_ip_id):
        if not current_user.is_admin:
            abort(403, "Permission denied")
        
        allowed_ip = AllowedIPs.query.get(allowed_ip_id)
        if not allowed_ip:
            abort(404, "Allowed IP not found")
        
        db.session.delete(allowed_ip)
        db.session.commit()
        
        return '', 204