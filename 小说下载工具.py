#coding:utf-8
'''
author:Wyili
version:Python 3.7.0
date:2018/10/1
'''
import re
import time
import os
import sys
import urllib.request
from urllib.parse import quote
from tkinter import *
from tkinter import ttk
import threading

global code
code = 'utf-8'
def website(url):
	global code
	if url  == 'www.qu.la':
		code = 'utf-8'
		s_book_url_f = r"https://sou.xanbhx.com/search?siteid=qula&q="
		s_book_re = '<span class="s2"><a href="(.*?)" target="_blank">\r\n                            (.*?)</a>'
		book_re = '<dd> <a style="" href="/book/.*?/(.*?).html">(.*?)</a></dd>'
		chap_re = '<div id="content">(.*?)<script>'
	elif url == 'www.xxbiquge.com':
		code = 'utf-8'
		s_book_url_f = r"https://www.xxbiquge.com/search.php?keyword="
		s_book_re = '<h3 class="result-item-title result-game-item-title">.*?href="(.*?)" title="(.*?)"'
		book_re = '<dd><a href="/.*?/(.*?).html.*?">(.*?)</a></dd>'
		chap_re = '<div id="content">(.*?)</div>'
	elif url == 'www.x23us.la':
		code = 'utf-8'
		s_book_url_f = r"https://sou.xanbhx.com/search?t=920895234054625192&siteid=23uscc&q="
		s_book_re = '<span class="s2"><a href="(.*?)".*?target="_blank">\r\n                            (.*?)</a>.*?</span>'
		book_re = '<dd> <a style=""=style="" href="(.*?).html">(.*?)</a></dd>'
		chap_re = '<div id="content">(.*?)</div>'
	elif url == 'www.x23us.com':
		code = 'gbk'
		s_book_url_f = r"https://www.x23us.com/modules/article/search.php?searchtype=keywords&searchkey="
		s_book_re = '<td class="odd"><a href=".*?">(.*?)</a></td>.*?<td class="even"><a href="(.*?)" target="_blank">'
		book_re = '<td class="L"><a href="(.*?).html">(.*?)</a></td>'
		chap_re = '<dd id="contents">(.*?)</div>'
	return s_book_url_f,s_book_re,book_re,chap_re

#### 通过链接选取网页内容	
def getStr(url,str_re):
	global code
	page = urllib.request.urlopen(url)
	html = page.read().decode(code)	 #需要解码
	str = r'%s' %str_re
	_re = re.compile(str,re.S)
	_str = re.findall(_re,html)
	return _str
	
#### 搜索获得此书，并获取书中各章节的链接
def getBook(book_name,s_book_url_f,s_book_re,book_re):
	global code
	keyword = quote(book_name.encode(code))
	s_book_url = s_book_url_f + keyword
	s_book_str = getStr(s_book_url,s_book_re)
	book_url = 'none'
	if code == 'utf-8':
		for s_book in s_book_str:
			if s_book[1] == book_name:
				book_url = s_book[0]
				break
	else:
		for s_book in s_book_str:
			a = s_book[0].replace('<b style="color:red">', '').replace('</b>','')
			if a == book_name:
				book_url = s_book[1]
				break
	if book_url == 'none':
		text.insert(END,'\n您可能想找这些书：\n')
		text.see(END)
		for s_book in s_book_str:
			if code == 'utf-8':
				text.insert(END,'\t%s\n' %s_book[1])
			else:
				text.insert(END,'\t%s\n' %s_book[0].replace('<b style="color:red">', '').replace('</b>',''))
			text.see(END)
	else:
		book_str = getStr(book_url,book_re)
		chap_num = len(book_str)
		text.insert(END,"\n*****小说《%s》，共有%s章，请选择下载章节*****\n" % (book_name,chap_num))
		text.see(END)
		return book_name,book_url,book_str,chap_num

#### 获取选择的章节并保存到本地
def getChap(Book,start_num,end_num,path,chap_re):
	book_name = Book[0]
	book_url = Book[1]
	book_str = Book[2]
	chap_num = Book[3]
	if path == '' or path == 'C:\\Users\\Wyili\\Desktop':
		path = 'C:\\Users\\Wyili\\Desktop'
	if not os.path.isdir(path):     #如果该路径下不存在path所指文件夹，则创建
		os.makedirs(path)
	file = path + '\\' + '%s.txt' %book_name
	if start_num == '' or start_num == '第一章':
		start_num = 1
	else:
		start_num = int(start_num)
	num = start_num
	if end_num == '' or end_num == '最后一章':
		book = book_str[(start_num-1):]
		down_num = chap_num - start_num + 1
	else:
		end_num = int(end_num)
		book = book_str[(start_num-1):end_num]
		down_num = end_num - start_num + 1
	text.insert(END,"\n.....小说《%s》，已选择%s章，开始下载.....\n" % (book_name,down_num))
	text.see(END)
	for chap in book:
		start_time = time.time()
		chap_title = chap[1]
		chap_url = book_url + chap[0] + '.html'
		chap_str = getStr(chap_url,chap_re)[0]
		chap = chap_str.replace("&nbsp;", " ").replace('<br/>','\n').replace('<br />','\n').replace('</br>','\n');
		fo = open(file, mode = 'w', encoding = 'utf-8',)  if num == 1  else open(file, mode = 'a', encoding = 'utf-8',)
		fo.write( chap_title + "\n" + chap + "\n\n\n")
		end_time = time.time()
		if num == start_num:
			cost_time = end_time - start_time
		else:
			cost_time = (end_time - start_time + cost_time) / 2
		down_time = round(down_num * cost_time)
		hour = down_time // (60*60)
		min = down_time % (60*60) // 60
		sec = down_time % (60*60) % 60
		down_num -= 1
		num += 1
		text.insert(END,"\n.....%s...下载成功！...还剩%s章...预计还需%s小时%s分钟%s秒.....\n" % (chap_title,down_num,hour,min,sec))
		text.see(END)
		global fun_2,fun_3
		if fun_3 == 1:
			text.insert(END,'\n.....已暂停...请按“暂停/继续”按钮继续.....\n')
			text.see(END)
		while fun_3 == 1:
			if fun_2 == 0:
				break
		if fun_2 == 0:
			break
	text.insert(END,"\n.....小说《%s》已结束下载！.....\n" % book_name)
	text.see(END)

def search():	
	url = e1.get()
	if url == '':
		url = 'www.qu.la'
	global Book,Web,fun_1
	Web = website(url)
	book_name = e2.get()       #搜索书名
	Book = getBook(book_name,Web[0],Web[1],Web[2])
	fun_1 = 1

def download():
	start_num =  e3.get()   #选择下载章节的范围
	end_num = e4.get()
	path = e5.get()   #选择本地保存TXT的路径
	getChap(Book,start_num,end_num,path,Web[3])

def stop_run():
	global fun_3
	if fun_3 == 0:
		fun_3 = 1
	else:
		fun_3 = 0

def fun1():
	global fun_1,fun_2
	fun_1 = 0
	fun_2 = 0
	th1 = threading.Thread(target = search)
	th1.setDaemon(True)
	th1.start()

def fun2():
	global fun_1,fun_2,fun_3
	if fun_1 == 1:
		fun_1 = 0
		time.sleep(0.1)
		fun_2 = 1
		fun_3 = 0
		th2 = threading.Thread(target = download)
		th2.setDaemon(True)
		th2.start()
	
def fun3():
	global fun_2
	if fun_2 == 1:
		th3 = threading.Thread(target = stop_run)
		th3.setDaemon(True)
		th3.start()

def fun4():
	sys.exit()
	
root = Tk(className = "小说下载工具 by Wyili")

FM = Frame(root)
fm = Frame(FM)
fm1 = Frame(fm)
Label(fm1,text='小说网网址：',font = 35).pack(side=TOP, anchor=W, fill=X, expand=YES,pady = 15)
Label(fm1,text='书名：',font = 35).pack(side=TOP, anchor=W, fill=X, expand=YES,pady = 15)
Label(fm1,text='开始章节：',font = 35).pack(side=TOP, anchor=W, fill=X, expand=YES,pady = 15)
Label(fm1,text='结束章节：',font = 35).pack(side=TOP, anchor=W, fill=X, expand=YES,pady = 15)
Label(fm1,text='下载路径：',font = 35).pack(side=TOP, anchor=W, fill=X, expand=YES,pady = 15)
fm1.pack(side=LEFT, fill=BOTH, expand=YES)

fm2 = Frame(fm)
v1 = StringVar()    # 设置变量 . 
v2 = StringVar()
v3 = StringVar()
v4 = StringVar()
v5 = StringVar()
e1 = ttk.Combobox(fm2, textvariable=v1,font = 35)
e1["values"] = ('www.qu.la', 'www.xxbiquge.com','www.x23us.la','www.x23us.com')
e1["state"] = "readonly"
e1.current(0)
e2 = Entry(fm2,textvariable=v2,font = 35)
e3 = Entry(fm2,textvariable=v3,font = 35)
e4 = Entry(fm2,textvariable=v4,font = 35)
e5 = Entry(fm2,textvariable=v5,font = 35)
e1.pack(side=TOP, anchor=W, fill=X, expand=YES,ipady=2.5)
e2.pack(side=TOP, anchor=W, fill=X, expand=YES,ipady=2.5)
e3.pack(side=TOP, anchor=W, fill=X, expand=YES,ipady=2.5)
e4.pack(side=TOP, anchor=W, fill=X, expand=YES,ipady=2.5)
e5.pack(side=TOP, anchor=W, fill=X, expand=YES,ipady=2.5)
fm2.pack(side=LEFT, fill=BOTH, expand=YES)
fm.pack(side=TOP, fill=BOTH, expand=YES)
e2.insert(END,'搜索书名之后再下载')
e3.insert(END,'第一章')
e4.insert(END,'最后一章')
e5.insert(END,'C:\\Users\\Wyili\\Desktop')
fm3 = Frame(FM)
Button(fm3,text='搜索',command=fun1,font = 35).pack(side=LEFT, anchor=W, fill=X, expand=YES)
Button(fm3,text='下载',command=fun2,font = 35).pack(side=LEFT, anchor=W, fill=X, expand=YES)
Button(fm3,text='暂停/继续',command=fun3,font = 35).pack(side=LEFT, anchor=W, fill=X, expand=YES)
Button(fm3,text='退出',command=fun4,font = 35).pack(side=LEFT, anchor=W, fill=X, expand=YES)
fm3.pack(side=TOP, fill=BOTH, expand=YES,pady = 15)
FM.pack(side=LEFT, fill=BOTH, expand=YES,padx= 25)

s1 = Scrollbar(root)
s1.pack(side = RIGHT, fill = Y)
s2 = Scrollbar(root, orient = HORIZONTAL)
s2.pack(side = BOTTOM, fill = X)
text = Text(root,yscrollcommand = s1.set, xscrollcommand = s2.set, wrap = 'none',font = 35)
text.pack(side=RIGHT, expand = YES,fill = BOTH)
s1.config(command = text.yview)
s2.config(command = text.xview)

import win32api, win32gui                #隐藏DOS窗口，仅在windows平台使用
ct = win32api.GetConsoleTitle()
hd = win32gui.FindWindow(0,ct)
win32gui.ShowWindow(hd,0)

root.mainloop()