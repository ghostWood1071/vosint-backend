from elasticsearch import Elasticsearch

# Tạo một đối tượng Elasticsearch với địa chỉ IP và cổng của máy chạy Elasticsearch
es = Elasticsearch(['192.168.1.58:9200'])

# Kiểm tra kết nối đến Elasticsearch server
if es.ping():
    print('Kết nối thành công đến Elasticsearch trên máy khác!')
else:
    print('Không thể kết nối đến Elasticsearch trên máy khác!')