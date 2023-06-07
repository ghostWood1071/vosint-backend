from db.init_db import get_collection_client

client = get_collection_client("new_vn")

def insert_into_mongodb(data):
    client.insert_many(data)
