import json
import re
import requests
import time
import multiprocessing
from handle_mysql import lagou_mysql
import random



class HandleLaGou(object):
    def __init__(self):
        self.lagou_session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
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
        for page in range(1,31):
            data = {
                "pn":str(page),
                "kd":"python",
            }
            job_index_url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
            self.handle_request(method='GET',url=job_index_url)
            page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false"%city
            self.header['Referer'] = job_index_url.encode()
            job_result = self.handle_request(method='POST',url=page_url,data=data)
            try:
                lagou_data = json.loads(job_result)
            except:
                continue
            else:
                job_list = lagou_data['content']['positionResult']['result']
                if job_list:
                    for job in job_list:
                        job['crawl_date'] = time.strftime("%Y-%m-%d", time.localtime())
                        lagou_mysql.insert_item(job)
                else:
                    break

    def handle_request(self,method,url,data=None):
        while True:
            proxyinfo = "http://%s:%s@%s:%s" %('H1V32R6470A7G90D','CD217C660A9143C3','http-dyn.abuyun.com','9020')
            proxy = {
                "http": proxyinfo,
                "https": proxyinfo,
            }

            try:
                if method == "GET":
                    response = self.lagou_session.get(url=url,headers=self.header,proxies=proxy,timeout=6)
                elif method == "POST":
                    response = self.lagou_session.post(url=url,headers=self.header,data=data,proxies=proxy,timeout=6)
            except Exception as e:
                print(e)
            else:
                if '您操作太频繁,请稍后再访问' in response.text:
                    print('频繁')
                    self.lagou_session.cookies.clear()
                    # job_index_url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
                    # self.handle_request(method='GET',url=job_index_url)
                    # time.sleep(random.choice(range(3,11)))
                    time.sleep(1)
                    continue
                elif '爬虫行为' in response.text:
                    print('爬虫')
                    self.lagou_session.cookies.clear()
                    time.sleep(1)
                    # time.sleep(random.choice(range(3,11)))
                    continue
                else:
                    return response.text

    def run(self):
        self.handle_city()
        print(self.city_list)
        # for city in self.city_list:
        #     self.handle_city_job(city=city)
        pool = multiprocessing.Pool(2)
        for city in self.city_list:
            pool.apply_async(self.handle_city_job,args=(city,))
        pool.close()
        pool.join()


def main():
    lagou = HandleLaGou()
    lagou.run()

if __name__ == '__main__':
    main()
