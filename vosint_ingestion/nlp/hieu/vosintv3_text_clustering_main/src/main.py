import re 
import pymongo

class Text_Clustering:
    '''
    khởi tạo kết nối tới mongodb
    '''
    def __init__(self,class_name = "class_chude") :
        self.myclient = pymongo.MongoClient("mongodb://vosint:vosint_2022@192.168.1.100:27017/?authMechanism=DEFAULT")
        self.mydb = self.myclient["vosint_db"]
        self.mydb = self.mydb[class_name]
    '''
    check nếu từ khóa loại trừ xuất hiện trong câu => trả về True
    nếu từ khóa loại trừ không xuất hiện trong câu => trả về False
    '''
    @staticmethod
    def check_tu_khoa_loai_tru(lst_class,str):
        tu_khoa_loai_tru = list(lst_class['tu_khoa_loai_tru'].strip("").split(","))
        res = any(ele in str for ele in tu_khoa_loai_tru)
        return res

    '''
    check nếu tất cả từ khóa bắt buộc xuất hiện trong câu => trả về True
    nếu không => trả về False
    '''
    @staticmethod
    def check_tu_khoa_bat_buoc(lst_class,str):
        for i in lst_class["tu_khoa_bat_buoc"]:
            if (all(x in str for x in list(i.strip("").split(","))) == False):
                continue
            elif (all(x in str for x in list(i.strip("").split(","))) == True):
                return True
    '''
    phân cụm văn bản
    nếu không từ khóa loại trừ nào xuất hiện trong câu và trong câu chứa tất cả các từ khóa bắt buộc => câu thuộc cụm
    nếu không => câu không thuộc cụm
    '''
    def clustering(self,str):
        x = self.mydb.find({})

        class_ = []

        for i in x:
            if self.check_tu_khoa_loai_tru(i,str) == False and self.check_tu_khoa_bat_buoc(i,str) == True:
                class_.append(i['class_name'])

        self.myclient.close()

        return class_

def text_clustering(sentence : str,class_name):
    cluster = Text_Clustering(class_name)
    sentence = sentence.lower()
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return(cluster.clustering(sentence))

