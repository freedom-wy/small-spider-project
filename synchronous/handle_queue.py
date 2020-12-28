import queue
from handle_request import DangdangRequest


class DangdangQueue(object):
    def __init__(self):
        self.queue = queue.Queue()

    def insert_data(self, data):
        print("添加抓取任务: ", data)
        if isinstance(data, DangdangRequest):
            self.queue.put(data)
        return False

    def get_data(self):
        if not self.queue.empty():
            data = self.queue.get()
            print("取出任务：", data)
            return data
        else:
            return False

    def database_empty(self):
        return self.queue.qsize() == 0
