# 消息队列 任务函数
# 写多任务脚本模板
# 创建100个数字，放⼊消息队列中，设置5个线程去消息队列中取出数据。如果取出尾数为6的数据，就
# 完成任务，脚本结束运⾏

import queue, random
import threading, time

# Q是消息队列、守护线程?
# #这个模板有没有其他结束
#queue.Queue 是 Python 提供的线程安全的消息队列，适合在线程间共享数据。
# 这里你创建了一个消息队列 Q，并用 Q.put(num) 将随机生成的数字放入队列中。
    #线程安全：Queue 自带锁机制，支持多线程访问。
    #FIFO：消息队列按先进先出的顺序取出数据（Q.get())
Q = queue.Queue()
for i in range(100):
    num = random.randint(1000, 10000)
    # 把数字放入队列中
    Q.put(num)


def worker():
    """
    核心逻辑
    worker 是每个线程执行的任务函数。它从队列中取数据并检查是否满足条件（尾数为 6），如果满足，
    则清空队列并结束任务。


    :return:
    """
    while not Q.empty():  # 当队列不为空时继续执行
        num = str(Q.get())  # 从队列中取出一个数字
        print(num)  # 打印数字
        if num[-1] == '6':  # 检查尾数是否是 '6'
            with Q.mutex:  # 加锁以确保队列操作的线程安全
                Q.queue.clear()  # 清空队列，任务结束
        time.sleep(1)  # 模拟随机耗时


if __name__ == '__main__':
    threads = []
    for i in range(5):         # 创建 5 个线程
        t = threading.Thread(target=worker)  # 指定 worker 函数为线程的任务
        # 守护线程
        #守护线程是后台线程，当主线程退出时，守护线程也会随之终止。守护线程的特点是：
            #自动关闭：当主线程结束时，即使守护线程仍在运行，也会强制停止。
            #适用场景：通常用于非关键任务（如日志记录、后台维护任务）。
        #在你的脚本中，设置 t.daemon = True 表示这些线程是守护线程，主线程结束后不再等待它们完成。
            #注意：如果没有设置 daemon=True，主线程会等所有子线程结束后再退出。
        t.daemon = True
        t.start()           # 启动线程
        threads.append(t)   # 将线程添加到线程列表中
    for t in threads:
        t.join()             # 阻塞主线程，直到对应的线程完成
        #虽然设置了 daemon = True，但这里使用了 join()，表明主线程希望等待这些线程完成后再结束。
        #如果没有 join()，主线程在完成后可能会退出，而守护线程将被强制停止（未完成的任务可能丢失）。