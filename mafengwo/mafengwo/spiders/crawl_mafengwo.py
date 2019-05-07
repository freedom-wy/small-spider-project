# -*- coding: utf-8 -*-
import scrapy
from ..items import MafengwoItem


class CrawlMafengwoSpider(scrapy.Spider):
    name = 'crawl_mafengwo'
    allowed_domains = ['mafengwo.cn']
    # start_urls = ['http://mafengwo.cn/']

    def start_requests(self):
        url = "http://www.mafengwo.cn/u/wenhao/note.html"
        yield scrapy.Request(url=url,callback=self.parse_index)

    def parse_index(self, response):
        item = {}
        for article in response.xpath("//div[@class='notes_list']/ul/li"):
            item['from_url'] = "http://www.mafengwo.cn"+article.xpath("./dl/dt/a/@href").extract_first()
            read_comment_value = article.xpath(".//div[@class='note_more']/span[1]/em/text()").extract_first().split("/")
            if len(read_comment_value) == 2:
                item['read_sum'] = read_comment_value[0]
                item['comment_sum'] = read_comment_value[1]
            item['star_sum'] = article.xpath(".//div[@class='note_more']/span[2]/em/text()").extract_first()
            item['support_sum'] = article.xpath(".//div[@class='MDing']/span[1]/text()").extract_first()
            item['release_time'] = article.xpath(".//div[@class='note_more']/span[@class='time']/text()").extract_first()
            print(item)

