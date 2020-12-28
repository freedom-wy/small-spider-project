import multiprocessing
import time


def work(item):
    time.sleep(0.05)
    return "进程ID:{id},进程名称{name},执行任务item:{item}".format(id=multiprocessing.current_process().pid,
                                                         name=multiprocessing.current_process().name, item=item)


def main():
    # 进程池大小为4
    pool = multiprocessing.Pool(processes=4)
    for item in range(100):
        result = pool.apply_async(func=work, args=(item,))
        print(result.get())
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
