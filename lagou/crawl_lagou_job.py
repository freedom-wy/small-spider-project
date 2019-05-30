import json
import random
import re
import requests
import time
import pymongo
from pymongo.collection import Collection



class HandleLaGou(object):
    def __init__(self):
        self.lagou_session = requests.session()
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        }
        self.city_list = ""
        lagou_client = pymongo.MongoClient(host="127.0.0.1",port=27017)
        self.lagou_db = lagou_client['lagou']

    def handle_city(self):
        city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method='GET',url=city_url)
        self.city_list = city_search.findall(city_result)
        #清除cookie
        self.lagou_session.cookies.clear()

    def handle_city_job(self,city):
        print(city)
        job_index_url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
        self.handle_request(method='GET',url=job_index_url)
        page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false"%city
        for page in range(1,31):
            data = {
                "first":"false",
                "pn":str(page),
                "kd":"python",
            }
            self.header['Referer'] = job_index_url
            job_result = self.handle_request(method='POST',url=page_url,data=data)
            self.handle_data(job_result)

    def handle_data(self,data):
        lagou_data = json.loads(data)
        job_list = lagou_data['content']['positionResult']['result']
        for job in job_list:
            self.handle_save_data(job)

    def handle_request(self,method,url,data=None):
        while True:
            proxy="http://HTK32673HL02BK2D:50125D2D38937C94@http-dyn.abuyun.com:9020"
            proxies = {
                "http":proxy,
                "https":proxy
            }
            try:
                if method == "GET":
                    response = self.lagou_session.get(url=url,headers=self.header,proxies=proxies)
                elif method == "POST":
                    response = self.lagou_session.post(url=url,headers=self.header,data=data,proxies=proxies,timeout=3)
                    # response = self.lagou_session.post(url=url,headers=self.header,data=data)
            except Exception as e:
                print(e)
                continue
            else:
                if '您操作太频繁,请稍后再访问' in response.text:
                    print('频繁')
                    time.sleep(random.choice(range(5,16)))
                    continue
                elif '爬虫行为' in response.text:
                    print('爬虫')
                    time.sleep(random.choice(range(5,16)))
                    continue
                else:
                    return response.text

    def handle_save_data(self,item):
        lagou_collection = Collection(self.lagou_db,"lagou_data")
        lagou_collection.update({"positionId":item['positionId']},item,True)

    def run(self):
        self.handle_city()
        print(self.city_list)
        for city in self.city_list:
            self.handle_city_job(city=city)


def main():
    lagou = HandleLaGou()
    lagou.run()

if __name__ == '__main__':
    main()
