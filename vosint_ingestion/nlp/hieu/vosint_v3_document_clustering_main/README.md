# Phân loại văn bản dựa trên tập mẫu có sẵn

Đây là hệ thông phân loại văn bản dựa trên một tập văn bản được cho sẵn

## Tính năng

- Phân loại một văn bản mới vào một chủ đề đã có tập văn bản mẫu có sẵn
- Không giới hạn số lượng chủ đề

## Công nghệ

- [Python] 
- [Underthesea] - Dùng để tokenize văn bản
- [fastapi] - tạo API 
- [bm25] - thuật toán BM25

## Cài đặt
Bước 1 : Download source code
```sh
git clone https://gitlab.aiacademy.edu.vn/research-develop/nlp/vosint_v3_document_clustering.git
cd ../vosint_v3_document_clustering
```

Bước 2 : Cài đặt các thư viện cần thiết
```sh
pip install -r requirements.txt
```

Bước 3 : Khởi chạy dự án
```sh
cd ../src
python main.py
```
