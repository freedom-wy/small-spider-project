import re
from lxml import etree
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


class Crawl_kolesa(object):
    def __init__(self):
        #首页URL
        self.index_url = "https://kolesa.kz/cars/"
        self.header = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Host":"kolesa.kz",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        }
        self.brand_list_url = ""

    #处理请求方法
    def handle_request(self,url):
        response = requests.get(url=url,headers=self.header)
        return response.text

    #处理品牌方法
    def handle_brand(self):
        response = self.handle_request(url=self.index_url)
        html = etree.HTML(response)
        #解析品牌列表
        self.brand_list_url = html.xpath("//div[@class='cross-links'][2]/div[@class='cross-links-container']/ul[@class='col-sm-4 cross-links-list']/li/a/@href")

    #解析品牌筛选条件下的页码页
    def handle_brand_page(self,url):
        detail_info_search = re.compile(r"listing.items.push\((.*?)\);")
        #网站仅显示1000页
        for page in range(1,1001):
            #https://kolesa.kz/cars/gaz/?sort_by=add_date-asc&page=2
            #构造品牌页码URL
            brand_url = "https://kolesa.kz%s?sort_by=add_date-asc&page=%s"%(url,page)
            print(brand_url)
            #请求品牌页码页
            response = self.handle_request(url=brand_url)
            #每页的详情数据
            detail_list = detail_info_search.findall(response)
            if detail_list:
                for detail in detail_list:
                    detail = json.loads(detail)
                    detail_info = {}
                    detail_info['car_name'] = detail.get("name",None)
                    detail_info['id'] = detail.get("id",None)
                    detail_info['car_model'] = detail['attributes']['model']
                    detail_info['car_brand'] = detail['attributes']['brand']
                    detail_info['price'] = detail.get("unitPrice",None)
                    detail_info['from_url'] = detail.get("url",None)
                    print(detail_info)
                    #对接mongo

    #处理详情页
    def handle_detail(self,item):
        response = self.handle_request(item['from_url'])
        html = etree.HTML(response)
        item['year'] = html.xpath("//span[@class='year']/text()")[0].strip()
        item_list = html.xpath("//div[@class='offer__parameters']/dl")
        for i in item_list:
            name = i.xpath("./dt/span/text()")[0]
            if name == "Пробег":
                item['mileage'] = i.xpath("./dd/text()")[0].strip()
            elif name == "Коробка передач":
                item['Gearbox'] = i.xpath("./dd/text()")[0].strip()
            elif name == "Руль":
                item['Steering_wheel'] = i.xpath("./dd/text()")[0].strip()
        print(item)

    #处理任务方法
    def handle_task(self):
        self.handle_brand()
        print("处理品牌")
        t = ThreadPoolExecutor()
        thread_list = []
        for url in self.brand_list_url:
            thread = t.submit(self.handle_brand_page,url)
            thread_list.append(thread)
        t.shutdown()

    #爬虫启动方法
    def run(self):
        m1 = multiprocessing.Process(target=self.handle_task)
        m1.start()
        m1.join()





if __name__ == '__main__':
    kolesa = Crawl_kolesa()
    kolesa.run()
