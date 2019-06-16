import json
import re
import requests
import time
import multiprocessing
from handle_mysql import lagou_mysql

class HandleLaGou(object):
    def __init__(self):
        #使用session保存cookie信息
        self.lagou_session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }
        self.city_list = ""

    def handle_request(self,method,url,data=None,info=None):
        '''
        处理请求方法
        :param method: 请求方法
        :param url: 请求url
        :param data: post请求的数据
        :return: 数据入库
        '''
        # 由于代理不稳定，所以使用while循环
        while True:
            # 动态版阿布云代理
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
                # 由于反爬虫造成的continue
                if '频繁' in response.text:
                    print('频繁')
                    # 首先清除当前存在的cookie信息
                    self.lagou_session.cookies.clear()
                    # 重新请求cookie信息,并休眠10秒
                    self.lagou_session.get(
                        url="https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info,
                        headers=self.header)
                    time.sleep(10)
                    continue
                elif '错误网关' in response.text:
                    print('错误网关')
                    time.sleep(1)
                    continue
                elif '页面加载中' in response.text:
                    print('页面加载中')
                    time.sleep(2)
                    continue
                else:
                    return response.text

    def handle_city(self):
        '''
        获取拉勾网岗位信息城市
        :return: 城市列表
        '''
        city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method='GET',url=city_url)
        self.city_list = city_search.findall(city_result)
        #清除cookie
        self.lagou_session.cookies.clear()

    def handle_city_job(self,city):
        '''
        :param city: 城市信息
        :return: 最终岗位数据，存储到Mysql
        '''
        #发出第一个请求，获取cookies信息和页码信息
        first_request_url="https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="%city
        first_response = self.handle_request(method='GET',url=first_request_url)
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page = total_page_search.search(first_response).group(1)
        #由于无岗位信息而return
        except Exception as e:
            return
        else:
            #经过分析，每个地区最多显示30页
            for i in range(1,int(total_page)+1):
                data = {
                    "pn":i,
                    "kd":"python"
                }
                #请求岗位信息时必须带上Referer
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="%city
                self.header["Referer"]=referer_url.encode()
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false"%city
                response = self.handle_request(method='POST',url=page_url,data=data,info=city)
                lagou_data = json.loads(response)
                job_list = lagou_data['content']['positionResult']['result']
                if job_list:
                    for job in job_list:
                        job['crawl_date'] = time.strftime("%Y-%m-%d", time.localtime())
                        lagou_mysql.insert_item(job)

if __name__ == '__main__':
    lagou = HandleLaGou()
    lagou.handle_city()
    print(lagou.city_list)
    pool = multiprocessing.Pool(2)
    for city in lagou.city_list:
        pool.apply_async(lagou.handle_city_job,args=(city,))
    pool.close()
    pool.join()
    # for city in lagou.city_list:
    #     lagou.handle_city_job(city)
