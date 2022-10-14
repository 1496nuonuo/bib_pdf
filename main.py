#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.filedialog as tkfd
from tkinter import *
from tkinter.filedialog import askopenfilename,askdirectory
from download import download_fromto
class Application(Frame):
    def __init__(self, parent=None):    #这里重写Application的父容器Frame，从而让其成为顶级容器
        Frame.__init__(self, parent)    #父容器Frame的parent是TK()，这个是所tkinter的组件的主窗口
        self.pack(expand=YES)           #打包application, tkinter会自动为其画一个矩形框，其所有的子部件将在这个矩形框里布局
                                                        #如果没有这个pack(),所有继承self的子类将都不会出现在主窗口中，表现形式上就是主窗口是个空的。
        self.create_widget()

    def create_widget(self):            #创建组件
        self.lab = Label(self, text='File_Path').grid(row=0, column=0)
        self.ent = Entry(self, width=40)
        self.ent.grid(row=0,column=1)
        self.lab = Label(self, text='Dir_Path').grid(row=1, column=0)
        self.entry0 = Entry(self, width=40)
        self.entry0.grid(row=1, column=1)
        self.button = Button(self, text='Open', command=self.get_file_path).grid(row=0, column=2)
        self.button = Button(self, text='Open', command=self.get_dir_path).grid(row=1, column=2)
        self.button = Button(self, text='submit', command=self.submit).grid(row=2,column=0)

    def get_file_path(self):         #获取文件路径
        self.ent.delete(0, END)      #先清空文件名框内的内容
        self.file_name = askopenfilename(filetypes=[('All Files', '.pdf')])  #弹出文件复选框，选择文件,可以指定文件类型以过滤
        self.ent.insert(END, self.file_name)    #显示文件名，用insert方法把文件名添加进去

    def get_dir_path(self):         #获取文件路径
        self.entry0.delete(0, END)      #先清空文件名框内的内容
        self.dir_name = askdirectory()  #弹出文件复选框，选择文件,可以指定文件类型以过滤
        self.entry0.insert(END, self.dir_name)    #显示文件名，用insert方法把文件名添加进去
    def submit(self):                    #点击提交的时候获取button内回调函数的变量值，这里是文件路径
        self.file_path = self.ent.get()  #用组件Entry的get获取输入框内的字符串，其在组件被销毁前就被取到
        self.dir_path = self.entry0.get()
        download_fromto(self.file_path, self.dir_path)
        finish_var.set('*************************finish*************************')
        #root.destroy()                  #同样是跳出mainloop(),但是这里销毁的是主窗口Tk(),默认情况下它是所有tkinter 组件的父容器
if __name__ == "__main__":
    root = Tk()                             #将主窗口实例化
    app = Application(parent=root)                      #将application实例化
    root.title('DOWNBIB')
    root.geometry('500x300')  # 这里的乘是小x
    finish_var = tk.StringVar()
    f = tk.Label(root, textvariable=finish_var, font=('Arial', 12))
    f.pack()
    app.mainloop()
