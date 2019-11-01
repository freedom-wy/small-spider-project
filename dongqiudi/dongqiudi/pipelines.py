# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from pymongo.collection import Collection
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

#存储数据
class DongqiudiPipeline(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(host='192.168.7.142',port=27017)
        self.dongqiudi_db = mongo_client['dongqiudi_data']
    def process_item(self, item, spider):
        dongqiudi_collection = Collection(self.dongqiudi_db,"dongqiudi")
        dongqiudi_collection.update({'from_url':item['from_url']},item,True)
        return item

#下载图片
class DongqiudiImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(url=image_url,meta={'img_name':image_url,'photo_id':item['title']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            pass
        return item

    def file_path(self, request, response=None, info=None):
        filename = './' + str(request.meta['photo_id'])+'/'+request.meta['img_name'].split("/")[-1]
        return filename
