import re
import requests
import time



class HandleLaGou(object):
    def __init__(self):
        self.lagou_session = requests.session()
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        }
        self.city_list = ""

    def handle_city(self):
        city_search = re.compile(r'zhaopin/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method='GET',url=city_url)
        self.city_list = city_search.findall(city_result)
        #清除cookie
        self.lagou_session.cookies.clear()

    def handle_city_job(self):
        job_index_url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
        self.handle_request(method='GET',url=job_index_url)
        for city in self.city_list:
            time.sleep(1)
            page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false"%city
            for page in range(1,31):
                data = {
                    "first":"false",
                    "pn":str(page),
                    "kd":"python",
                }
                self.header['Referer'] = job_index_url
                job_result = self.handle_request(method='POST',url=page_url,data=data)
                print(job_result)

    def handle_request(self,method,url,data=None):
        if method == "GET":
            response = self.lagou_session.get(url=url,headers=self.header)
            return response.text
        elif method == "POST":
            response = self.lagou_session.post(url=url,headers=self.header,data=data)
            return response.text

    def run(self):
        self.handle_city()
        self.handle_city_job()

def main():
    lagou = HandleLaGou()
    lagou.run()

if __name__ == '__main__':
    main()
