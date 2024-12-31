import tkinter
import queue
from tkinter import filedialog

def a():
    import queue
    import random
    Q = queue.Queue()
    for i in range(100):
        num = random.randint(1000, 10000)
        # 把数字放入队列中
        Q.put(num)
    print(Q.get())


class Request():
    def __init__(self):
        pass


class Window:
    def __init__(self, R: Request):
        """界面初始化"""
        self.R = R
        self.root = tkinter.Tk()
        self.root.geometry("600x300")
        self.root.title("目录扫描")

        self.creatui()
        self.root.mainloop()

    def creatui(self):
        # 左部分
        # 第一行
        self.lable1 = tkinter.Label(self.root, text='[请求方法]')
        self.lable1.grid(row=0, column=0)

        self.v1 = tkinter.StringVar()
        self.v1.set('http')
        self.radio1 = tkinter.Radiobutton(self.root, variable=self.v1, value='http', text='http').grid(row=0, column=1)
        self.radio2 = tkinter.Radiobutton(self.root, variable=self.v1, value='https', text='https').grid(row=0,
                                                                                                         column=2)

        # 第二行
        self.lable2 = tkinter.Label(self.root, text='[域  名]').grid(row=1, column=0)
        self.entry1 = tkinter.Entry(self.root, show='*').grid(row=1, column=1, columnspan=2)
        # 第三行
        self.lable3 = tkinter.Label(self.root, text='[目录字典]').grid(row=2, column=0)
        self.entry2 = tkinter.Entry(self.root, show='*').grid(row=2, column=1, columnspan=2)

        # 右部分
        # 第一行
        self.lable4 = tkinter.Label(self.root, text='[请求方法]').grid(row=0, column=3)
        self.v2 = tkinter.StringVar()
        self.v2.set('http')
        self.radio3 = tkinter.Radiobutton(self.root, variable=self.v2, value='http', text='http').grid(row=0, column=4)
        self.radio4 = tkinter.Radiobutton(self.root, variable=self.v2, value='https', text='https').grid(row=0,
                                                                                                         column=5)
        # 第二行
        self.lable4 = tkinter.Label(self.root, text='[端  口]').grid(row=1, column=3)
        self.entry3 = tkinter.Entry(self.root, show='*').grid(row=1, column=4, columnspan=2)
        # 第三行
        self.button1 = tkinter.Button(self.root, text='浏览', command=self.openfile).grid(row=2, column=3)
        self.button2 = tkinter.Button(self.root, text='开始扫描', command=self.scan).grid(row=2, column=5)

        # 下半部分
        self.text1 = tkinter.Text(self.root).grid(row=3, column=0, columnspan=6)

    def openfile(self):
        self.file = filedialog.askopenfilenames(
            defaultextension = "sd",
            title="选择⽂件",
            filetype=[('jpg图⽚', '*.jpg *.png')]
        )

    def scan(self):
        pass

    def init(self):
        """读取队列里的url，放入队列"""

    def _check(self):
        """线程函数
        """
        pass

    def start(self):
        """启动线程"""
        pass


# 界面
# http请求函数
# 线程启动函数
# 线程任务函数
# 文件处理函数
# 初始化操作，字典里的url目录放入队列中
R = Request()
win = Window(R)
