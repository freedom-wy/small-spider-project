import pymongo
from pymongo.collection import Collection



class Handle_lagou_mongo(object):
    def __init__(self):
        lagou_client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        self.lagou_db = lagou_client['lagou']

    def handle_save_data(self,item):
        print(item)
        lagou_collection = Collection(self.lagou_db,"lagou_data")
        lagou_collection.update({"positionId":item['positionId']},item,True)


lagou_mongo = Handle_lagou_mongo()