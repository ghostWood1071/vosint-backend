from pymongo import MongoClient

client = MongoClient("localhost", 27017)

mydatabase = client.text_clustering

mycollection = mydatabase.list_collection_names()

lst_class = []
for i in mycollection:
    collections = mydatabase[i]
    cursor = collections.find({})
    for document in cursor:
        class_ = document
        lst_class.append(class_)

# for k in range(len(lst_class)):
#     print("Tên các class :",lst_class[k]['class']['name'])
# print(list(lst_class[i]['class']['tu_khoa_loai_tru_1'].strip("").split(",")))

strings = "biển đông hôm nay rất nhiều nước trung quốc"


def check_tu_khoa_loai_tru(lst_tu_khoa_loai_tru, str):
    res = any(
        ele in str
        for ele in list(
            lst_tu_khoa_loai_tru["class"]["tu_khoa_loai_tru"].strip("").split(",")
        )
    )
    if res == True:
        return True
    elif res == False:
        return False


def check_tu_khoa_bat_buoc(lst_tu_khoa_bat_buoc, str):
    for j in range(1, len(lst_tu_khoa_bat_buoc["class"]) - 2 + 1):
        if (
            all(
                x in str
                for x in list(
                    lst_tu_khoa_bat_buoc["class"]["tu_khoa_bat_buoc_{}".format(j)]
                    .strip("")
                    .split(",")
                )
            )
            == False
        ):
            # print(list(lst_tu_khoa_bat_buoc['class']['tu_khoa_bat_buoc_{}'.format(j)].strip("").split(",")))
            return "Câu không thuộc chủ đề"
        else:
            # print(list(lst_tu_khoa_bat_buoc['class']['tu_khoa_bat_buoc_{}'.format(j)].strip("").split(",")))
            return "Câu thuộc chủ đề {}".format(lst_tu_khoa_bat_buoc["class"]["name"])


# for n in range(len(lst_class)):
#     if check_tu_khoa_loai_tru(lst_class[n], strings) == True:
#         print("Câu không thuộc chủ đề nào")
#     else:
#         result = check_tu_khoa_bat_buoc(lst_class[n], strings)
#    if result == False:
#         check_tu_khoa_loai_tru(lst_class[n],strings)

# check_tu_khoa_bat_buoc(lst_class[2],strings)

mycollection2 = mydatabase.bien_dong
for x in mycollection2.find({}, {"tu_khoa_bat_buoc"}):
    print(x)
