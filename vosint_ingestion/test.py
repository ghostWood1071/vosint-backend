
# import pymongo
# client = pymongo.MongoClient("mongodb://vosint:vosint_2022@192.168.1.100:27017/?authMechanism=DEFAULT")
# db = client["vosint_db"]

# # Get a reference to the collection you want to drop
# collection = db["cls_clustering"]

# # Drop the collection
# collection.drop()


from nlp.keyword_extraction.keywords_ext import Keywords_Ext
print(Keywords_Ext().extracting(document= "ngày ấy trong tôi bừng nắng hạ mặt trời chân lý trói qua tim",num_keywords =6))
from nlp.toan.v_osint_topic_sentiment_main.sentiment_analysis import topic_sentiment_classification
print(topic_sentiment_classification("ngày ấy trong tôi bừng nắng hạ mặt trời chân lý trói qua tim"))
from nlp.hieu.vosintv3_text_clustering_main_15_3.src.inference import text_clustering
print(text_clustering("Từ ấy", class_name="class_linhvuc"))