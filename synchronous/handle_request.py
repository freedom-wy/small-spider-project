import requests
import traceback


class DangdangRequest(object):
    def __init__(self, url, headers, callback, method="GET", need_proxy=False, fail_time=0, timeout=(5, 5)):
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
                    response = requests.get(url=self.url, headers=self.headers, timeout=self.timeout,
                                            proxies=proxy_info)
            except Exception as e:
                print(traceback.format_exc())
                return self
            else:
                return response


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 "
    }
    q = DangdangRequest(url="https://www.baidu.com", headers=headers, callback="hello")
    response = q.send_request()
    print(response.text)
