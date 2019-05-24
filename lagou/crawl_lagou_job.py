import re
import requests
from lxml import etree



class HandleLaGou(object):
    def __init__(self):
        self.lagou_session = requests.session()
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        }
        self.city_list = ""

    def handle_city(self):
        city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method='GET',url=city_url)
        self.city_list = city_search.findall(city_result)

    def handle_city_job(self):
        for city in self.city_list:
            job_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false"%city
            for page in range(1,31):
                data = {
                    "first":"false",
                    "pn":page,
                    "kd":"python",
                }
                # self.header['Referer'] = "https://www.lagou.com/jobs/list_python?city=%s"%city
                self.header['Referer'] = "https://www.lagou.com/jobs/list_python?city=%e5%8d%97%e4%ba%ac"
                job_result = self.handle_request(method='POST',url=job_url,data=data)
                print(job_result)
                break
            break

    def handle_request(self,method,url,data=None):
        if method == "GET":
            response = self.lagou_session.get(url=url,headers=self.header)
            return response.text
        elif method == "POST":
            print(data)
            response = self.lagou_session.post(url=url,headers=self.header,data=data)
            print(response.request.headers)
            return response.text

    def run(self):
        self.handle_city()
        self.handle_city_job()

def main():
    lagou = HandleLaGou()
    lagou.run()

if __name__ == '__main__':
    main()
