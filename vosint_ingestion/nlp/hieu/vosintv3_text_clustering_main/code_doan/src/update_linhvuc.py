from models import MongoRepository

#from ...src.main import text_clustering
from ....vosintv3_text_clustering_main_15_3.src.inference import text_clustering

mongo = MongoRepository()


def update_linhvuc(mode_rerun = True):
    if mode_rerun:
        a = mongo.get_many_d(
            collection_name="News",
            filter_spec={},
            filter_other={"_id": 1, "data:content": 1},
        )
    else:
        a = mongo.get_many_d(
            collection_name="News",
            filter_spec={"data:class_linhvuc": []},
            filter_other={"_id": 1, "data:content": 1},
        )

    for i in a[0]:
        content = ""
        try:
            content = i["data:content"]
        except:
            pass
        if content == "":
            continue
        class_text_clustering = text_clustering(content, class_name="class_linhvuc")
        _id = str(i["_id"])
        doc = {}
        doc["_id"] = _id

        # class_title = []
        # for class_id in class_text_clustering:
        #     class_title.append(mongo.get_one(collection_name="class_chude",filter_spec = {"class_name":class_id})['title'])
            
        doc['data:class_linhvuc'] = class_text_clustering
        mongo.update_one('News', doc)
        
        #print(class_text_clustering)

    new_letter, _ = mongo.get_many(
        "newsletter",
        {
            "$and": [
                {"tag": "linh_vuc"},
                {
                    "$and": [
                        {"required_keyword": {"$exists": True}},
                        {"exclusion_keyword": {"$exists": True}},
                    ]
                },
            ]
        },
    )
    _id = []
    for i in new_letter:
        _id.append(str(i["_id"]))
    for id_linhvuc in _id:
        query = { "data:class_linhvuc": { "$regex": ".*"+id_linhvuc+".*" } }
        results = mongo.get_many_d('News',filter_spec=query,filter_other={"_id":1})

        new_id = []
        for i in results[0]:
            new_id.append(i['_id'])
        mongo.update_one(collection_name='newsletter',doc={"_id":id_linhvuc,"news_id":new_id})
        
    return True


def test():
    a = text_clustering("Trên đông,nước,trung quốc,bóng đá,cá độ,thể thao",class_name="class_chude")
    print(a)
