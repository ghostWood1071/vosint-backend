# -*- coding: utf-8 -*-
import time
from .inference import Inference
from underthesea import word_tokenize
from .connect_mongodb import connect
import numpy as np
from .preprocess import lower_text, clean_text, remove_stopwords, remove_number


result = Inference()

'''Hàm tính toán'''
def BM25(query : str):
    '''tiền xử lý văn bản'''
    query = lower_text(query)
    query = clean_text(query)
    query = remove_stopwords(query)
    query = remove_number(query)
    result_final_bm25 = result.calculate_bm25(query)
    # result_lst = []
    # for i in range(len(result_final_bm25)):
    #     result_lst.append(result_final_bm25[i][-1:])
    query_lst = word_tokenize(query)
    class_ = np.empty([0])

    '''tìm cả các class đã truy vấn được'''
    for i in result_final_bm25:
        x = connect()["vosint_db"]["cls_clustering"].find_one({"van_ban_mau": i})
        class_ = np.append(class_,x["class_name"])
    class_ = np.unique(class_)

    '''
    + so sánh độ trùng khớp n-grams của văn bản input và các chủ đề (so sánh bằng cách tính số lần xuất hiện của các từ trong câu input với - score
      bộ vocab. Nếu score lớn hơn hoặc bằng với nửa độ dài của câu input, câu input sẽ thuộc lớp)
    + tham số cần thay đổi : 0.5 (độ tương đồng)
    '''
    class_or_not = []
    total_apperance = 0
    for j in class_:
        y = connect()["vosint_db"]["cls_clustering"].find_one({"class_name" : j})
        total_apperance = 0
        for k in query_lst:
            if k in y["vocab"]:
                total_apperance += 1
        if (total_apperance >= int(len(query_lst)*0.6)):
           class_or_not.append(y["class_name"])
    connect().close()
    return class_or_not

# start = time.time()
# print(BM25("VN có đường sắt đô thị sớm nhất vào năm 2011 (NLĐ) - Tại hội thảo “Đường sắt đô thị” tổ chức ngày 27-3 tại Hà Nội, Cục trưởng Cục Đường sắt VN Vũ Xuân Hồng cho biết nếu đúng tiến độ, VN sẽ có tuyến đường sắt đô thị đầu tiên vào năm 2011. Đó là tuyến đường sắt Bến Thành – Chợ Nhỏ – Suối Tiên được xây dựng tại TPHCM với tổng kinh phí khoảng 700 triệu USD. Chủ trương xây dựng đường sắt đô thị tại VN được hình thành từ năm 1999 với sự giúp đỡ kỹ thuật của Chính phủ Nhật Bản. Theo kinh nghiệm phát triển đường sắt đô thị của nước này (tuyến đường sắt Tsukuba có chiều dài 58,3km được xây dựng trong 7 năm với tổng kinh phí 830 tỉ yen), để xây dựng và vận hành đường sắt đô thị, nhất thiết phải có sự tham gia giải phóng mặt bằng của chính quyền địa phương và sự trợ giúp vốn đầu tư từ phía Chính phủ.   "
# " Xả nước hồ Hòa Bình để chống hạn Hôm nay 18-1, Tổng công ty Điện lực Việt Nam bắt đầu xả nước hồ Hòa Bình và Thác Bà nhằm nâng mực nước trên sông Hồng tại Hà Nội đạt trên 2,2 m. Lưu lượng xả tối đa 1.000 m3/s (trong đó Thác Bà chỉ 100 m3/s). Sáng nay, mực nước trên sông Hồng tại trạm đo Hà Nội đã nhích lên 1,75 m, tăng 9 cm so với hôm qua, và dự kiến đến 5h ngày mai sẽ đạt 2,2 m. Lúc đó các cống ven sông mới có thể lấy nước vào nội đồng.  Việc xả nước hồ thủy điện Hòa Bình và Thác Bà vào thời điểm này đồng nghĩa với tăng mức phát điện, chứ không phải mở cửa xả. Ông Nguyễn Danh Sơn, Phó giám đốc Trung tâm điều độ lưới điện quốc gia, cho biết, việc duy trì lưu lượng xả như thế nào còn phụ thuộc vào nguồn nước từ sông Thao, sông Lô và nhu cầu dùng điện. Dự kiến, trung bình tháng 1, tổng lưu lượng nước dành cho phát điện của hồ Hòa Bình và Thác Bà là 723 m3/s, gấp 1,3 lần lưu lượng nước về.  Tuy nhiên, một cán bộ của Trung tâm dự báo khí tượng thủy văn trung ương cho biết, nếu lưu lượng xả không ổn định, lúc cao lúc thấp thì không thể nâng mực nước sông Hồng. Các công ty thủy lợi không thể lấy nước gieo sạ. Đồng bằng sông Hồng và trung du Bắc Bộ sẽ gieo cấy 644.000 ha lúa đông xuân, trong đó có gần 400.000 ha cần bơm điện lấy nước."))
# print("Time :", time.time()-start)