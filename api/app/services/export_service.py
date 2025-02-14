import csv
import os
import tempfile
from app import mongo

class ExportService:
    def export_collection(self, collection_name: str) -> str:
        collection = mongo[collection_name]
        if collection.count_documents({}) == 0:
            return None
        
        tmpdir = tempfile.mkdtemp()
        filename = f"{collection_name}.csv"
        filepath = os.path.join(tmpdir, filename)
        
        cursor = collection.find()
        
        with open(filepath, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cursor[0].keys())
            writer.writeheader()
            for document in cursor:
                writer.writerow(document)
                
        return filepath