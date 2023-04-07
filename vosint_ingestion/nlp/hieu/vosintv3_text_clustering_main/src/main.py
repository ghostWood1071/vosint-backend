import re

import pymongo


class Text_Clustering:
    """
    khởi tạo kết nối tới mongodb
    """

    def __init__(self, class_name="class_chude"):
        self.myclient = pymongo.MongoClient(
            "mongodb://vosint:vosint_2022@192.168.1.100:27017/?authMechanism=DEFAULT"
        )
        self.mydb = self.myclient["vosint_db"]
        self.mydb = self.mydb[class_name]

    """
    check nếu từ khóa loại trừ xuất hiện trong câu => trả về True
    nếu từ khóa loại trừ không xuất hiện trong câu => trả về False
    """

    @staticmethod
    def check_tu_khoa_loai_tru(lst_class,str):
        if lst_class["tu_khoa_loai_tru"] is None:
            return False
        elif lst_class["tu_khoa_loai_tru"] == "":
            return False
        else:
            tu_khoa_loai_tru = list(lst_class['tu_khoa_loai_tru'].split(","))
            True_or_False = []
            for i in tu_khoa_loai_tru:
                pattern = r'\b{}\b'.format(re.escape(i))
                True_or_False.append(bool(re.search(pattern, str)))   
            res = any(True_or_False)
            return res

    '''
    check nếu tất cả từ khóa bắt buộc xuất hiện trong câu => trả về True
    nếu không => trả về False
    '''
    @staticmethod
    def check_tu_khoa_bat_buoc(lst_class,str):
        if lst_class["tu_khoa_bat_buoc"] is None:
            return False
        elif lst_class["tu_khoa_bat_buoc"] == "":
            return False
        else:
            if isinstance(lst_class["tu_khoa_bat_buoc"],list) == True:
                for i in lst_class["tu_khoa_bat_buoc"]:
                    if i == "" or i is None:
                        continue
                    True_or_False = []
                    tu_khoa_bat_buoc = list(i.split(","))
                    #print(tu_khoa_bat_buoc)
                    for k in tu_khoa_bat_buoc:
                        pattern = r'\b{}\b'.format(re.escape(k))
                        True_or_False.append(bool(re.search(pattern, str)))      
                    if all(True_or_False) == False:
                        continue
                    elif all(True_or_False) == True:
                        return True
            else:
                tu_khoa_bat_buoc = list(lst_class['tu_khoa_bat_buoc'].split(","))
                True_or_False = []
                for i in tu_khoa_bat_buoc:
                    if i == "" or i is None:
                        continue
                    pattern = r'\b{}\b'.format(re.escape(i))
                    True_or_False.append(bool(re.search(pattern, str)))   
                res = all(True_or_False)
                return res
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




def text_clustering(sentence: str, class_name):
    cluster = Text_Clustering(class_name)
    sentence = sentence.lower()
    sentence = re.sub(r"\s+", " ", sentence).strip()
    return cluster.clustering(sentence)
