import multiprocessing
import time

value = 1


def send_data(conn):
    global value
    value = value + 1
    conn.send(value)


def receive_data(conn):
    print("接收到的数据为:{data}".format(data=conn.recv()))


def pipe_main():
    # 进程通信管道
    conn_recv, conn_send = multiprocessing.Pipe()
    process_send = multiprocessing.Process(target=send_data, args=(conn_send,))
    process_send.start()
    process_send.join()
    process_recv = multiprocessing.Process(target=receive_data, args=(conn_recv,))
    process_recv.start()
    process_recv.join()


def worker(dict, lock):
    while True:
        # lock.acquire()
        with lock:
            number = dict.get("ticket")
            if number > 0:
                time.sleep(1)
                number = number - 1
                print("{}-ticket={}".format(multiprocessing.current_process().name, number))
                dict.update({"ticket": number})
            else:
                print("无票")
                break
        # lock.release()


def main():
    # 使用manager操作字典共享
    manager = multiprocessing.Manager()
    mgr_dict = manager.dict(ticket=5)
    lock = multiprocessing.Lock()
    print(mgr_dict)
    job_process = [multiprocessing.Process(target=worker, args=(mgr_dict, lock,), name="售票员-{item}".format(item=item))
                   for item in range(3)]
    for job in job_process:
        job.start()

    for end in job_process:
        end.join()


if __name__ == '__main__':
    # pipe_main()
    main()
