from models import MongoRepository

from ...src.main import text_clustering

mongo = MongoRepository()


def update_chude():
    a = mongo.get_many_d(
        collection_name="News",
        filter_spec={"data:class_chude": []},
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
        class_text_clustering = text_clustering(content, class_name="class_chude")
        _id = str(i["_id"])
        doc = {}
        doc["_id"] = _id

        # class_title = []
        # for class_id in class_text_clustering:
        #     class_title.append(mongo.get_one(collection_name="class_chude",filter_spec = {"class_name":class_id})['title'])
            
        doc['data:class_chude'] = class_text_clustering
        mongo.update_one('News', doc)
        #print(class_text_clustering)
        
    return True


def test():
    a = text_clustering("Trên đông,nước,trung quốc,bóng đá,cá độ,thể thao",class_name="class_chude")
    print(a)
