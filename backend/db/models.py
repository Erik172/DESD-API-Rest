from database import get_database

db = get_database()

class Work:
    def __init__(self, work_id: str = None):
        self.work_id = work_id
        self.collection = db[work_id]

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
    

