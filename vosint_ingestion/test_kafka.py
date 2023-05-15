
from kafka.admin import KafkaAdminClient, NewTopic

def check_topic_exist(topic_name):
        admin_client = KafkaAdminClient(bootstrap_servers=['192.168.1.63:9092'])
        topic_metadata = admin_client.list_topics()
        if topic_name not in set(t for t in topic_metadata):
            return False
        else:
            return True

print(check_topic_exist("crawling"))