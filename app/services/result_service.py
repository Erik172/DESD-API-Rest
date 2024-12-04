import csv
from app import mongo

class ResultService:
    def export_collection(self, collection_name: str) -> str:
        cursor = mongo[collection_name].find()
        if cursor.count() == 0:
            return None
        
        file_name = f"{collection_name}.csv"
        file_path = f"exports/{file_name}"
        
        with open(file_path, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cursor[0].keys())
            writer.writeheader()
            for document in cursor:
                writer.writerow(document)
                
        return file_name