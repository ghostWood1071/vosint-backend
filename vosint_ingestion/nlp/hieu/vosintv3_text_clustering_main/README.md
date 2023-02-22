# VOSINT V3 Phân loại văn bản theo từ khóa



Đây là hệ thống phân loại văn bản dựa trên từ khóa bắt buộc và từ khóa loại trừ

## Tính năng 
- Phân loại văn bản với số nhãn không giới hạn dựa trên từ khóa bắt buộc và từ khóa loại trừ
- Mỗi nhãn sẽ có từ khóa bắt buộc và từ khóa loại trừ. Nếu văn bản chứa toàn bộ các từ khóa bắt buộc và không chứa từ khóa loại trừ nào thì văn bản sẽ thuộc nhãn đó

## Công nghệ

- [Python] 

## Cài đặt

Download source code 
```sh
git clone https://gitlab.aiacademy.edu.vn/research-develop/nlp/vosintv3_text_clustering.git
cd ../vosintv3_text_clustering
```

Cài đặt các thư viện cần thiết
```sh
pip install -r requirements.txt
```

Chạy service
```sh
python src/main.py
```
