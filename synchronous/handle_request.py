import requests


class DangdangRequest(object):
    def __init__(self, url, headers, callback, method="GET", need_proxy=False, fail_time=0, timeout=(2, 2)):
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout
        self.headers = headers
        self.url = url
        self.method = method

    def __str__(self):
        return self.url

    def send_request(self):
        print("请求{url}".format(url=self.url))
        proxy_info = {}
        if self.method == "GET":
            try:
                if not self.need_proxy:
                    response = requests.get(url=self.url, headers=self.headers, timeout=self.timeout)
                else:
                    response = requests.get(url=self.url, headers=self.headers, timeout=self.timeout, proxies=proxy_info)
            except:
                return self
            else:
                return response