from flask import request, jsonify
from flask_restful import Resource
from database import get_database
from datetime import datetime

class Resultados(Resource):
    db = get_database()

    def get(self, collection_name: str = None):
            """
            Retrieves the documents from a specified collection or returns a list of available collections.

            Args:
                collection_name (str, optional): The name of the collection to retrieve documents from. Defaults to None.

            Returns:
                Flask Response: A JSON response containing the retrieved documents or a list of available collections.
            """
            if collection_name:
                results = list(self.db[collection_name].find())
                for result in results:
                    result['_id'] = str(result['_id'])
                return jsonify(results)
            else:
                collections = self.db.list_collection_names()
                return jsonify(collections)
    
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
