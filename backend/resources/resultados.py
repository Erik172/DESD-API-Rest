from flask import request, jsonify
from flask_restful import Resource
from database import get_database
from datetime import datetime

class Resultados(Resource):
    db = get_database()

    def get(self, collection_name: str = None):
        """
        Retrieves data from the specified collection or returns a list of collection names if no collection is specified.

        Args:
            collection_name (str, optional): The name of the collection to retrieve data from. Defaults to None.

        Returns:
            Flask Response: A JSON response containing the retrieved data or a list of collection names.
        """
        if collection_name:
            return jsonify(list(self.db[collection_name].find()))
        return jsonify(self.db.list_collection_names())
    
    def post(self, collection_name: str):
        """
        Inserts a document into the specified collection in the database.

        Args:
            collection_name (str): The name of the collection to insert the document into.

        Returns:
            dict: A JSON response indicating the status of the insertion operation.
        """
        data = request.json
        data['created_at'] = datetime.now()
        self.db[collection_name].insert_one(data)
        return jsonify({"status": "ok"})
    
    #FIXME: Implement the put method.
    def put(self, collection_name: str, document_id: str):
        """
        Updates a document in the specified collection in the database.

        Args:
            collection_name (str): The name of the collection to update the document in.
            document_id (str): The ID of the document to update.

        Returns:
            dict: A JSON response indicating the status of the update operation.
        """
        data = request.json
        self.db[collection_name].update_one({"_id": document_id}, {"$set": data})
        return jsonify({"status": "ok"})
    
    def delete(self, collection_name: str, document_id: str = None):
            """
            Deletes a document from a collection in the database.

            Args:
                collection_name (str): The name of the collection to delete from.
                document_id (str, optional): The ID of the document to delete. If not provided, the entire collection will be dropped.

            Returns:
                dict: A JSON response indicating the status of the deletion operation.
            """
            if document_id:
                self.db[collection_name].delete_one({"_id": document_id})
            else:
                self.db.drop_collection(collection_name)
                
            return jsonify({"status": "ok"})
