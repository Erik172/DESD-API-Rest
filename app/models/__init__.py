from .status import Status

def mongo_db():
    from dotenv import load_dotenv
    import pymongo
    import os
    
    load_dotenv()
    
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    return client["DESD"]