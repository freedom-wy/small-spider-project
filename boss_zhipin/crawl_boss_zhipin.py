from urllib.parse import urljoin
import requests
import pymongo
from pymongo.collection import Collection
import time
import json
from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor



class HandleBossZhiPin(object):
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        }
        self.city_list = ""
        boss_client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.boss_db = boss_client['boss']
        self.city_list = []

    def handle_city(self):
        city_api_url = "https://www.zhipin.com/wapi/zpCommon/data/city.json"
        city_response = self.handle_request(method='GET',url=city_api_url)
        for province in json.loads(city_response)['zpData']['cityList']:
            for city in province['subLevelModelList']:
                self.city_list.append(city)

    def handle_job_request(self,job,city):
        print(city['name'])
        for page in range(1,11):
            job_url = "https://www.zhipin.com/c%s/?query=%s&page=%s"%(city['code'],job,page)
            print(job_url)
            response = self.handle_request(method='GET',url=job_url)
            html = etree.HTML(response)
            job_list = html.xpath("//div[@class='job-list']/ul/li")
            for item in job_list:
                info = {}
                info['job_title'] = item.xpath(".//div[@class='job-title']/text()")[0]
                if '实习' in info['job_title']:
                    continue
                info['price'] = item.xpath(".//span[@class='red']/text()")[0]
                describe_1 = item.xpath(".//div[@class='info-primary']/p/text()")
                if len(describe_1) == 3:
                    info['location'] = describe_1[0]
                    info['working_life'] = describe_1[1]
                    info['education'] = describe_1[2]
                info['company_name'] = item.xpath(".//div[@class='info-company']//h3[@class='name']/a/text()")[0]
                describe_2 = item.xpath(".//div[@class='info-company']//p/text()")
                info['company_type'] = describe_2[0]
                info['job_id'] = urljoin("https://www.zhipin.com",item.xpath(".//h3/a/@href")[0])
                info['city'] = city['name']
                self.handle_save_data(item=info)
            if not html.xpath("//div[@class='page']/a[@class='next']"):
                break


    def handle_job_detail(self,response):
        pass

    def handle_save_data(self,item):
        boss_collection = Collection(self.boss_db, "boss_data")
        boss_collection.update({"job_id": item['job_id']}, item, True)

    def handle_request(self,method,url,data=None):
        while True:
            proxy="http://HTK32673HL02BK2D:50125D2D38937C94@http-dyn.abuyun.com:9020"
            proxies = {
                "http":proxy,
                "https":proxy
            }
            try:
                if method == "GET":
                    response = requests.get(url=url,headers=self.header,proxies=proxies)
                elif method == "POST":
                    response = requests.post(url=url,headers=self.header,data=data,proxies=proxies,timeout=3)
            except Exception as e:
                print(e)
                time.sleep(2)
                continue
            else:
                return response.text

    def run(self):
        self.handle_city()
        t = ThreadPoolExecutor(max_workers=3)
        for city in self.city_list:
            t.submit(self.handle_job_request(job='python',city=city))
        t.shutdown()

def main():
    boss = HandleBossZhiPin()
    boss.run()

if __name__ == '__main__':
    main()
