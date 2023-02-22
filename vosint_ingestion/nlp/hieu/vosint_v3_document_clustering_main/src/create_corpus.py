from underthesea import word_tokenize
from connect_mongodb import connect

class Create_corpus:
    '''Hàm tạo tập dữ liệu'''
    def Create_corpus_final(self):
        self.corpus_tst = []
        '''Kết nối tới cơ sở dữ liệu mongo'''
        # mongo = Connect_to_mongo()
        # mongo.connect()
        cursor = connect().find({})

        for i in cursor:
            self.corpus_tst.extend(i["van_ban_mau"])
        self.tokenized_corpus = [word_tokenize(doc) for doc in self.corpus_tst]

