import tkinter
from tkinter import filedialog
from tkinter import ttk


#askopenfilename() 与 askopenfilenames() 都可以选择⽂件，
# 前者只能选择⼀个⽂件，后者可以同时 选择多个⽂件。

def a():
    # 打开⽂件会话框，其返回值为⼀个元组形式的⽂件名
    file = filedialog.askopenfilenames(
        title="选择⽂件",
        filetype=[('jpg图⽚', '*.jpg *.png')]
    )


win = tkinter.Tk()
win.title("显示所选⽂件的信息")
tkinter.Button(win, text="选择", command=a).pack(pady=5)  # 添加按钮
win.mainloop()
