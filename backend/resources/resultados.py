from flask import request, jsonify, send_file
from flask_restful import Resource
from werkzeug.utils import secure_filename
from datetime import datetime
from db import Resultados
from database import get_database
import os

class Resultados(Resource):
    db = get_database()

    def get(self):
        return jsonify(self.db.list_collection_names())
    
    def delete(self, collection_name):
        self.db.drop_collection(collection_name)
        return jsonify({"status": "ok"})