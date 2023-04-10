from nlp.toan.v_osint_topic_sentiment_main.sentiment_analysis import topic_sentiment_classification
from models import MongoRepository
mongo = MongoRepository()
def update_sacthai(mode_rerun = True):
    if mode_rerun:
        a = mongo.get_many_d(
            collection_name="News",
            filter_spec={},
            filter_other={"_id": 1, "data:content": 1},
        )
    else:
        a = mongo.get_many_d(
            collection_name="News",
            filter_spec={"data:class_sacthai": []},
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
    
        
        # if str(class_text_clustering)!= '[]':
        #     print(class_text_clustering)
        _id = str(i["_id"])
        doc = {}
        doc["_id"] = _id

        # class_title = []
        # for class_id in class_text_clustering:
        #     class_title.append(mongo.get_one(collection_name="class_chude",filter_spec = {"class_name":class_id})['title'])
        kq = topic_sentiment_classification(content)
        #print(str(kq))
        if str(kq['sentiment_label']) == 'tieu_cuc':
            kq = '-1'
        elif str(kq['sentiment_label']) == 'trung_tinh':
            kq = '0'
        elif str(kq['sentiment_label']) == 'tich_cuc':
            kq = '1'
        else:
            kq = ''
        doc['data:class_sacthai'] = kq
        mongo.update_one('News', doc)
        
        #print(class_text_clustering)

    # query = {
    #         "$and": [
    #             #{"required_keyword": {"$exists": True}},
    #             #{"exclusion_keyword": {"$exists": True}},
    #             {"news_samples": {"$exists": True}},
    #             {"news_samples": {"$ne": None}},
    #             {"news_samples": {"$ne": []}}
    #                 ]
    #     }

    # new_letter, _ = mongo.get_many(
    #     "newsletter",
    #     query
    # )
    # _id = []
    # for i in new_letter:
    #     _id.append(str(i["_id"]))
    # for id_chude in _id:
    #     query = { "data:class_tinmau": { "$regex": ".*"+id_chude+".*" } }
    #     results = mongo.get_many_d('News',filter_spec=query,filter_other={"_id":1})

    #     new_id = []
    #     for i in results[0]:
    #         new_id.append(i['_id'])
    #     mongo.update_one(collection_name='newsletter',doc={"_id":id_chude,"news_id":new_id})
        
    return True

update_sacthai()