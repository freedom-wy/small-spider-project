import _thread
import threading
import time


def _thread_handle(thread_name, delay):
    for num in range(10):
        time.sleep(delay)
        print("{}的num:{}".format(thread_name, num))


def threading_handle(delay=1):
    for num in range(10):
        time.sleep(delay)
        print("{}-num-{}".format(threading.current_thread().name, num))


def main():
    # for item in range(10):
    #     _thread.start_new_thread(_thread_handle, ("Thread - {}".format(item), 1))
    # # 和进程不同，如果进程死亡，则线程也会死亡
    # time.sleep(200)
    for item in range(10):
        # thread = threading.Thread(target=threading_handle, args=(1,), name="执行线程-{}".format(item))
        thread = threading.Thread(target=threading_handle, args=(1,))
        thread.start()


if __name__ == '__main__':
    main()
