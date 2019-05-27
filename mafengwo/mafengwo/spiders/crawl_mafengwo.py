# -*- coding: utf-8 -*-
import json
import re
import scrapy
from scrapy import Selector
from ..items import MafengwoItem
import time


class CrawlMafengwoSpider(scrapy.Spider):
    name = 'crawl_mafengwo'
    allowed_domains = ['mafengwo.cn']
    # start_urls = ['http://www.mafengwo.cn/u/wenhao/note.html']

    #请求首页
    def start_requests(self):
        #直接构造请求页码URL,如请求200页,热门游记
        for page in range(1,200):
            url = 'http://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?params={"type":0,"objid":0,"page":%s,"ajax":1,"retina":0}'%page
            yield scrapy.Request(url=url,callback=self.handle_page,dont_filter=True)

    #解析有多少篇游记，构造游记阅读量等信息URL并请求
    def handle_page(self, response):
        #获取页码页返回中的文章ID
        article_id_search = re.compile(r'<a href="/i/(.*?)\.html"')
        #获取文章ID并去重
        article_id_list = set(article_id_search.findall(json.loads(response.text)['data']['html']))
        print(article_id_list)
        #构造文章阅读量、评论数量、发表时间请求URL
        for article_id in article_id_list:
            article_header_url = 'http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?params={"iid":%s}'%article_id
            yield scrapy.Request(url=article_header_url,callback=self.handle_detail_request,meta={"article_id":article_id},dont_filter=True)

    #获取文章阅读量、评论数量、发表时间等数据，构造游记URL并请求
    def handle_detail_request(self,response):
        read_comment_search = re.compile(r'<span><i\sclass="ico_view"></i>(.*?)</span>')
        name_search = re.compile(r'class="per_name"\stitle="(.*?)">')
        star_search = re.compile(r'<span>(\d+)</span><strong>收藏</strong>')
        release_time_search = re.compile(r'<span\sclass="time">(.*?)</span>')
        html = json.loads(response.text)['data']['html']
        info = {}
        read_comment = read_comment_search.search(html).group(1).split('/')
        info['read_sum'] = read_comment[0]
        info['comment_sum'] = read_comment[1]
        info['name'] = name_search.search(html).group(1)
        info['star_sum'] = star_search.search(html).group(1)
        info['release_time'] = release_time_search.search(html).group(1)
        info['id'] = response.request.meta['article_id']
        info['url'] = 'http://www.mafengwo.cn/i/%s.html' % (response.request.meta['article_id'])
        print(info)
        yield scrapy.Request(url=info['url'],callback=self.handle_detail,meta=info,dont_filter=True)

    # 解析游记
    def handle_detail(self, response):
        id_search = re.compile(r"window.Env\s=\s(.*);")
        seq_search = re.compile(r'data-seq="(\d+)"')
        try:
            id_result = json.loads(id_search.search(response.text).group(1))
        except:
            return
        #获取是否存在下一页标志
        iid = id_result.get('new_iid')
        # 存在下一页
        if iid:
            print(response.url + "存在多页")
            response.request.meta['iid'] = iid
            # 文章标题
            response.request.meta['title'] = response.xpath("//title/text()").extract_first()
            # 文章内容
            response.request.meta['content'] = response.xpath("//div[@class='_j_content_box']").extract()
            # 请求URL
            response.request.meta['from_url'] = response.url
            # 请求下一页所使用的ID
            next_request_seq = seq_search.findall(response.text)[-1]
            next_detail_url = "http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id=%s&iid=%s&seq=%s&back=0" % (response.request.meta['id'], iid, next_request_seq)
            yield scrapy.Request(url=next_detail_url, callback=self.handle_detail_json, dont_filter=True,meta=response.request.meta)
        # 不存在下一页
        else:
            # 处理游记
            mafengwo_data = MafengwoItem()
            mafengwo_data['title'] = response.xpath("//title/text()").extract_first()
            mafengwo_data['from_url'] = response.request.meta['from_url']
            mafengwo_data['read_sum'] = response.request.meta['read_sum']
            mafengwo_data['comment_sum'] = response.request.meta['comment_sum']
            mafengwo_data['star_sum'] = response.request.meta['star_sum']
            mafengwo_data['release_time'] = response.request.meta['release_time']
            mafengwo_data['name'] = response.request.meta['name']
            mafengwo_data['id'] = response.request.meta['id']
            mafengwo_data['content'] = self.handle_img_src(''.join(response.xpath("//div[@id='pnl_contentinfo']").extract_first()))
            #获取文章中所有图片URL
            photo_url_search = re.compile(r'data-src="(.*?)\?')
            mafengwo_data['image_urls'] = photo_url_search.findall(mafengwo_data['content'])
            mafengwo_data['crawl_time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
            yield mafengwo_data

    def handle_detail_json(self, response):
        seq_search = re.compile(r'data-seq="(\d+)"')
        html_text = json.loads(response.text)['data']
        #请求到末页
        if html_text['html'] == "":
            mafengwo_data = MafengwoItem()
            mafengwo_data['title'] = response.request.meta['title']
            mafengwo_data['from_url'] = response.request.meta['from_url']
            mafengwo_data['read_sum'] = response.request.meta['read_sum']
            mafengwo_data['comment_sum'] = response.request.meta['comment_sum']
            mafengwo_data['star_sum'] = response.request.meta['star_sum']
            mafengwo_data['release_time'] = response.request.meta['release_time']
            mafengwo_data['name'] = response.request.meta['name']
            mafengwo_data['id'] = response.request.meta['id']
            mafengwo_data['content'] = self.handle_img_src(''.join(response.request.meta['content']))
            mafengwo_data['crawl_time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
            photo_url_search = re.compile(r'data-src="(.*?)\?')
            mafengwo_data['image_urls'] = photo_url_search.findall(mafengwo_data['content'])
            yield mafengwo_data
        #继续请求下一页
        else:
            html = html_text['html']
            response.request.meta['content'].append(html)
            next_request_seq = seq_search.findall(html)[-1]
            if next_request_seq:
                next_detail_url = "http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id=%s&iid=%s&seq=%s&back=0" % (response.request.meta['id'], response.request.meta['iid'], next_request_seq)
                yield scrapy.Request(url=next_detail_url, callback=self.handle_detail_json, dont_filter=True,meta=response.request.meta)

    # 处理游记中的图片URL
    def handle_img_src(self, text):
        img_search = re.compile(r"<img.*?alt=.*?>|<img.*?>")
        img_data_src_search = re.compile(r'data-src="(.*?)\?')
        src_search = re.compile(r'[^-]src="(.*?)"')
        img_list = img_search.findall(text)
        for img in img_list:
            try:
                img_data_src = img_data_src_search.search(img).group(1)
                src = src_search.search(img).group(1)
                img_new = img.replace(src, img_data_src)
                text = text.replace(img, img_new)
            except:
                pass
        return text

