from flask import request, jsonify, json
from flask_restful import Resource
from datetime import datetime
from db import Work
from database import get_database
import os

class Works(Resource):
    db = get_database()

    def get(self):
        return jsonify(self.db.list_collection_names())
    
    def delete(self, collection_name):
        self.db.drop_collection(collection_name)
        return jsonify({"status": "ok"})
    
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
    
class WorkExport(Resource):
    def get(self, work_id):
        work = Work(work_id)
        file_name = work.all_documents_to_csv()
        data = {
            "file_name": file_name,
            "work_id": work_id,
            "total": work.count(),
            "url": f"/descargar/{work_id}"
        }

        return jsonify(data)
    
    def delete(self, work_id):
        try:
            os.remove(f"exports/{work_id}.csv")
            return jsonify({"status": "ok"})
        except:
            return jsonify({"status": "pass"})