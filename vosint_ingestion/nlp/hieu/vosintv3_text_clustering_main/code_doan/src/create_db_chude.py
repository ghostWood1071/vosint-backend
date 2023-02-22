#class_name string
#tu_khoa_loai_tru string
#tu_khoa_bat_buoc array {string}

from models import MongoRepository
def create_db_chude():
    mongo = MongoRepository()
    #{"$and": [{"a": 1}, {"$or": [{"b": 2}, {"c": 3}]}]}

    new_letter,_ = mongo.get_many('newsletter',{"$and": [{'tag':"chu_de"},{"$and":[{"required_keyword": {"$exists": True}},{"exclusion_keyword": {"$exists": True}}]}]})
    _id = []
    class_name = []
    tu_khoa_loai_tru = []
    tu_khoa_bat_buoc = []
    for i in new_letter:
        _id.append(str(i["_id"]))
        class_name.append(i['title'])
        tu_khoa_loai_tru.append(i['exclusion_keyword'])
        tu_khoa_bat_buoc.append(i['required_keyword'])
    for i in range(len(class_name)):
        doc ={}
        doc['class_name'] = _id[i]
        doc['tu_khoa_loai_tru'] = tu_khoa_loai_tru[i]
        doc['tu_khoa_bat_buoc'] = tu_khoa_bat_buoc[i]
        doc['title'] = class_name[i]
        mongo.insert_one('class_chude',doc)
    return True



