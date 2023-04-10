
import pymongo
client = pymongo.MongoClient("mongodb://vosint:vosint_2022@192.168.1.100:27017/?authMechanism=DEFAULT")
db = client["vosint_db"]

# Get a reference to the collection you want to drop
collection = db["cls_clustering"]

# Drop the collection
collection.drop()