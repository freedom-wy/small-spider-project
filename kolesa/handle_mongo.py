import pymongo
from pymongo.collection import Collection


class Handle_Mongo(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        self.db_data = mongo_client['kolesa']

    def handle_save_task(self,item):
        task_collection = Collection(self.db_data,'kolesa_task')
        task_collection.update({'id':item['id']},item,True)

    def handle_get_task(self):
        task_collection = Collection(self.db_data,'kolesa_task')
        return task_collection.find_one_and_delete({})

    def handle_save_data(self,item):
        task_collection = Collection(self.db_data,'kolesa_data')
        task_collection.update({'id':item['id']},item,True)

kolesa_mongo = Handle_Mongo()