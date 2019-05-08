# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.collection import Collection

class MafengwoPipeline(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db_data = mongo_client['mafengwo']

    def process_item(self, item, spider):
        db_collections = Collection(self.db_data, 'mafengwo_article')
        db_collections.update({'from_url':item['from_url']},item,True)
        return item
