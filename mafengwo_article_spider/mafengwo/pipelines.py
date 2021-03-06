# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.collection import Collection
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class MafengwoPipeline(object):
    def __init__(self):
        # mongo_client = pymongo.MongoClient(host='127.0.0.1', port=39070)
        mongo_client = pymongo.MongoClient(host='10.70.120.156', port=27017)
        self.db_data = mongo_client['oreo']

    def process_item(self, item, spider):
        db_collections = Collection(self.db_data, 'mafengwo_article')
        db_collections.update({'from_url':item['from_url']},item,True)
        return item


class MafengwoImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(url=image_url,meta={'img_name':image_url,'photo_id':item['id']})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            pass
        #item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        filename = './' + str(request.meta['photo_id'])+'/'+request.meta['img_name'].split("/")[-1]
        return filename
