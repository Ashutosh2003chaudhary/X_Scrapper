from pymongo import MongoClient
from datetime import datetime
import uuid

class MongoDB:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['twitter_trends']
        self.collection = self.db['trends']
        
    def save_trends(self, trends, ip_address):
        record = {
            '_id': str(uuid.uuid4()),
            'trends': trends,
            'timestamp': datetime.now(),
            'ip_address': ip_address
        }
        self.collection.insert_one(record)
        return record
        
    def get_latest_record(self):
        return self.collection.find_one(sort=[('timestamp', -1)])
