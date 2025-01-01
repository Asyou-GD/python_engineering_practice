import json
import threading
import tkinter as tk
from tkinter import filedialog, ttk
import socket
import multiprocessing
import re
import queue

class Request():
    def __init__(self):
        self.headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        }
        
    def requests(self,methor:str,ip, port):
        s = socket.socket()
        s.settimeout(3)
        r = s.connect_ex((ip, int(port)))
        if r == 0:
            return f'ip:{ip}, 端口{port}: 端口开启'
        else:
            return f'ip:{ip}, 端口{port}: 端口关闭'
        s.close()

#tk 对象不能被直接传递到子进程中，因为它们不能被序列化（pickle）。
#self._check() 调用方式错误，导致线程函数被提前调用。
class Window:
    def __init__(self, R: Request):
        """界面初始化"""
        self.R = R
        # 创建进程通信队列
        self.file = ''
        self.result_queue = multiprocessing.Queue()  # 用于与子进程通信的队列
        self.task_queue = multiprocessing.Queue()  #  #存放urls  进程不可传入queue.Queue()

        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.title("目录扫描")

        self.creatui()
        self.configure_grid()
        self.listen_to_data()
        self.help=False
        self.root.mainloop()

    def creatui(self):
        """
        设置 sticky 属性：通过 sticky 来让组件"粘附"到 N/S/E/W 边界（分别代表上、下、右、左）。
        :return:
        """
        # 左部分
        # 第一行
        self.label1 = tk.Label(self.root, text='[请求方法]')
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.v1 = tk.StringVar()
        self.v1.set('http')
        self.radio1 = tk.Radiobutton(self.root, variable=self.v1, value='http', text='http')
        self.radio1.grid(row=0, column=1, )
        self.radio2 = tk.Radiobutton(self.root, variable=self.v1, value='https', text='https')
        self.radio2.grid(row=0, column=2, padx=50)

        # 第二行
        self.label2 = tk.Label(self.root, text='[域  名]')
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry1 = tk.Entry(self.root)
        self.entry1.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # 第三行
        self.label3 = tk.Label(self.root, text='[目录字典]')
        self.label3.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry2 = tk.Entry(self.root)
        self.entry2.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # 右部分
        # 第一行
        self.label4 = tk.Label(self.root, text='[请求方法]')
        self.label4.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.v2 = tk.StringVar()
        self.v2.set('GET')
        self.radio3 = tk.Radiobutton(self.root, variable=self.v2, value='GET', text='GET')
        self.radio3.grid(row=0, column=4)
        self.radio4 = tk.Radiobutton(self.root, variable=self.v2, value='POST', text='POST')
        self.radio4.grid(row=0, column=5, padx=50)

        # 第二行
        self.label5 = tk.Label(self.root, text='[端  口]')
        self.label5.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry3 = tk.Entry(self.root)
        self.entry3.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="ew")

        # 第三行
        style = ttk.Style()
        style.configure('Primary.TButton', 
                       background='blue', 
                       foreground='black',
                       padding=5)
        style.configure('Secondary.TButton', 
                       background='#6c757d',
                       foreground='black',
                       padding=5)
        style.configure('Danger.TButton',
                       background='#dc3545',
                       foreground='black', 
                       padding=5)

        self.button1 = tk.Button(self.root, 
                                    text='浏览',
                                    bg='#BA55D3',  # 背景色
                                    fg='white',    # 文字颜色
                                    relief='flat', # 扁平化效果
                                    padx=10,
                                    pady=5,
                                    command=self.openfile)
        self.button1.grid(row=2, column=3, padx=5, pady=5)
        
        self.button2 = tk.Button(self.root, 
                                    text='开始扫描',
                                    bg='#007bff',
                                    fg='white',
                                    relief='flat',
                                    padx=10,
                                    pady=5,
                                    command=self.start_process)
        self.button2.grid(row=2, column=4, padx=50, pady=5)
        
        self.button3 = tk.Button(self.root, 
                                    text='清除',
                                    bg='#dc3545',
                                    fg='white',
                                    relief='flat',
                                    padx=10,
                                    pady=5,
                                    command=self.delete)
        self.button3.grid(row=2, column=5, pady=5)
        # 下半部分
        self.text1 = tk.Text(self.root)
        self.text1.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

    def configure_grid(self):
        """
        配置行列权重，使组件自动填充窗口
        """
        # 配置行权重
        self.root.grid_rowconfigure(3, weight=1)  # 第 3 行（文本框行）可拉伸

        # 配置列权重
        self.root.grid_columnconfigure(1, weight=1)  # 第 1 列（域名输入框所在列）可拉伸
        self.root.grid_columnconfigure(4, weight=1)  # 第 4 列（端口输入框所在列）可拉伸

    def listen_to_data(self):
        """
        监听数据
        :return:
        """
        try:
            result = self.entry3.get()
            if (result or self.file) and not self.help:
                help = """
Port数据格式
    1. 110-225 范围
    2. 110,55,99,88 逗号隔开
    3. 55 单个

*********json文件的数据应该形式如是**********
[
    {
        "ip":"127.0.0.1",
        "port":"3306"
    }
]                        
"""
                self.help=True
                self.text1.insert(tk.INSERT, help)
            self.text1.see(tk.END)  # 滚动到底部
        except Exception as e:
            print(e)
        finally:
            # 每隔 100 毫秒再次调用自己
            self.root.after(100, self.listen_to_data)

    def delete(self):
        self.text1.delete(1.0, tk.END)
        self.help=False

    def openfile(self):
        """
        文件打开操作，文件路径写入entry
        :return:
        """
        file = filedialog.askopenfilenames(
            defaultextension = "sd",
            title="选择⽂件",
            filetype=[('*.jpg *.png','*.json')]
        )
        self.entry2.insert(0,file[0])
        self.file = file[0]


    def init(self):
        """读取队列里的url，放入队列"""
        with open(self.file, 'r', encoding='utf8') as f:
            urls = json.load(f)

        for url in urls:
            self.task_queue.put((url['ip'].strip(), url['port'].strip()))

    def update_ui(self):
        """更新UI，读取队列中的扫描结果"""
        try:
            while True:
                result = self.result_queue.get_nowait()  # 非阻塞获取队列内容
                self.text1.insert(tk.INSERT, result)
                self.text1.see(tk.END)  # 滚动到末尾
        except queue.Empty:
            self.root.after(100, self.update_ui)

    def start_process(self):
        self.text1.delete(1.0, tk.END)
        #1.0：表示从第一行的第一个字符开始。
        #iINSERT 当前位置
        #END  末尾
        self.help = False
        if (self.entry1.get()=='' or self.entry3.get()=='') and self.entry2.get()=='':
            self.text1.insert(tk.INSERT,'数据为空，请输入域名端口或者目录字典文件！！！\n')
            return

        if self.file:
            self.init()
        if self.entry1.get()!='':
            if self.entry3.get():
                port = self.entry3.get()
                qujian = [p.strip() for p in re.split(r'[-,]', port, flags=re.S)]
                if len(qujian) == 2:
                    left, right = int(qujian[0]), int(qujian[1])
                    port = [i for i in range(left, right + 1, 1)]
                    # 多线程 创建参数
                    [self.task_queue.put((self.entry1.get(), p)) for p in port]
                else:
                    port = qujian
                    # 多线程 创建参数
                    [self.task_queue.put((self.entry1.get(), p)) for p in port]


        process = multiprocessing.Process(target=self.scan_process,
                                          args=(self.task_queue,
                                                self.result_queue,
                                                self.R))
        process.start()


        # 定时更新UI
        self.update_ui()

    @staticmethod
    def check(task_queue,result_queue:multiprocessing.Queue,R):
        """线程任务函数"""
        #self.text1.insert(tk.INSERT,urls)
        while not task_queue.empty():  # 当队列不为空时继续执行
            url, port = task_queue.get()
            res = R.requests('GET',url, port)
            result_queue.put(res+'\n')

    @staticmethod
    def scan_process(task_queue, result_queue, R):
        """子进程中的扫描任务"""
        threads_pool = []
        for i in range(10):
            t = threading.Thread(target=Window.check,args=(task_queue, result_queue, R))  # 指定 worker 函数为线程的任务
            t.start()  # 启动线程
            threads_pool.append(t)  # 将线程添加到线程列表中
        for t in threads_pool:
            t.join()
        # 扫描完成标志
        result_queue.put("扫描完成！\n")


# 界面
# http请求函数
# 线程启动函数
# 线程任务函数
# 文件处理函数
# 初始化操作，字典里的url目录放入队列中
if __name__ == "__main__":
    # 在 Python 程序打包成 exe 时，经常会遇到多进程相关的问题。
    # 主要原因是 multiprocessing 在 Windows 下的 "freeze support" 问题。
    # 添加这一行，可以解决这个问题。
    multiprocessing.freeze_support()  # 添加这一行
    R = Request()
    win = Window(R)
