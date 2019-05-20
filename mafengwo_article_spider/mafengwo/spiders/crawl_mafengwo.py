# -*- coding: utf-8 -*-
import json
import re
import time
import scrapy
from ..items import MafengwoItem
from mafengwo.handle_mongo import mongo


class CrawlMafengwoSpider(scrapy.Spider):
    name = 'crawl_mafengwo'
    allowed_domains = ['mafengwo.cn']

    #从task库中取出任务
    def start_requests(self):
        for i in range(1):
            task = mongo.get_task()
            #如果有任务则执行
            if task:
                if '_id' in task:
                    task.pop('_id')
                print(task)
                if task['item_type'] == 'head_item':
                    yield scrapy.Request(url=task['url'],callback=self.handle_detail_head,dont_filter=True,meta=task)
                elif task['item_type'] == 'article_item':
                    yield scrapy.Request(url=task['url'],callback=self.handle_detail,dont_filter=True,meta=task)

    #解析美篇游记的头部信息
    def handle_detail_head(self,response):
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
        info['item_type'] = 'article_item'
        info['url'] = 'http://www.mafengwo.cn/i/%s.html'%(response.request.meta['id'])
        mongo.insert_task(info)

    #解析游记
    def handle_detail(self,response):
        id_search = re.compile(r"window.Env\s=\s(.*);")
        seq_search = re.compile(r'data-seq="(\d+)"')
        try:
            id_result = json.loads(id_search.search(response.text).group(1))
        except:
            return
        id = id_result['iid']
        iid = id_result.get('new_iid')
        #存在下一页
        if iid:
            print(response.url+"存在多页")
            response.request.meta['id'] = id
            response.request.meta['iid'] = iid
            #文章标题
            response.request.meta['title'] = response.xpath("//title/text()").extract_first()
            #文章内容
            response.request.meta['content'] = response.xpath("//div[@class='_j_content_box']").extract()
            #请求URL
            response.request.meta['from_url'] = response.url
            #请求下一页所使用的ID
            next_request_seq = seq_search.findall(response.text)[-1]
            next_detail_url = "http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id=%s&iid=%s&seq=%s&back=0" % (id, iid, next_request_seq)
            yield scrapy.Request(url=next_detail_url, callback=self.handle_detail_json, dont_filter=True,meta=response.request.meta)
        # 不存在下一页
        else:
            #处理游记
            m3u8_search = re.compile(r'data-url="(.*\.m3u8)"')
            mafengwo_data = MafengwoItem()
            mafengwo_data['title'] = response.xpath("//title/text()").extract_first()
            mafengwo_data['from_url'] = response.request.meta['from_url']
            mafengwo_data['read_sum'] = response.request.meta['read_sum']
            mafengwo_data['comment_sum'] = response.request.meta['comment_sum']
            mafengwo_data['star_sum'] = response.request.meta['star_sum']
            # mafengwo_data['support_sum'] = response.request.meta['support_sum']
            mafengwo_data['release_time'] = response.request.meta['release_time']
            mafengwo_data['name'] = response.request.meta['name']
            mafengwo_data['id'] = id
            mafengwo_data['content'] = self.handle_img_src(''.join(response.xpath("//div[@id='pnl_contentinfo']").extract_first()))
            photo_url_search = re.compile(r'data-src="(.*?)\?')
            mafengwo_data['video_urls'] = m3u8_search.findall(mafengwo_data['content'])
            mafengwo_data['image_urls'] = photo_url_search.findall(mafengwo_data['content'])
            mafengwo_data['upload_status'] = 0
            mafengwo_data['crawl_time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
            yield mafengwo_data

    def handle_detail_json(self,response):
        m3u8_search = re.compile(r'data-url="(.*\.m3u8)"')
        seq_search = re.compile(r'data-seq="(\d+)"')
        html_text = json.loads(response.text)['data']
        if html_text['html'] == "":
            mafengwo_data = MafengwoItem()
            mafengwo_data['title'] = response.request.meta['title']
            mafengwo_data['from_url'] = response.request.meta['from_url']
            mafengwo_data['read_sum'] = response.request.meta['read_sum']
            mafengwo_data['comment_sum'] = response.request.meta['comment_sum']
            mafengwo_data['star_sum'] = response.request.meta['star_sum']
            # mafengwo_data['support_sum'] = response.request.meta['support_sum']
            mafengwo_data['release_time'] = response.request.meta['release_time']
            mafengwo_data['name'] = response.request.meta['name']
            mafengwo_data['id'] = response.request.meta['id']
            mafengwo_data['content'] = self.handle_img_src(''.join(response.request.meta['content']))
            mafengwo_data['upload_status'] = 0
            mafengwo_data['crawl_time'] = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
            photo_url_search = re.compile(r'data-src="(.*?)\?')
            mafengwo_data['video_urls'] = m3u8_search.findall(mafengwo_data['content'])
            mafengwo_data['image_urls'] = photo_url_search.findall(mafengwo_data['content'])
            yield mafengwo_data
        else:
            html = html_text['html']
            response.request.meta['content'].append(html)
            next_request_seq = seq_search.findall(html)[-1]
            if next_request_seq:
                next_detail_url = "http://www.mafengwo.cn/note/ajax/detail/getNoteDetailContentChunk?id=%s&iid=%s&seq=%s&back=0" % (response.request.meta['id'], response.request.meta['iid'], next_request_seq)
                yield scrapy.Request(url=next_detail_url, callback=self.handle_detail_json, dont_filter=True,meta=response.request.meta)

    #处理游记中的图片URL
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
