import multiprocessing
import random
import time

value = 2
# test_list = [11, 22]


def test1():
    global value
    test_value = random.randint(1, 11)
    print("{process_name}输入的值为:{test_value}".format(process_name=multiprocessing.current_process().name, test_value=test_value))
    value = value * test_value
    time.sleep(random.randint(1, 5))
    print(multiprocessing.current_process().name, value)
    # test_list.append(33)


def test2():
    # print("test2", test_list)
    print("test2", value)


if __name__ == '__main__':
    # 进程与进程之间不共享数据
    # pool = multiprocessing.Pool(processes=2)
    # for i in range(10):
    #     pool.apply_async(func=test1)
    # pool.close()
    # pool.join()
    # p1 = multiprocessing.Process(target=test1)
    # p2 = multiprocessing.Process(target=test2)
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    test1()
    test2()
