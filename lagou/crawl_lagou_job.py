import json
import re
import requests
import time
import multiprocessing
from lagou.handle_mongo import lagou_mongo
import random



class HandleLaGou(object):
    def __init__(self):
        self.lagou_session = requests.session()
        self.header = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Referer': 'https://www.lagou.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        }
        self.city_list = ""

    def handle_city(self):
        city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method='GET',url=city_url)
        self.city_list = city_search.findall(city_result)
        #清除cookie
        self.lagou_session.cookies.clear()

    def handle_city_job(self,city):
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
            lagou_data = json.loads(job_result)
            job_list = lagou_data['content']['positionResult']['result']
            if job_list:
                for job in job_list:
                    lagou_mongo.handle_save_data(job)
                time.sleep(10)
            else:
                break

    def handle_request(self,method,url,data=None):
        while True:
            # proxy="http://HTK32673HL02BK2D:50125D2D38937C94@http-dyn.abuyun.com:9020"
            # proxies = {
            #     "http":proxy,
            #     "https":proxy
            # }
            try:
                if method == "GET":
                    # response = self.lagou_session.get(url=url,headers=self.header,proxies=proxies)
                    response = self.lagou_session.get(url=url,headers=self.header)
                elif method == "POST":
                    # response = self.lagou_session.post(url=url,headers=self.header,data=data,proxies=proxies,timeout=3)
                    response = self.lagou_session.post(url=url,headers=self.header,data=data)
            except Exception as e:
                print(e)
                continue
            else:
                if '您操作太频繁,请稍后再访问' in response.text:
                    print('频繁')
                    time.sleep(random.choice(range(10,13)))
                    continue
                elif '爬虫行为' in response.text:
                    print('爬虫')
                    time.sleep(random.choice(range(10,13)))
                    continue
                else:
                    return response.text

    def run(self):
        self.handle_city()
        print(self.city_list)
        pool = multiprocessing.Pool()
        for city in self.city_list:
            pool.apply_async(self.handle_city_job,args=(city,))
        pool.close()
        pool.join()


def main():
    lagou = HandleLaGou()
    lagou.run()

if __name__ == '__main__':
    main()
