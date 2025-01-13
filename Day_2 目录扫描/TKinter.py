from tkinter import *

def Simple_window():
    #最简单的窗⼝：
    root = Tk()
    root.mainloop()


def set_title_size():
    #设置title和⼤⼩：
    root = Tk()
    root.geometry('300x200')
    root.title('hello')
    root.mainloop()

#pack布局
#pack() ⽅法是⼀种常⻅的布局⽅式，主要的参数如下 ：
#pad 是左右都有pad
def pack():
    root = Tk()
    # root.geometry('600x600')
    root.geometry()
    root.title("目录扫描")
    Label(root, text='hello', bg='red').\
        pack(side="left", padx=50, pady=100)
    Label(root, text='hello', bg='orange').\
        pack(side="left", padx=50)
    root.mainloop()

#grid()
#⽹格化布局， row代表⾏， column代表列
#推荐大家使用这个
def grid():
    root = Tk()
    root.geometry("300x300")
    laber1 = Label(root, text='laber1', bg='red')
    laber2 = Label(root, text='laber2', bg='blue')
    laber3 = Label(root, text='laber3', bg='orange')
    laber4 = Label(root, text='laber4', bg='purple')
    laber1.grid(column=0, row=0)
    laber2.grid(column=0, row=1)
    laber3.grid(column=1, row=2)
    laber4.grid(column=2, row=3)
    root.mainloop()

#place() ⽅法可以对组件进⾏绝对定位，其参数如下
def place():
    root = Tk()
    laber1 = Label(root, text="laber1", bg="red")
    laber2 = Label(root, text="laber2", bg="blue")
    laber1.place(width="50", height="50", x=20, y=50)
    laber2.place(width="50", height="50", x=20, y=100)
    root.mainloop()

#Label标签组件
def label():
    root = Tk()
    root.geometry('300x200')
    root.title('hello')
    label = Label(root, justify='center', font=8, text='这是label标签').pack(ipadx=
                                                                             10, ipady=10)
    root.mainloop()

#Entry单⾏⽂本框组件
def entry():
    root = Tk()
    root.geometry('200x200')
    laber1 = Label(root, text="⽤户名:")
    laber2 = Label(root, text="密 码:")
    entry1 = Entry(root)
    entry2 = Entry(root, show='*')
    laber1.grid(column=0, row=0)
    laber2.grid(column=0, row=1)
    entry1.grid(column=1, row=0)
    entry2.grid(column=1, row=1)
    root.mainloop()

#Text多⾏⽂本框组件
def text():
    root = Tk()
    text1 = Text(root)
    text1.insert(INSERT, "hello\nworld")
    text1.pack()
    print(text1.get(2.1))
    root.mainloop()


#Button 组件
def button():
    root = Tk()
    entry1 = Entry(root, )

    def f1():
        print(entry1.get())

    btn1 = Button(root, text='点击', command=f1)
    entry1.grid(column=0, row=0)
    btn1.grid(column=1, row=1)
    root.mainloop()

#RadioButton 单选按钮组件
def RadioButton_():
    root = Tk()
    vali = StringVar()
    vali.set('female')   #默认选项
    check1 = Radiobutton(root, variable=vali, text='male', value='male')
    check2 = Radiobutton(root, variable=vali, text='female', value='female')
    #variable参数一样 代表同一个单选框

    def f1():
        print(vali.get())

    btn1 = Button(root, text='点击', command=f1)
    check1.pack()
    check2.pack()
    btn1.pack()
    root.mainloop()
