# 消息队列 任务函数
# 写多任务脚本模板
# 创建100个数字，放⼊消息队列中，设置5个线程去消息队列中取出数据。如果取出尾数为6的数据，就
# 完成任务，脚本结束运⾏

import queue, random
import threading, time

# Q是消息队列、守护线程?
# #这个模板有没有其他结束
Q = queue.Queue()
for i in range(100):
    num = random.randint(1000, 10000)
    # 把数字放入队列中
    Q.put(num)


def worker():
    while not Q.empty():
        num = str(Q.get())
        print(num)
        if num[-1] == '6':
            with Q.mutex:
                Q.queue.clear()
        time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker)
        # 守护线程
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
