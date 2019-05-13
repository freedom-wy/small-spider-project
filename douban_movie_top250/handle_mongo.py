import pymongo
from pymongo.collection import Collection


class Handle_Mongo(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        self.db_data = mongo_client['douban']

    def handle_save_data(self,item):
        task_collection = Collection(self.db_data,'douban_data')
        task_collection.insert(item)

douban_mongo = Handle_Mongo()
