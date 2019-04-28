import requests
import time
from lxml import etree
import re

class HandleLishipin(object):
    def __init__(self):
        self.header = {
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
        }

    def handle_html(self,url):
        response = requests.get(url=url,headers=self.header)
        return response.text

if __name__ == '__main__':
    l = HandleLishipin()
    list_url = [
        {"name":"新知","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=10&start=%d&sort=%d"},
        {"name":"社会","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=1&start=%d&sort=%d"},
        {"name":"世界","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=2&start=%d&sort=%d"},
        {"name":"生活","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=5&start=%d&sort=%d"},
        {"name":"娱乐","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=4&start=%d&sort=%d"},
        {"name":"财富","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=3&start=%d&sort=%d"},
        {"name":"美食","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=6&start=%d&sort=%d"},
        {"name":"音乐","item_url":"https://www.pearvideo.com/popular_loading.jsp?reqType=1&categoryId=59&start=%d&sort=%d"},
    ]
    for item in list_url:
        for i in range(0,110,10):
            item_url =item['item_url']%(i,i)
            detail_text = l.handle_html(item_url)
            detail_html = etree.HTML(detail_text)
            detail_url = detail_html.xpath("//li[@class='popularem clearfix']//a[@class='actplay']/@href")
            video_url_search = re.compile(r'srcUrl="(.*?)"')
            video_name_search = re.compile(r'<h1\sclass="video-tt">(.*?)</h1>')
            for url in detail_url:
                url = "https://www.pearvideo.com/"+url
                video_text = l.handle_html(url)
                video_url = video_url_search.search(video_text).group(1)
                video_name = video_name_search.search(video_text).group(1)
                info = {}
                info['video_url'] = video_url
                info['name'] = video_name
                info['type'] = item['name']
                info['from_url'] = url
                info['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
