# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo,json
from pymongo.collection import Collection

class DoubanPipeline(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db_data = mongo_client['douban_scrapy']

    def process_item(self, item, spider):
        #指定数据库和表
        douban_collection = Collection(self.db_data,'douban')
        douban_collection.insert(dict(item))
        return item

class DoubanJsonPipeline(object):
    def __init__(self):
        self.file = open('douban.json','w')

    def process_item(self, item, spider):
        # json数据中添加逗号和换行符
        content = json.dumps(dict(item),ensure_ascii = False) + ",\n"
        self.file.write(content)
        return item

    def close_spider(self,spider):
        self.file.close()
