from flask import request, jsonify, json
from flask_restful import Resource
from datetime import datetime
from db import Work
from database import get_database

class Works(Resource):
    db = get_database()

    def get(self):
        return jsonify(self.db.list_collection_names())
    
class WorkEndPoint(Resource):
    def get(self, work_id):
        work = Work(work_id)
        return json.loads(json.dumps(list(work.get_all()), default=str))
    
    def post(self, work_id):
        work = Work(work_id)
        data = request.json
        data['created_at'] = datetime.now()
        result = work.save(data)
        return jsonify({"_id": str(result)})
    
    def put(self, work_id, document_id):
        work = Work(work_id)
        data = request.json
        result = work.update(document_id, data)
        return jsonify({"updated_count": result})
    
    def delete(self, work_id, document_id):
        work = Work(work_id)
        result = work.delete(document_id)
        return jsonify({"deleted_count": result})