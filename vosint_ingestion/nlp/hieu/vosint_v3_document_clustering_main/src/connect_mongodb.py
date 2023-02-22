import pymongo

def connect():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["document_clustering"]
    return mydb["cls_clustering"]