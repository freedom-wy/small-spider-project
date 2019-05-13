import pymongo
from pymongo.collection import Collection


class Handle_Mongo(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        self.db_data = mongo_client['kolesa']

    def handle_save_task(self,item):
        task_collection = Collection(self.db_data,'kolesa_task')
        task_collection.update({'id':item['id']},item,True)

mongo = Handle_Mongo()