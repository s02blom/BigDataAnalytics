import pymongo
from pymongo import MongoClient
from os import environ

def get_connection() -> pymongo.synchronous.database.Database:
    """Established a connection with the Mongo and connects to the database"""
    try:
        client = MongoClient(environ.get("DATABASE_HOST"), int(environ.get("DATABASE_PORT")))
        db = client[environ.get("DATABASE_NAME")]
        db.client.close()
    except Exception as err:
        print(err)
    return db
    
def close_connection(db: pymongo.synchronous.database.Database):
    """Closes the connection with the database"""
    db.client.close()