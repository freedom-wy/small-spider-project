import random
import time
import requests
import re
import json
from handle_mongo import mongo
from settings import proxy_url
from concurrent.futures.thread import ThreadPoolExecutor
import multiprocessing


class HandleMaFengWoTask(object):
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.proxy_list = []

    def handle_proxy(self):
        response = requests.get(url=proxy_url)
        data = json.loads(response.text)
        sum = 0
        #每请求一次加入200个代理
        for proxy in data['proxys']:
            sum = sum + 1
            if sum > 200:
                break
            proxy_dict = {
                "http": proxy['proxy'],
                "https": proxy['proxy']
            }
            self.proxy_list.append(proxy_dict)


    #最新游记
    def handle_new_article(self,page):
        article_url_search = re.compile(r'a\shref="/i/(\d+)\.html"')
        info = {}
        info['flag'] = 'GET'
        info['url'] = 'https://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?params={"type":3,"objid":0,"page":%s,"ajax":1,"retina":0}'%page
        print(info['url'])
        new_article = self.handle_request(info)
        try:
            html = json.loads(new_article)['data']['html']
        except:
            return
        article_url_list = article_url_search.findall(html)
        for article_id in set(article_url_list):
            insert_mongo = {}
            insert_mongo['id'] = article_id
            insert_mongo['url'] = 'http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?params={"iid":"%s"}'%article_id
            insert_mongo['item_type'] = 'head_item'
            print(insert_mongo)
            mongo.insert_task(insert_mongo)

    #热门游记
    def handle_hot_article(self,page):
        article_url_search = re.compile(r'a\shref="/i/(\d+)\.html"')
        info = {}
        info['flag'] = 'GET'
        info['url'] = 'https://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?params={"type":0,"objid":0,"page":%s,"ajax":1,"retina":0}' % page
        print(info['url'])
        new_article = self.handle_request(info)
        try:
            html = json.loads(new_article)['data']['html']
        except:
            return
        article_url_list = article_url_search.findall(html)
        for article_id in set(article_url_list):
            insert_mongo = {}
            insert_mongo['id'] = article_id
            insert_mongo[
                'url'] = 'http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?params={"iid":"%s"}' % article_id
            insert_mongo['item_type'] = 'head_item'
            print(insert_mongo)
            mongo.insert_task(insert_mongo)

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
        #判断代理数量，如果小于10则更新代理
        if len(self.proxy_list)<10:
            self.handle_proxy()
        if info['flag'] == 'GET':
            while True:
                try:
                    response = requests.get(url=info['url'],headers=self.header,proxies=self.proxy_list.pop(0),timeout=6)
                except Exception as e:
                    print(e)
                    time.sleep(2)
                    continue
                else:
                    return response.text
        elif info['flag'] == 'POST':
            response = requests.post(url=info['url'],headers=self.header,data=info['data'],proxies=self.proxy_list.pop(0),timeout=6)
            return response.text

    #最新游记处理进程
    def process_1(self):
        t1 = ThreadPoolExecutor()
        for page in range(1,8):
            print(page)
            t1.submit(self.handle_new_article,page)
        t1.shutdown()

    #热门游记处理进程
    def process_2(self):
        t2 = ThreadPoolExecutor()
        for page in range(1,8):
            print(page)
            t2.submit(self.handle_hot_article,page)
        t2.shutdown()
        # self.handle_new_column()
        # self.handle_hot_column()

    def run(self):
        m1 = multiprocessing.Process(target=self.process_1)
        m2 = multiprocessing.Process(target=self.process_2)
        m1.start()
        m2.start()
        m1.join()
        m2.join()

def main():
    mafengwo_task = HandleMaFengWoTask()
    mafengwo_task.run()

if __name__ == '__main__':
    main()
