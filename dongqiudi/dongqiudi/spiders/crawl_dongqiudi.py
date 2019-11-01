# -*- coding: utf-8 -*-
import scrapy
from ..items import DongqiudiItem
import time
import json


class CrawlDongqiudiSpider(scrapy.Spider):
    name = 'crawl_dongqiudi'
    allowed_domains = ['dongqiudi.com']
    start_urls = ['http://dongqiudi.com/']

    #分析懂球帝页面，通过浏览器开发者工具xhr，可以看到异步json请求
    def start_requests(self,time_value=None):
        #初始时间使用time.time()构造
        if time_value == None:
            time_value = int(time.time())
        #分析页面新闻结构
        for item_value in [56,232,57,3,4,5,6]:
            #如该请求https://dongqiudi.com/api/app/tabs/web/56.json?after=1572577395&page=1
            #其中56为栏目编号,after为时间戳,page为页码
            page_url = "https://dongqiudi.com/api/app/tabs/web/%s.json?after=%s&page=1"%(item_value,time_value)
            yield scrapy.Request(url=page_url,callback=self.handle_page_response,dont_filter=True)

    #处理页码请求的返回
    def handle_page_response(self,response):
        response_dict = json.loads(response.text)
        #从返回中获取下一页链接
        next_url = response_dict.get('next')
        if next_url:
            #请求下一页
            yield scrapy.Request(url=next_url,callback=self.handle_page_response,dont_filter=True)

        #解析新闻列表
        news_list = response_dict.get('articles')
        if news_list:
            for item in news_list:
                info = {}
                #新闻URL
                info['from_url'] = item.get('url')
                #新闻标题
                info['title'] = item.get('title')
                #新闻发表时间
                info['release_time'] = item.get('published_at')
                yield scrapy.Request(url=info['from_url'],callback=self.handle_detail,dont_filter=True,meta=info)

    #处理新闻详情页
    def handle_detail(self,response):
        dongqiudi = DongqiudiItem()
        #作者
        dongqiudi['author'] = response.xpath("//header/h2/a/text()").extract_first()
        #内容
        dongqiudi['content'] = ''.join(response.xpath("//div[@class='con']/p/text()").extract())
        #新闻图片
        dongqiudi['image_urls'] = response.xpath("//div[@class='con']/p/img/@data-src").extract()
        #抓取时间
        dongqiudi['crawl_time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        #新闻标题
        dongqiudi['title'] = response.request.meta['title']
        #抓取url
        dongqiudi['from_url'] = response.request.meta['from_url']
        #发表时间
        dongqiudi['release_time'] = response.request.meta['release_time']
        #yield到pipeline中
        yield dongqiudi
