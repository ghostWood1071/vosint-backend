# class_name string
# tu_khoa_loai_tru string
# tu_khoa_bat_buoc array {string}
import pymongo
from models import MongoRepository


def create_db_linhvuc():
    mongo = MongoRepository()
    # {"$and": [{"a": 1}, {"$or": [{"b": 2}, {"c": 3}]}]}

    try:
        client = pymongo.MongoClient("mongodb://vosint:vosint_2022@192.168.1.100:27017/?authMechanism=DEFAULT")
        db = client["vosint_db"]

        # Get a reference to the collection you want to drop
        collection = db["class_linhvuc"]

        # Drop the collection
        collection.drop()
    except:
        pass

    new_letter, _ = mongo.get_many(
        "newsletter",
        {
            "$and": [
                {"tag": "linh_vuc"},
                {
                    "$and": [
                        #{"required_keyword": {"$exists": True}},
                        #{"exclusion_keyword": {"$exists": True}},
                        {"required_keyword": {"$ne": None}},
                        {"exclusion_keyword": {"$ne": None}},
                    ]
                },
            ]
        },
    )
    _id = []
    class_name = []
    tu_khoa_loai_tru = []
    tu_khoa_bat_buoc = []
    for i in new_letter:
        _id.append(str(i["_id"]))
        class_name.append(i["title"])
        tu_khoa_loai_tru.append(i["exclusion_keyword"])
        tu_khoa_bat_buoc.append(i["required_keyword"])
    for i in range(len(class_name)):
        doc = {}
        doc["class_name"] = _id[i]
        doc["tu_khoa_loai_tru"] = tu_khoa_loai_tru[i]
        doc["tu_khoa_bat_buoc"] = tu_khoa_bat_buoc[i]
        doc["title"] = class_name[i]
        mongo.insert_one("class_linhvuc", doc)
    return True
