import multiprocessing
import sys
import time


# 继承multiprocessing.Process类
class MyProcess(multiprocessing.Process):
    def __init__(self, name, delay, count):
        # 调用父类方法传入名称
        super().__init__(name=name)
        self.delay = delay
        self.count = count

    # 多进程类具体执行方法
    def run(self) -> None:
        for num in range(self.count):
            print("{process}进程ID:{id},进程名称:{name}".format(process=num, id=multiprocessing.current_process().pid,
                                                          name=multiprocessing.current_process().name))
            time.sleep(self.delay)


def main():
    for item in range(3):
        process = MyProcess(name="item-{id}".format(id=item), delay=1, count=10)
        # 多进程类start方法会调用run方法
        process.start()

    print("进程ID:{id},进程名称:{name}".format(id=multiprocessing.current_process().pid,
                                                  name=multiprocessing.current_process().name))
    print("主进程退出")
    sys.exit(0)


if __name__ == '__main__':
    main()
