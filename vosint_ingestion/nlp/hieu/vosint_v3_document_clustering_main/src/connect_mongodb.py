import pymongo

def connect():
    myclient = pymongo.MongoClient("mongodb://vosint:vosint_2022@192.168.1.100:27017/?authMechanism=DEFAULT")
    return myclient
    # mydb = myclient["document_clustering"]
    # my_col = mydb["cls_clustering"]