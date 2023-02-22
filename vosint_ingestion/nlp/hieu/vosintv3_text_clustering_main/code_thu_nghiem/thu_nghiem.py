import pymongo

def connect():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["text_clustering"]
    mydb = mydb["class"]
    x = mydb.find({})
    for i in x:
        print(i["tu_khoa_bat_buoc"])

print(connect())