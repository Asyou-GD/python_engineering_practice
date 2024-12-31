import argparse
from typing import Any, Dict, Optional
import socket
import re
from multiprocessing import pool,Pool


def multi_process(fun):
    # 创建进程池
    pool = Pool(processes=4)  # 指定进程数为 4
    pool.starmap(fun,[(0,1),(0,1),(0,1)]) #多参数
    pool.map(fun, [0,0,0]) #单参数
    # 关闭进程池
    #于关闭进程池，表示不会再向进程池中添加新的任务。
    # 它告诉进程池："不要再接收新的任务了，但是已经提交的任务仍然会继续执行。"
    pool.close()
    #用于等待所有进程池中的任务执行完成。它阻塞当前主线程，
    # 直到所有子进程（或线程）执行完毕后才继续执行主进程。
    pool.join()

def multi_threadpool(fun, args:list, poolnumber:int = 20):
    """
    :param fun: 传入一个函数对象
    :param args: 传入该函数的参数
    :param poolnumber: 线程个数
    :return: None
    """
    # 创建进程池
    ThreadPool = pool.ThreadPool(processes=poolnumber)  # 指定进程数为 4
    if isinstance(args[0],tuple):
        ThreadPool.starmap(fun, args)  # 多参数
    else:
        ThreadPool.map(fun, args)  # 单参数
    # 关闭进程池
    # 于关闭进程池，表示不会再向进程池中添加新的任务。
    # 它告诉进程池："不要再接收新的任务了，但是已经提交的任务仍然会继续执行。"
    ThreadPool.close()
    # 用于等待所有进程池中的任务执行完成。它阻塞当前主线程，
    # 直到所有子进程（或线程）执行完毕后才继续执行主进程。
    ThreadPool.join()

def connect(ip, port):
    s = socket.socket()
    s.settimeout(3)
    r = s.connect_ex((ip, port))
    if r == 0:
        print(f'端口{port}: 端口开启')
    else:
        print(f'端口{port}: 端口关闭')
    s.close()

def scaner(ip: str = '127.0.0.1', port: Optional[str] = '3310'):
    try:
        port = int(port)
        connect(ip, port)
    except:
        qujian = [p.strip() for p in re.split(r'[-,]',port,flags=re.S)]
        if len(qujian) == 2:
            left, right = int(qujian[0]), int(qujian[1])
            port = [i for i in range(left, right + 1, 1)]
            #多线程 创建参数
            args = [(ip,p) for p in port]
            multi_threadpool(connect,args)
        else:
            port = qujian
            # 多线程 创建参数
            args = [(ip, int(p)) for p in port]
            multi_threadpool(connect, args)




def parse_args():
    parser = argparse.ArgumentParser(description='test')
    """
    位置参数 按照顺序给 -
    选项参数 不用按照顺序给 -- 可选
    """
    parser.add_argument('-p', '--port', required=False, type=str, default=3310,
                        help='Specify the port 单个端口 或者一系列 xxxx - xxxx')
    parser.add_argument('-u', '--user', required=False, type=str, default='guest', help='Specify the user')
    parser.add_argument('-i', '--ip', required=False, type=str, default='127.0.0.1', help='Specify the ip')
    # 将解析结果传递给 Arguments 类
    args = parser.parse_args()
    return args


args = parse_args()
scaner(args.ip, args.port)
#在 Windows 上
#你可以使用命令行工具 netstat 查看开放的端口信息
# netstat -ano
# netstat -ano | findstr :端口号
