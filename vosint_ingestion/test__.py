# from elasticsearch import Elasticsearch

# # Connect to Elasticsearch
# es = Elasticsearch([{'host': '192.168.1.99', 'port': 9200}])

# # Define your query
# query = {
#   "query": {
#     "match": {
#       "url": 'https://dantri.com.vn/van-hoa/thuc-hu-thong-tin-binh-tinh-duoc-co-nghe-si-vu-linh-de-lai-het-tai-san-20230328063244094.htm'
#     }
#   },
#   "size": 1

# }

# # Execute the query
# response = es.search(index="vosint", body=query)

# # Process the results
# for hit in response['hits']['hits']:
#     print((hit['_source']))
   
# import json
# from elasticsearch import Elasticsearch
# from features.job.minh.Elasticsearch_main.elastic_main import My_ElasticSearch
# # from elastic_main import My_ElasticSearch

# my_es = My_ElasticSearch(host=['http://192.168.1.99:9200'], user='USER', password='PASS', verify_certs=False)
# print(my_es.search_main(index_name="vosint", query='"nghệ sĩ" + "con gái"', k=10))


import requests

url = 'http://vosint.aiacademy.edu.vn/api/pipeline/Job/api/create_required_keyword'
params = {'newsletter_id': '642e78353515902f1620006a'}

response = requests.post(url, params=params)

if response.status_code == 200:
    # API call successful
    data = response.json()
    print(data)
else:
    # API call unsuccessful
    print('Error:', response.status_code)