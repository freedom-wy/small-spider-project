import multiprocessing
import time


def send(msg):
    time.sleep(5)
    print("进程ID:{id},进程名称:{name},发送消息:{msg}".format(id=multiprocessing.current_process().pid,
                                                    name=multiprocessing.current_process().name, msg=msg))


def main():
    process = multiprocessing.Process(target=send, name="TEST", args=("发送消息测试",))
    process.start()
    # 阻塞主进程执行，将等待子进程执行完毕后再执行主进程
    # process.join()
    time.sleep(2)
    print("进程ID:{id},进程名称:{name}".format(id=multiprocessing.current_process().pid,
                                         name=multiprocessing.current_process().name))
    # 中断进程前判断进程是否存活
    if process.is_alive():
        # 中断进程
        process.terminate()
        print("进程被中断:{name}".format(name=process.name))


if __name__ == '__main__':
    main()
