from underthesea import word_tokenize

from .connect_mongodb import connect


class Create_corpus:
    '''Hàm tạo tập dữ liệu'''
    def Create_corpus_final(self):
        #Tập các tất cả các tin tức
        self.corpus_tst = []
        '''Kết nối tới cơ sở dữ liệu mongo'''
        # mongo = Connect_to_mongo()
        # mongo.connect()
        cursor = connect()["vosint_db"]["cls_clustering"].find({})
        
        for i in cursor:
            self.corpus_tst.extend(i["van_ban_mau"])
        #Tập tất cả các từ trong mongodb
        self.tokenized_corpus = [word_tokenize(doc) for doc in self.corpus_tst]
        connect().close()
# start = time.time()
# result = Create_corpus().Create_corpus_final()
# print("Time :", time.time()-start)