import multiprocessing


# value = 1
#
#
# def send_data(conn):
#     global value
#     value = value + 1
#     conn.send(value)
#
#
# def receive_data(conn):
#     print("接收到的数据为:{data}".format(data=conn.recv()))
#
#
# def main():
#     # 进程通信管道
#     conn_recv, conn_send = multiprocessing.Pipe()
#     process_send = multiprocessing.Process(target=send_data, args=(conn_send,))
#     process_send.start()
#     process_send.join()
#     process_recv = multiprocessing.Process(target=receive_data, args=(conn_recv,))
#     process_recv.start()
#     process_recv.join()

def worker(list, item):
    list.append("添加值为:{}-{}".format(multiprocessing.current_process().name, item))


def main():
    # 使用manager操作列表共享
    # manager = multiprocessing.Manager()
    # main_item = multiprocessing.current_process().name
    # mgr_list = manager.list([main_item])
    # 不共享
    mgr_list = [multiprocessing.current_process().name]
    print(mgr_list)
    job_process = [multiprocessing.Process(target=worker, args=(mgr_list, item,)) for item in range(3)]
    for job in job_process:
        job.start()

    for end in job_process:
        end.join()
    print(mgr_list)


if __name__ == '__main__':
    main()
