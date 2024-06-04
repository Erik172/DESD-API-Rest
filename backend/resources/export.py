from flask_restful import Resource
from database import get_database
from flask import jsonify
import os

class Export(Resource):
    db = get_database()

    def get(self, resultado_id: str):
            """
            Retrieves the export data for a given `resultado_id`.

            Args:
                resultado_id (str): The ID of the result.

            Returns:
                dict: A dictionary containing the export data, including the file name, resultado_id, total count, and download URL.
            """
            file_name = self._all_documents_to_csv(resultado_id)
            data = {
                "file_name": file_name,
                "resultado_id": resultado_id,
                "total": self.db[resultado_id].count_documents({}),
                "url": f"/descargar/{resultado_id}"
            }

            return jsonify(data)
    
    def delete(self, resultado_id: str):
        """
        Deletes the exported CSV file with the given resultado_id.

        Args:
            resultado_id (str): The ID of the resultado to be deleted.

        Returns:
            dict: A JSON response indicating the status of the deletion operation.
                If the file is successfully deleted, the response will have a "status" key with the value "ok".
                If an error occurs during the deletion, the response will have a "status" key with the value "pass".
        """
        try:
            os.remove(f"exports/{resultado_id}.csv")
            return jsonify({"status": "ok"})
        except:
            return jsonify({"status": "pass"})
        
    def _all_documents_to_csv(self, collection_name: str) -> str:
        """
        Export all documents from a collection to a CSV file.

        Args:
            collection_name (str): The name of the collection to export.

        Returns:
            str: The name of the exported CSV file.

        Raises:
            None

        """
        data = list(self.db[collection_name].find())
        if not data:
            return None
        keys = data[0].keys()
        file_name = f"{collection_name}.csv"  # Use collection_name as the file name
        file_path = os.path.join("exports", file_name)  # Use os.path.join for file path
        with open(file_path, "w") as f:
            f.write(",".join(keys) + "\n")
            for document in data:
                f.write(",".join([str(document[key]) for key in keys]) + "\n")

        return file_name
