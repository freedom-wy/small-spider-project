import redis
from pickle import dumps, loads
from handle_request import DangdangRequest


class RedisQueue(object):
    def __init__(self):
        pool = redis.ConnectionPool(host="192.168.149.129", port=6379)
        self.r = redis.Redis(connection_pool=pool)

    def insert_data(self, data):
        print("添加抓取任务: ", data)
        if isinstance(data, DangdangRequest):
            self.r.rpush("TEST", dumps(data))
        return False

    def get_data(self):
        if self.r.llen("TEST"):
            data = loads(self.r.lpop("TEST"))
            print("取出任务：", data)
            return data
        else:
            return False

    def database_empty(self):
        return self.r.llen("TEST") == 0


if __name__ == '__main__':
    db = RedisQueue()
    start_url = "https://www.baidu.com"
    baidu_request = DangdangRequest(url=start_url, callback="hello", need_proxy=True)
    db.insert_data(data=baidu_request)
    request = db.get_data()
