import pymongo
from pymongo.collection import Collection




class Mafengwo_mongo(object):
    def __init__(self):
        # mongo_client = pymongo.MongoClient(host='127.0.0.1', port=39070)
        mongo_client = pymongo.MongoClient(host='10.70.120.156', port=27017)
        self.db_data = mongo_client['oreo']

    def get_from_url(self, item):
        db_collections = Collection(self.db_data, 'mafengwo_article')
        result = db_collections.find_one({'from_url':item})
        if result:
            return True
        else:
            return False
        #return False

    def insert_task(self,item):
        db_collections = Collection(self.db_data, 'mafengwo_article_task')
        db_collections.insert_one(item)

    def get_task(self):
        db_collections = Collection(self.db_data, 'mafengwo_article_task')
        return db_collections.find_one_and_delete({})


mongo = Mafengwo_mongo()
