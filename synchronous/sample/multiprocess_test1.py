from multiprocessing import cpu_count

print("cpu内核数量为:{count}".format(count=cpu_count()))
import multiprocessing
import sys
import time


def worker(delay, count):
    for num in range(count):
        print("{process}进程ID:{id},进程名称:{name}".format(process=num, id=multiprocessing.current_process().pid,
                                                      name=multiprocessing.current_process().name))
        time.sleep(delay)


def main():
    # 创建三个进程
    for item in range(3):
        # 传入参数和进程名称
        process = multiprocessing.Process(target=worker, args=(1, 10,), name="item-{item}".format(item=item))
        process.start()
    print("进程ID:{id},进程名称:{name}".format(id=multiprocessing.current_process().pid, name=multiprocessing.current_process().name))
    # 未设置进程阻塞，主进程即使退出也不会影响子进程执行
    print("主进程退出")
    sys.exit(0)


if __name__ == '__main__':
    main()
