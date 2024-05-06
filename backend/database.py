import pymongo

def get_database():
    """
    Returns the MongoDB database object for the DESD application.

    Returns:
        pymongo.database.Database: The MongoDB database object.
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client["DESD"]