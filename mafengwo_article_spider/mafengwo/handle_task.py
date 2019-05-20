import requests
import re
import json
from mafengwo.handle_mongo import mongo


class HandleMaFengWoTask(object):
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def handle_new_article(self):
        article_url_search = re.compile(r'a\shref="/i/(\d+)\.html"')
        for i in range(1,80000):
            info = {}
            info['flag'] = 'GET'
            info['url'] = 'https://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?params={"type":3,"objid":0,"page":%s,"ajax":1,"retina":0}'%i
            new_article = self.handle_request(info)
            html = json.loads(new_article)['data']['html']
            #解析游记
            article_url_list = article_url_search.findall(html)
            for article_id in set(article_url_list):
                insert_mongo = {}
                insert_mongo['id'] = article_id
                insert_mongo['url'] = 'http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?params={"iid":"%s"}'%article_id
                insert_mongo['item_type'] = 'head_item'
                mongo.insert_task(insert_mongo)
            break

    def handle_hot_article(self):
        article_url_search = re.compile(r'a\shref="(/i/\d+\.html)"')
        for i in range(1,200):
            info = {}
            info['flag'] = 'GET'
            info['url'] = 'https://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?params={"type":0,"objid":0,"page":%s,"ajax":1,"retina":0}'%i
            hot_article = self.handle_request(info)
            html = json.loads(hot_article)['data']['html']
            #解析游记
            article_url_list = article_url_search.findall(html)
            for article_url in set(article_url_list):
                url = 'https://www.mafengwo.cn'+article_url
                print(url)
            break

    def handle_new_column(self):
        column_url_search = re.compile(r'/traveller/article.php\?id=\d+')
        for i in range(0,2000,10):
            info= {}
            info['flag'] = 'GET'
            info['url'] = 'https://www.mafengwo.cn/traveller/ajax.php?action=getMoreArticles&sort=ctime&start=%s'%i
            new_column = self.handle_request(info)
            html = json.loads(new_column)['html']
            column_list = column_url_search.findall(html)
            for column in set(column_list):
                url = 'https://www.mafengwo.cn'+column
                print(url)
            break

    def handle_hot_column(self):
        column_url_search = re.compile(r'/traveller/article.php\?id=\d+')
        for i in range(0,2000,10):
            info= {}
            info['flag'] = 'GET'
            info['url'] = 'https://www.mafengwo.cn/traveller/ajax.php?action=getMoreArticles&sort=hot&start=%s'%i
            new_column = self.handle_request(info)
            html = json.loads(new_column)['html']
            column_list = column_url_search.findall(html)
            for column in set(column_list):
                url = 'https://www.mafengwo.cn'+column
                print(url)
            break


    def handle_request(self,info):
        if info['flag'] == 'GET':
            response = requests.get(url=info['url'],headers=self.header)
            return response.text
        elif info['flag'] == 'POST':
            response = requests.post(url=info['url'],headers=self.header,data=info['data'])
            return response.text

    def run(self):
        self.handle_new_article()
        # self.handle_hot_article()
        # self.handle_new_column()
        # self.handle_hot_column()

def main():
    mafengwo_task = HandleMaFengWoTask()
    mafengwo_task.run()

if __name__ == '__main__':
    main()
