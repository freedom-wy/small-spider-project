import time
import multiprocessing


def status():
    """守护进程方法"""
    while True:
        print("守护进程ID:{id},守护进程名称:{name}".format(id=multiprocessing.current_process().pid,
                                                 name=multiprocessing.current_process().name))
        time.sleep(1)


def worker():
    """具体执行工作的方法"""
    # 创建守护进程,daemon为TRUE
    daemon_process = multiprocessing.Process(target=status, name="守护进程", daemon=True)
    daemon_process.start()
    for item in range(10):
        print("进程ID:{id},进程名称:{name}".format(id=multiprocessing.current_process().pid, name=multiprocessing.current_process().name))
        time.sleep(2)


def main():
    process = multiprocessing.Process(target=worker, name="工作进程")
    process.start()


if __name__ == '__main__':
    main()
