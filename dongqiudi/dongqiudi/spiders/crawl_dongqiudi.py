# -*- coding: utf-8 -*-
import scrapy
from ..items import DongqiudiItem
import time


class CrawlDongqiudiSpider(scrapy.Spider):
    name = 'crawl_dongqiudi'
    allowed_domains = ['dongqiudi.com']
    start_urls = ['http://dongqiudi.com/']

    #构造页码请求,如当前页面显示有13822页,需要分析当前标签下最大请求页码
    def start_requests(self):
        for page in range(1,50):
            #分析标签结构
            for item_value in [1,56,55,37,120,3,5,4,6]:
                page_url = "http://www.dongqiudi.com/?tab=%s&page=%s"%(item_value,page)
                yield scrapy.Request(url=page_url,callback=self.handle_page_response,dont_filter=True)

    #处理页码请求的返回
    def handle_page_response(self,response):
        news_list = response.xpath("//div[@id='news_list']/ol/li")
        for news in news_list:
            info = {}
            #新闻URL
            info['from_url'] = news.xpath("./h2/a/@href").extract_first()
            #新闻标题
            info['title'] = news.xpath("./h2/a/text()").extract_first()
            yield scrapy.Request(url=info['from_url'],callback=self.handle_detail,dont_filter=True,meta=info)

    #处理新闻详情页
    def handle_detail(self,response):
        dongqiudi = DongqiudiItem()
        #新闻发表时间
        dongqiudi['release_time'] = response.xpath("//span[@class='time']/text()").extract_first()
        #作者
        dongqiudi['author'] = response.xpath("//span[@class='name']/text()").extract_first()
        #内容
        dongqiudi['content'] = ''.join(response.xpath("//div[@class='detail']/div/p/text()").extract())
        #新闻图片
        dongqiudi['image_urls'] = response.xpath("//div[@class='detail']/div/p/img/@src").extract()
        #抓取时间
        dongqiudi['crawl_time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
        #新闻标题
        dongqiudi['title'] = response.request.meta['title']
        #抓取url
        dongqiudi['from_url'] = response.request.meta['from_url']
        #yield到pipeline中
        yield dongqiudi
