# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy
from scrapy import Selector
from ..items import MafengwoItem


class CrawlMafengwoSpider(scrapy.Spider):
    name = 'crawl_mafengwo'
    allowed_domains = ['mafengwo.cn']
    # start_urls = ['http://www.mafengwo.cn/u/wenhao/note.html']

    #请求首页
    def start_requests(self):
        # with open('url_list.txt', 'r') as f:
        #     url_list = f.readlines()
        #     for url in url_list:
        #         yield scrapy.Request(url=url.replace("\n",""),callback=self.parse_index)
        url = "http://www.mafengwo.cn/u/wenhao/note.html"
        yield scrapy.Request(url=url,callback=self.parse_index)

    #解析有多少篇游记
    def parse_index(self, response):
        item = {}
        item['name'] = response.xpath("//span[@class='MAvaName']/text()").extract_first()
        for article in response.xpath("//div[@class='notes_list']/ul/li"):
            item['from_url'] = "http://www.mafengwo.cn"+article.xpath("./dl/dt/a/@href").extract_first()
            read_comment_value = article.xpath(".//div[@class='note_more']/span[1]/em/text()").extract_first().split("/")
            if len(read_comment_value) == 2:
                item['read_sum'] = read_comment_value[0]
                item['comment_sum'] = read_comment_value[1]
            item['star_sum'] = article.xpath(".//div[@class='note_more']/span[2]/em/text()").extract_first()
            item['support_sum'] = article.xpath(".//div[@class='MDing']/span[1]/text()").extract_first()
            item['release_time'] = article.xpath(".//div[@class='note_more']/span[@class='time']/text()").extract_first()
            item['id'] = None
            item['iid'] = None
            item['detail'] = []
            yield scrapy.Request(url=item['from_url'],meta=item,callback=self.handle_detail)

    #解析游记
    def handle_detail(self,response):
        sub_something = re.compile(r"[\r\n\s]+")
        id_search = re.compile(r"window.Env\s=\s(.*);")
        try:
            id_result = json.loads(id_search.search(response.text).group(1))
        except:
            return
        id = id_result['iid']
        iid = id_result.get('new_iid')
        #存在滑动页面
        if iid:
            response.request.meta['id'] = id
            response.request.meta['iid'] = iid
            response.request.meta['title'] = response.xpath("//title/text()").extract_first()
            detail_list = response.xpath("//div[@class='_j_content_box']//p").xpath('string(.)').extract()
            for detail_item in detail_list:
                response.request.meta['detail'].append(sub_something.sub("", detail_item))
            next_request_seq = response.xpath("//p[last()]/@data-seq").extract_first()
            next_detail_url = "http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id=%s&iid=%s&seq=%s&back=0" % (id, iid, next_request_seq)
            yield scrapy.Request(url=next_detail_url, callback=self.handle_detail_json, dont_filter=True,meta=response.request.meta)
        #不存在滑动页面
        else:
            mafengwo_data = MafengwoItem()
            mafengwo_data['title'] = response.xpath("//title/text()").extract_first()
            mafengwo_data['from_url'] = response.request.meta['from_url']
            mafengwo_data['read_sum'] = response.request.meta['read_sum']
            mafengwo_data['comment_sum'] = response.request.meta['comment_sum']
            mafengwo_data['star_sum'] = response.request.meta['star_sum']
            mafengwo_data['support_sum'] = response.request.meta['support_sum']
            mafengwo_data['release_time'] = response.request.meta['release_time']
            mafengwo_data['name'] = response.request.meta['name']
            detail_list = response.xpath("//p[@class='_j_note_content']").xpath('string(.)').extract()
            for detail_item in detail_list:
                response.request.meta['detail'].append(sub_something.sub("",detail_item))
            mafengwo_data['content'] = ''.join(response.request.meta['detail'])
            yield mafengwo_data

    def handle_detail_json(self,response):
        mafengwo_data = MafengwoItem()
        sub_something = re.compile(r"[\r\n\s]+")
        html_text = json.loads(response.text)['data']
        if html_text['html'] == "":
            mafengwo_data['title'] = response.request.meta['title']
            mafengwo_data['from_url'] = response.request.meta['from_url']
            mafengwo_data['read_sum'] = response.request.meta['read_sum']
            mafengwo_data['comment_sum'] = response.request.meta['comment_sum']
            mafengwo_data['star_sum'] = response.request.meta['star_sum']
            mafengwo_data['support_sum'] = response.request.meta['support_sum']
            mafengwo_data['release_time'] = response.request.meta['release_time']
            mafengwo_data['content'] = ''.join(response.request.meta['detail'])
            mafengwo_data['name'] = response.request.meta['name']
            yield mafengwo_data
        html = Selector(text=html_text['html'])
        detail_list = html.xpath("//p").xpath('string(.)').extract()
        for detail_item in detail_list:
            response.request.meta['detail'].append(sub_something.sub("", detail_item))
        next_request_seq = html.xpath("//p[last()]/@data-seq").extract_first()
        if next_request_seq:
            next_detail_url = "http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id=%s&iid=%s&seq=%s&back=0" % (response.request.meta['id'], response.request.meta['iid'], next_request_seq)
            yield scrapy.Request(url=next_detail_url, callback=self.handle_detail_json, dont_filter=True,meta=response.request.meta)


