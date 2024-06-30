from flask_restful import Resource
from flask import send_file
from database import get_database
from flask import jsonify
import os

class Export(Resource):
    def __init__(self):
        self.db = get_database()

    def get(self, resultado_id: str):
        file_name = self._all_documents_to_csv(resultado_id)
        if not file_name:
            return "No data found", 404
        
        route = f'exports/{file_name}'
        
        if os.path.exists(route):
            return send_file(route, as_attachment=True, mimetype='csv')
        else:
            return f"File not found", 404
    
    def delete(self, resultado_id: str):
        try:
            os.remove(f"exports/{resultado_id}.csv")
            return jsonify({"status": "ok"})
        except:
            return jsonify({"status": "pass"})
        
    def _all_documents_to_csv(self, collection_name: str) -> str:
        data = list(self.db[collection_name].find())
        if not data:
            return None
        keys = data[0].keys()
        file_name = f"{collection_name}.csv"  # Use collection_name as the file name
        file_path = f"exports/{file_name}"
        with open(file_path, "w") as f:
            f.write(",".join(keys) + "\n")
            for document in data:
                f.write(",".join([str(document[key]) for key in keys]) + "\n")

        return file_name
