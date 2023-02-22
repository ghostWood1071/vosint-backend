# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer
from pyvi.ViTokenizer import tokenize
import torch
import time

def load_model():
    """
    Load Sentence transformer model
    :return:
        model
    """
    model = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')
    return model

def get_embeddings(model, sentences):
    st = time.time()
    device_ = "cuda:0" if torch.cuda.is_available() else "cpu"
    # print("Getting embedding for document.")
    sentences_tokenizer = [tokenize(sentence) for sentence in sentences]
    embeddings = model.encode(sentences_tokenizer,device = device_)
    # print("Embedding time: ", time.time() - st)
    # print("Embedding shape :",embeddings.shape)
    return embeddings

# model = load_model()
# query = ["kuznetsova chấm dứt chuỗi trận thắng của mauresmo mauresmo trong trận thua kuznetsova nếu giành được chiến thắng trước kuznetsova thì mauresmo tại tứ kết giải dubai mở rộng thì đkvđ úc mở rộng sẽ bước lên vị trí số 1 thế giới nhưng trong một trận đấu diễn ra dưới thời tiết rất xấu hạt giống số 1 mauresmo đã gác vợt trước kuznetsova với tỷ số 7 6 6 4 ngoài việc lọt vào được bán kết giải dubai mở rộng kuznetsova còn chấm dứt luôn chuỗi 16 trận thắng liên tiếp của amelie mauresmo đây có thể coi là bất ngờ của giải bởi vì kể từ sau khi đăng quang tại giải mỹ mở rộng vào năm 2004 kuznetsova thi đấu rất dở trong khi có thể nói mauresmo đang ở trong thời kỳ đẹp nhất trong sự nghiệp của mình đối thủ của kuznetsova trong trận bán kết sẽ là tay vợt người bỉ justine henin hardenne người đã vượt qua francesca schiavone 6 4 7 6 ở một trận tứ kết khác maria sharapova đã có cuộc trả thù ngọt ngào trước martina hingis người đã loại cô ở bán kết giải pan pacific mở rộng hồi đầu tháng sharapova đã giành được chiến thắng 6 4 7 6 và giành quyền lọt vào bán kết đối thủ của cô trong trận bán kết là lindsay davenport người đã vượt qua một đồng hương của sharapova maria kirilenko sau 3 séc với tỷ số 4 6 6 2 6 3 các cặp đấu vòng bán kết svetlana kuznetsova 4 justine henin hardenne 2 lindsay davenport 3 maria sharapova"]

# print(get_embeddings(model, query))