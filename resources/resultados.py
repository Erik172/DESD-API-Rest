from flask import request, jsonify
from flask_restful import Resource
from database import get_database
from datetime import datetime

class Resultados(Resource):
    def __init__(self):
        self.db = get_database()

    def get(self, collection_name=None):
        if collection_name:
            results = list(self.db.get_collection(collection_name).find())
            for result in results:
                result['_id'] = str(result['_id'])
            return jsonify(results)
        else:
            collections = self.db.list_collection_names()
            return jsonify(collections)

    def post(self, collection_name):
        data = request.json
        data['created_at'] = datetime.now()
        self.db[collection_name].insert_one(data)
        return jsonify({"status": "ok"})

    def delete(self, collection_name, document_id=None):
        if document_id:
            self.db[collection_name].delete_one({"_id": document_id})
        else:
            self.db.drop_collection(collection_name)
            
        return jsonify({"status": "ok"})

