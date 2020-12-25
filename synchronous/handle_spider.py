from handle_redis import RedisQueue
from handle_request import DangdangRequest
from lxml import etree


class Spider(object):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.75 Safari/537.36 "
    }

    queue = RedisQueue()

    def start(self):
        """爬虫起始方法"""
        for page in range(1, 26):
            start_url = "http://bang.dangdang.com/books/fivestars/2-{page}".format(page=page)
            dangdang_request = DangdangRequest(url=start_url, callback=self.parse_item, headers=Spider.headers)
            Spider.queue.insert_data(data=dangdang_request)

    def do_request(self, request):
        """发送请求"""
        response = request.send_request()
        return response

    def parse_item(self, response):
        """解析数据"""
        data = []
        html = etree.HTML(response.text)
        items = html.xpath("//ul[@class='bang_list']/li")
        for item in items:
            title = item.xpath(".//div[@class='name']/a/text()")
            if title:
                data.extend(title)
        yield data

    def error(self, request):
        """请求错误后返回队列"""
        request.fail_time = request.fail_time + 1
        if request.fail_time < 20:
            print("该请求异常{url}, 将该请求放回队列".format(url=request))
            Spider.queue.insert_data(data=request)

    def schedule(self):
        """任务调度"""
        while not Spider.queue.database_empty():
            dangdang_request = self.queue.get_data()
            if dangdang_request:
                print("当前调度：", dangdang_request)
                callback = dangdang_request.callback
                response = self.do_request(dangdang_request)
                if not isinstance(response, DangdangRequest):
                    # 通过回调方法解析
                    result = callback(response)
                    for item in result:
                        print(item)
                else:
                    dangdang_request = DangdangRequest(url=response.url, headers=Spider.headers, callback=self.parse_item)
                    # 错误处理
                    self.error(dangdang_request)

    def run(self):
        self.start()
        self.schedule()


if __name__ == '__main__':
    s = Spider()
    s.run()
