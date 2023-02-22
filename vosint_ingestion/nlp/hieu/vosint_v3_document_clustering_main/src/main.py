# -*- coding: utf-8 -*-
from rank_bm25 import BM25Okapi
from underthesea import word_tokenize
from create_corpus import Create_corpus
import re
from connect_mongodb import connect

class Inference:
    def __init__(self):
        '''
        Các tham số mặc định
        '''
        # self.corpus_tst = []
        self.filename = "D:/Aiacademy/VOSINT3_document_clustering/thu_nghiem_bm25/stopwords/stopwords.txt"
        self.create_corpus = Create_corpus()
        self.create_corpus.Create_corpus_final()
        self.top_n = 10

    '''Hàm in thường'''
    @staticmethod
    def lower_text(text):
        return text.lower()

    '''Hàm loại một số ký tự đặc biệt'''
    @staticmethod    
    def clean_text(text):
        text = re.sub('<.*?>', ' ', text).strip()
        text = re.sub('(\s)+', r'\1', text)
        text = re.sub(r'[^\w\s]',' ', text)
        return text
    
    '''Hàm loại bỏ khoảng trắng'''
    @staticmethod
    def remove_whitespace(text):
        return re.sub(r'\s+', ' ', text)

    '''Hàm loại bỏ số'''
    @staticmethod
    def remove_number(text):
        return re.sub("(\s\d+)", " ", text)    

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

    '''Hàm tính toán bm25'''
    def calculate_bm25(self, query):
        bm25 = BM25Okapi(self.create_corpus.tokenized_corpus)
        #query = "Khoảng cách tình yêu Trong một thời khắc của tình yêu, rất nhiều anh chàng đã nói với người yêu rằng ""Anh muốn được xa em!"". Và khi cô gái nghe được câu nói trên, chắc chắn tình yêu của 2 bạn đang ở giai đoạn rất mong manh. ""Cứ mỗi tháng một lần, bạn trai tôi muốn đi thật xa một chuyến vài ngày để chụp ảnh. Khi thì Lào Cai, Yên Bái, có lần vào tít tận Vĩnh Long, Kiên Giang. Từ khi yêu tôi, những địa điểm anh chọn thường gần hơn, có thể cho cả tôi đi theo. Nhưng sau một năm, anh đặt vấn đề thẳng thắn với tôi: ""Anh đã mất đi cảm giác thích đi xa, điều đó làm chết luôn cả đam mê trong anh. Anh sợ điều đó. Vậy em có thể để anh xa em trong thời gian một tuần mỗi tháng, để anh trở về với thói quen đó được không?"", Nga kể về anh bạn cũ như thế và kết luận: ""Đó là bi kịch của tôi, anh ấy rất tuyệt vời, trừ việc anh ta là một gã S-men (những anh chàng mê khoảng cách)"". Cãi nhau? Không. Bạn là một cô gái nhàm chán? Cũng không. Bạn luôn ""bám dính"" anh ta trong mọi lúc mọi nơi? Không hẳn. Nhưng anh ta vẫn muốn xa bạn. Vì khi mọi thứ quanh anh ta quá suôn sẻ, quá tròn trịa, đầy đủ, anh ta tự dưng thích cựa mình vài cái để cảm thấy mình đang thiếu cái gì đó. ""Ngày trước, anh ấy thích đến nhà một ông bạn thân ở cả tháng trời, dù cứ sau thời gian đó, trông anh như một ""dị nhân"" vì đầu tóc, quần áo và ăn uống hầu như không theo một chuẩn mực thông thường nào cả. Từ khi chúng tôi yêu nhau, hình như anh ít đến đó hơn, vì anh dành thời gian ở bên tôi, tôi cũng nhắc anh quan tâm nhiều hơn đến quần áo, ăn uống. Mọi thứ cứ thế trong 1 năm. Rồi sau đó, đột nhiên anh luôn căng thẳng, bực tức vô cớ. Anh bảo anh chẳng làm được gì cả. Anh mất tự do quá. Anh không đổ lỗi cho tôi, nhưng bảo tôi làm anh hình thành một thói quen xấu: không còn thích thú với lối sống tự do nữa. Nó làm cho anh như mất hết chân tay! Tôi nghe mà bàng hoàng cả người, vì thực ra tôi không hề giữ chân anh, anh tự muốn gần tôi đấy chứ. Vô lý thật..."", Hoài tâm sự. Cô gái nào cũng sửng sốt khi người yêu đột ngột có những ý nghĩ kiểu: ""Anh thấy mình không còn là mình nữa, anh muốn đi tu!"" hoặc ""Em để anh một mình trong một thời gian ngắn được không, anh cần phải suy nghĩ một số việc..."" hay ""Em phải cho anh làm những việc anh thích chứ"". Bạn sẽ hoang mang khi nghe anh ấy đề nghị ""ly thân""? Liệu có cần thiết phải giận điên lên và cảm thấy tự ái vì nghĩ rằng anh ấy không cần bạn? Có nhiều cô gái còn đùng đùng đòi chia tay chỉ vì không thể chịu được sự...xúc phạm. Mai, 22 tuổi, nói: ""Mình chưa gặp kiểu đòi hỏi đó bao giờ, nhưng nếu là mình, mình sẽ chọn kiểu ""lạt mềm buộc chặt"" như trong quảng cáo bột nêm Knorr, có cô gái nấu món ăn thơm ngon đến độ chồng bỏ luôn cả trận bóng đá để ở nhà ăn bữa cơm của vợ. Mình nghĩ rằng những phút giây anh ấy mất tự do và thèm được ở một mình chỉ chiếm một phần mười mấy của quãng thời gian ở bên người phụ nữ thôi. Cho nên chẳng việc gì phải tức giận vì quyết định đó cả"". Hà, 24 tuổi, kể lại: ""Tôi đã tức điên lên khi nghe anh ấy nói muốn đi du lịch một mình chẳng có lý do gì cả. Tôi không gặp mặt anh ấy 2 ngày sau đó. Nhưng rồi tôi nghĩ lại: đã lâu lắm rồi anh ấy không có thời gian thư giãn. Chúng tôi làm cùng cơ quan nên mọi chuyện giữa 2 đứa đều xoay quanh công việc. Dù chia sẻ được nhiều nhưng anh ấy nhiều khi rất căng thẳng. Thế là tôi gọi điện làm hòa và hỏi xem anh ấy chuẩn bị chuyến đi đến đâu rồi. Nhưng cuối cùng anh ấy đổi ý, rủ tôi đi cùng"". Nguyệt, 20 tuổi, tâm sự: ""Tôi đã chấp nhận xa anh ấy trong vòng 1 tháng. Anh muốn đi 1 tour xuyên Việt cùng vài người bạn chưa biết mặt qua Internet. Tôi lo anh đi xa có an toàn không, rồi trong nhóm bạn của anh sẽ có cả những cô gái đẹp hơn tôi, năng động, đam mê du lịch và khám phá... Nhưng tôi vẫn không gọi điện đúng như ""giao ước"" với anh. Ngày thứ 8 của chuyến đi, anh gọi cho tôi và nói: ""Anh đi vui lắm, em giữ sức khỏe nhé. Rồi đến ngày thứ 15, anh đã đứng trước cửa nhà tôi. Anh ôm chặt tôi và nói: ""Bạn bè anh đã về cả rồi. Họ không thể bỏ công việc quá lâu, và anh không thể bỏ em thêm một ngày nào nữa"". Tôi thực sự hạnh phúc và hiểu rằng: Đôi khi khoảng cách cũng là một phương thuốc hâm nóng và làm mới thêm tình yêu của chúng tôi."
        tokenized_query = word_tokenize(query)
        # doc_scores = bm25.get_scores(tokenized_query)
        relevant_doc = bm25.get_top_n(tokenized_query, self.create_corpus.corpus_tst, n=self.top_n)
        return relevant_doc

result = Inference()

'''Hàm tính toán'''
def BM25(query : str):
    query = result.lower_text(query)
    query = result.clean_text(query)
    query = result.remove_stopwords(query)
    query = result.remove_whitespace(query)
    query = result.remove_number(query)

    result_final_bm25 = result.calculate_bm25(query)
    # result_lst = []
    # for i in range(len(result_final_bm25)):
    #     result_lst.append(result_final_bm25[i][-1:])
    query_lst = word_tokenize(query)
    class_ = []

    for i in result_final_bm25:
        x = connect().find_one({"van_ban_mau": i})
        class_.append(x["class_name"])
    
    class_or_not = []
    class_ = list(dict.fromkeys(class_))
    score = 0
    for j in class_:
        y = connect().find_one({"class_name" : j})
        score = 0
        for k in query_lst:
            if k in y["vocab"]:
                score += 1
        if score >= int(len(y["vocab"])*0.2):
           class_or_not.append(y["class_name"])
    return class_or_not

# model = load_model()

# @app.post("/BM25_with_embedding")
# def BM25_with_embedding(query : str):
#     start = time.time()
#     query = result.lower_text(query)
#     query = result.clean_text(query)
#     query = result.remove_stopwords(query)
#     query = result.remove_whitespace(query)
#     query = result.remove_number(query)
#     result_final_bm25 = result.calculate_bm25_with_embedding(query)
#     candidate_lst = []
#     for k in result_final_bm25:
#         candidate = word_tokenize(k)
#         candidate = list(dict.fromkeys(candidate))
#         candidate_lst.append(candidate)

#     query_embedd = get_embeddings(model, [query])
#     result_final_bm25_embedd = get_embeddings(model, result_final_bm25)
#     # score = np.max(cosine_similarity(query_embedd, result_final_bm25_embedd[0]), axis = 1)
#     class_or_not = []
#     '''Kiểm tra xem một văn bản có thuộc một lớp không dựa trên độ tương đồng cosine giữa các vectơ biểu diễn thông qua BERT'''
#     for i in range(len(result_final_bm25_embedd)):
#         score_individual = (np.max(cosine_similarity(query_embedd, result_final_bm25_embedd[i].reshape(1,-1)),axis=1))
#         # if score_individual > 0.5:
#         #     class_or_not.append("Văn bản thuộc lớp " + candidate_lst[i][-1])
#         # else:
#         #     class_or_not.append("Văn bản không thuộc lớp "+ candidate_lst[i][-1])
#         class_or_not.append(np.array2string(score_individual) + " " + candidate_lst[i][-1])
#     return {
#         "Query" : query,
#         "Time" : time.time() - start,
#         "Class" : class_or_not
        
#     }

# print(BM25("VN có đường sắt đô thị sớm nhất vào năm 2011 (NLĐ) - Tại hội thảo “Đường sắt đô thị” tổ chức ngày 27-3 tại Hà Nội, Cục trưởng Cục Đường sắt VN Vũ Xuân Hồng cho biết nếu đúng tiến độ, VN sẽ có tuyến đường sắt đô thị đầu tiên vào năm 2011. Đó là tuyến đường sắt Bến Thành – Chợ Nhỏ – Suối Tiên được xây dựng tại TPHCM với tổng kinh phí khoảng 700 triệu USD. Chủ trương xây dựng đường sắt đô thị tại VN được hình thành từ năm 1999 với sự giúp đỡ kỹ thuật của Chính phủ Nhật Bản. Theo kinh nghiệm phát triển đường sắt đô thị của nước này (tuyến đường sắt Tsukuba có chiều dài 58,3km được xây dựng trong 7 năm với tổng kinh phí 830 tỉ yen), để xây dựng và vận hành đường sắt đô thị, nhất thiết phải có sự tham gia giải phóng mặt bằng của chính quyền địa phương và sự trợ giúp vốn đầu tư từ phía Chính phủ. "))