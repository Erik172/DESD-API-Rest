from database import get_database

db = get_database()

class Resultados:
    def __init__(self, resultado_id: str = None):
        self.resultado_id = resultado_id
        self.collection = db[resultado_id]

    def save(self, data: dict):
        result = self.collection.insert_one(data)
        return result.inserted_id
    
    def update(self, data: dict, document_id: str):
        actual_data = self.collection.find_one({"_id": document_id})
        actual_data = {k: v for k, v in actual_data.items() if v is not None}
        actual_data.pop("_id")
        result = self.collection.update_one(
            {"_id": document_id},
            {"$set": {**actual_data, **data}}
        )

        return result.modified_count
    
    def delete(self, document_id: str):
        result = self.collection.delete_one({"_id": document_id})
        return result.deleted_count
    
    def get_all(self):
        return self.collection.find({})
    
    def all_documents_to_csv(self):
        data = self.get_all()
        data = list(data)
        if not data:
            return None
        keys = data[0].keys()
        with open(f"exports/{self.resultado_id}.csv", "w") as f:
            f.write(",".join(keys) + "\n")
            for document in data:
                f.write(",".join([str(document[key]) for key in keys]) + "\n")
                
        return f"{self.resultado_id}.csv"
    
    def count(self):
        return self.collection.count_documents({})
    

