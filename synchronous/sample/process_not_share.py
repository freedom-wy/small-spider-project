import multiprocessing
import threading

# 多进程修改值
value = 0
lock = multiprocessing.Lock()


def test1(lock=None):
    global value
    for i in range(1000000):
        # 使用锁解决多线程共享变量时的不安全问题
        lock.acquire()
        value = value + 1
        lock.release()


def multiprocess_value():
    p1 = multiprocessing.Process(target=test1)
    p2 = multiprocessing.Process(target=test1)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def thread_value():
    t1 = threading.Thread(target=test1, args=(lock, ))
    t2 = threading.Thread(target=test1, args=(lock, ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    # 进程与进程之间不共享数据
    # multiprocess_value()
    # print(value)
    # 多线程间共享数据
    thread_value()
    print(value)
