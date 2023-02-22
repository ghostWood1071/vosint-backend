import pandas as pd
from underthesea import word_tokenize
import re
from collections import Counter
from connect_mongodb import connect

class Create_vocab_corpus:
    '''Các tham số khởi tạo'''
    def __init__(self) :
        self.filename = "D:/Aiacademy/VOSINT3_document_clustering/thu_nghiem_bm25/stopwords/stopwords.txt"
        

    '''Hàm in thường'''
    @staticmethod    
    def lower_text(text):
        return text.lower()

    '''Hàm loại bỏ một số ký tự đặc biệt'''
    @staticmethod    
    def clean_text(text):
        text = re.sub('<.*?>', ' ', text).strip()
        text = re.sub('(\s)+', r'\1', text)
        text = re.sub(r'[^\w\s]',' ', text)
        return text

    '''Hàm loại bỏ từ dừng'''
    def remove_stopwords(self, text):
        text = text.split()
        f = open(self.filename, 'r', encoding="utf-8")  
        stopwords = f.readlines()
        stop_words = [s.replace("\n", '') for s in stopwords]
        #print("mid: ", stop_words)
        doc_words = []
        #### YOUR CODE HERE ####
        
        for word in text:
            if word not in stop_words:
                doc_words.append(word)

        #### END YOUR CODE #####
        doc_str = ' '.join(doc_words).strip()
        return doc_str
    
    '''Hàm loại bỏ khoảng trắng'''
    @staticmethod
    def remove_whitespace(text):
        return re.sub(r'\s+', ' ', text)

    '''Hàm loại bỏ số'''
    @staticmethod
    def remove_number(text):
        return re.sub("(\s\d+)", " ", text)

    def lst_document(self, class_name):
        self.document = []
        collection = connect()
        corsur = collection.find({"class_name" : class_name})
        van_ban_mau = []
        for x in corsur:
            van_ban_mau = x["van_ban_mau"]
        
        # df = pd.read_csv("data/{}.csv".format(class_name), encoding="utf-8")
        for i in van_ban_mau:
            i = self.lower_text(i)
            i = self.clean_text(i)
            i = self.remove_stopwords(i)
            i = self.remove_whitespace(i)
            i = self.remove_number(i)
            self.document.append(i)

    def create_vocab(self, class_name):
        self.vocab_chinh_tri_xa_hoi = []
        collection = connect()
        corsur = collection.find({"class_name" : class_name})
        van_ban_mau = []
        for x in corsur:
            van_ban_mau = x["van_ban_mau"]
        for i in van_ban_mau:
            i = self.lower_text(i)
            i = self.clean_text(i)
            i = self.remove_stopwords(i)
            i = self.remove_whitespace(i)
            i = self.remove_number(i)
            self.vocab_chinh_tri_xa_hoi.extend(word_tokenize(i)[:-1])
    
        counts = Counter(self.vocab_chinh_tri_xa_hoi)
        print(len(counts))
        self.result = []
        for i in counts.items():
            if i[1] >= 10:
                self.result.append(i[0])
        return self.result
        

# result = Create_vocab_corpus()
# print(result.create_vocab("Chinh_tri_Xa_hoi"))