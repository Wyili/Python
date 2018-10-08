#coding:utf-8
'''
author:Wyili
version:Python 3.7.0
date:2018/10/1
'''
import re
import os
import sys
import time
import urllib.request
from tkinter import *
from tkinter import ttk
import threading
from tkinter.filedialog import askdirectory

#### 获取网页源码
def getHtml(url):
	page = urllib.request.urlopen(url)
	html = page.read().decode('utf-8')	 #需要解码
	return html
	
#### 下载图片
def getImage(html):
	global num,x,pin
	#### 获取HTML源码里面的app.page["pins"]部分，主要图片ID位于此部分
	app_page_pins_re = re.compile(r'app\.page\["pins"\](.*?);',re.S)
	app_page_pins_str = re.findall(app_page_pins_re,html)[0]
	#### 获取图片ID，保存在列表中
	pin_id_re = re.compile(r'"pin_id":(\d+)')
	pin_id_list = re.findall(pin_id_re,app_page_pins_str)
	x += 1
	if x >= pin:
		for pin_id in pin_id_list:
			#### 获取跳转网页网址
			url_str = r'http://huaban.com/pins/%s/' % pin_id
			#### 获取点击图片时弹出网页的源码
			pin_id_source = getHtml(url_str)
			#### 解析源码，获取原图片的网址
			img_url_re = re.compile('main-image.*?src="(.*?)"',re.S)
			img_url_list = re.findall(img_url_re,pin_id_source)
			try:
				img_url = 'http:' + img_url_list[0]
				#### 获取原图片的网址，以_fw658结尾的链接并不是原图片的链接，需要把_fw658去掉
				if '_fw658' in img_url:
					img_url = img_url[:-6]
				name = '%s__%s' %(e1.get(),num)
				urllib.request.urlretrieve(img_url,'{}{}.jpg'.format(paths,name))
			except:
				text.insert(END,"\n获取图片：%s失败，跳过，获取下一张。\n" % img_url)
				text.see(END)
				continue
			text.insert(END,"\n图片《%s》：%s获取成功！\n" % (name,img_url))
			text.see(END)
			if num == end_num:
				text.insert(END,"\n.....图片保存成功！.....\n")
				text.see(END)
				exit()		
			num += 1
			global fun_1,fun_2
			if fun_2 == 1:
				text.insert(END,'\n.....已暂停...请按“暂停/继续”按钮继续.....\n')
				text.see(END)
			while fun_2 == 1:
				if fun_1 == 0:
					break
			if fun_1 == 0:
				break
	return pin_id_list[-1]

def handle(url,first_num,all_num,path):
	global num,end_num,paths,x,fun_1,flag
	x = 0
	num = first_num
	end_num = first_num + all_num -1
	if not os.path.isdir(path):     #如果该路径下不存在path所指文件夹，则创建
		os.makedirs(path)
	paths = path+'\\'	  #保存到path所指的文件夹下
	html = getHtml(url)
	new_id = getImage(html)
	while fun_1 == 1:
		url = url+"/?&max=" + str(new_id) + '&limit=' + str(20) + '&wfl=1';
		html = getHtml(url)
		new_id = getImage(html)
	text.insert(END,'\n\n*****图片已结束下载！*****\n\n')
	text.see(END)
	flag = 1

def main():
	text.insert(END,'\n\n*****"%s"图片开始下载！*****\n\n' % e1.get())
	text.see(END)
	if e1.get() == '美女':
		url = "http://huaban.com/favorite/beauty/" 
	elif e1.get() == '儿童':
		url = "http://huaban.com/favorite/kids/"
	elif e1.get() == '美食':
		url = "http://huaban.com/favorite/food_drink/"
	elif e1.get() == '明星':
		url = "http://huaban.com/favorite/people/"
	elif e1.get() == '美图':
		url = "http://huaban.com/favorite/quotes/"
	elif e1.get() == '旅行':
		url = "http://huaban.com/favorite/travel_places/"
	global pin
	pin = int(e2.get())               #从第几个pins包开始下载图片
	first_num = int(e3.get())		#命名第一张图片
	all_num = int(e4.get())		  #下载图片的数量
	path = e5.get()    #选择本地保存图片的路径
	handle(url,first_num,all_num,path)
	
def stop_run():
	global fun_2
	if fun_2 == 0:
		fun_2 = 1
	else:
		fun_2 = 0

def fun():
	th = threading.Thread(target = fun1)
	th.setDaemon(True)
	th.start()

global flag,flag2
flag = 0
flag2 = 0
def fun1():
	global fun_1,fun_2,flag,flag2
	fun_1 = 0
	while flag == 0 and flag2 == 1:
		time.sleep(0.5)
	if flag == 1 or flag2 == 0:
		flag = 0
		flag2 = 1
		fun_1 = 1
		fun_2 = 0
		th1 = threading.Thread(target = main)
		th1.setDaemon(True)
		th1.start()

def fun2():
	global fun_1
	if fun_1 == 1:
		th2 = threading.Thread(target = stop_run)
		th2.setDaemon(True)
		th2.start()

def fun3():
	sys.exit()
	
def selectPath():
    path_ = askdirectory()
    v5.set(path_)
	
root = Tk(className = "花瓣网图片下载工具 by Wyili")

FM = Frame(root)
fm_l = Frame(FM)
fm_r = Frame(FM)
fm1 = Frame(fm_l)
fm2 = Frame(fm_l)
fm3 = Frame(fm_l)
fm4 = Frame(fm_l)
fm5 = Frame(fm_l)
fm6 = Frame(fm_l)

Label(fm1,text='图片类别：',font = 35).pack(side=LEFT, anchor=W, fill=X, pady = 15)
v1 = StringVar()
e1 = ttk.Combobox(fm1, textvariable=v1,font = 35,width=15)
e1["values"] = ('美女', '儿童','明星','美食','旅行','美图')
e1["state"] = "readonly"
e1.current(0)

Label(fm2,text='起始节点：',font = 35).pack(side=LEFT, anchor=W, fill=X)
v2 = StringVar()
e2 = Entry(fm2,textvariable=v2,font = 35,width=35)

Label(fm3,text='起始命名：',font = 35).pack(side=LEFT, anchor=W, fill=X)
v3 = StringVar()
e3 = Entry(fm3,textvariable=v3,font = 35,width=35)

Label(fm4,text='下载数量：',font = 35).pack(side=LEFT, anchor=W, fill=X)
v4 = StringVar()
e4 = Entry(fm4,textvariable=v4,font = 35,width=35)

Label(fm5,text='下载路径：',font = 35).pack(side=LEFT, anchor=W, fill=X)
v5 = StringVar()
e5 = Entry(fm5,textvariable=v5,font = 35,width=25)
e6 = Button(fm5,text = "路径选择", command = selectPath,font = 35)

e1.pack(side=LEFT, anchor=W, fill=X, expand=YES,ipady=1.5)
e2.pack(side=LEFT, anchor=W, fill=X, expand=YES,ipady=3)
e3.pack(side=LEFT, anchor=W, fill=X, expand=YES,ipady=3)
e4.pack(side=LEFT, anchor=W, fill=X, expand=YES,ipady=3)
e5.pack(side=LEFT, anchor=W, fill=X, expand=YES,ipady=3)
e6.pack(side=LEFT, anchor=W, fill=X, expand=YES)

e2.insert(END,'1')
e3.insert(END,'1')
e4.insert(END,'20')
e5.insert(END,'C:\\Users\\Wyili\\Desktop\\HUABAN')

Button(fm6,text='下载',command=fun,font = 35).pack(side=LEFT, anchor=W, fill=X, expand=YES)
Button(fm6,text='暂停/继续',command=fun2,font = 35).pack(side=LEFT, anchor=W, fill=X, expand=YES)
Button(fm6,text='退出',command=fun3,font = 35).pack(side=LEFT, anchor=W, fill=X, expand=YES)

s1 = Scrollbar(fm_r)
s1.pack(side = RIGHT, fill = Y)
s2 = Scrollbar(fm_r, orient = HORIZONTAL)
s2.pack(side = BOTTOM, fill = X)
text = Text(fm_r,yscrollcommand = s1.set, xscrollcommand = s2.set, wrap = 'none',font = 35)
text.pack(side=RIGHT, expand = YES,fill = BOTH)
s1.config(command = text.yview)
s2.config(command = text.xview)

fm1.pack(side=TOP, fill=BOTH, expand=YES,pady=5)
fm2.pack(side=TOP, fill=BOTH, expand=YES,pady=10)
fm3.pack(side=TOP, fill=BOTH, expand=YES,pady=10)
fm4.pack(side=TOP, fill=BOTH, expand=YES,pady=10)
fm5.pack(side=TOP, fill=BOTH, expand=YES,pady=10)
fm6.pack(side=TOP, fill=BOTH, expand=YES,pady=10)
fm_l.pack(side=LEFT, fill=BOTH, expand=YES,padx=10)
fm_r.pack(side=RIGHT, fill=BOTH, expand=YES)
FM.pack(side=LEFT, fill=BOTH, expand=YES)


import win32api, win32gui                #隐藏DOS窗口，仅在windows平台使用
ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0,ct)
win32gui.ShowWindow(hd,0)

root.mainloop()