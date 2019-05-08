# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MafengwoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #文章数量
    article_sum = scrapy.Field()
    #文章标题
    title = scrapy.Field()
    #作者名称
    name = scrapy.Field()
    #id
    id = scrapy.Field()
    #文章发表时间
    release_time = scrapy.Field()
    #评论数
    comment_sum = scrapy.Field()
    #收藏数
    star_sum = scrapy.Field()
    #顶
    support_sum = scrapy.Field()
    #阅读数
    read_sum = scrapy.Field()
    #文章内容
    content = scrapy.Field()
    #抓取URL
    from_url = scrapy.Field()
    #抓取时间
    crawl_time = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
