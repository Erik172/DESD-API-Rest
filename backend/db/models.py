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
        result = self.collection.update_one({"_id": document_id}, {"$set": data})
        return result.modified_count
    
    def delete(self, document_id: str):
        result = self.collection.delete_one({"_id": document_id})
        return result.deleted_count
    
    def get_all(self):
        return self.collection.find()
    
    def get_by_id(self, document_id: str):
        return self.collection.find_one({"_id": document_id})
    
    def get_by_archivo(self, archivo: str):
        return self.collection.find({"archivo": archivo})
    
    def get_by_prediccion(self, prediccion: str):
        return self.collection.find({"prediccion": prediccion})
    
    def get_by_query(self, query: dict):
        return self.collection.find(query)
    
    def get_by_query_limit(self, query: dict, limit: int):
        return self.collection.find(query).limit(limit)
