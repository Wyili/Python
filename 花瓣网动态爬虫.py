#coding:utf-8

import re
import os
import urllib.request

#### 获取网页源码
def getHtml(url):
	page = urllib.request.urlopen(url)
	html = page.read().decode('utf-8')	 #需要解码
	return html
	
#### 下载图片
def getImage(html):
	global num
	#### 获取HTML源码里面的app.page["pins"]部分，主要图片ID位于此部分
	app_page_pins_re = re.compile(r'app\.page\["pins"\](.*?);',re.S)
	app_page_pins_str = re.findall(app_page_pins_re,html)[0]
	#### 获取图片ID，保存在列表中
	pin_id_re = re.compile(r'"pin_id":(\d+)')
	pin_id_list = re.findall(pin_id_re,app_page_pins_str)
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
			urllib.request.urlretrieve(img_url,'{}{}.jpg'.format(paths,num))
		except:
			print("获取图片：%s失败，跳过，获取下一张。" % img_url)
			continue
		print("第%s张图片：" % num)
		print("%s获取成功！" % img_url)
		if num == end_num:
			print("图片保存成功！")
			exit()		
		num += 1
	return pin_id_list[-1]

def handle(url,first_num,all_num,path):
	global num,end_num,paths
	num = first_num
	end_num = first_num + all_num -1
	if not os.path.isdir(path):     #如果该路径下不存在path所指文件夹，则创建
		os.makedirs(path)
	paths = path+'\\'	  #保存到path所指的文件夹下
	html = getHtml(url)
	new_id = getImage(html)
	while True:
		url = url+"/?&max=" + str(new_id) + '&limit=' + str(20) + '&wfl=1';
		html = getHtml(url)
		new_id = getImage(html)

if __name__ == '__main__':
	url = "http://huaban.com/explore/luoli/"   #下载图片的网址
	first_num = 1		#命名第一张图片
	all_num = 21		  #下载图片的数量
	path = 'E:\\Downloads'    #选择本地保存图片的路径
	handle(url,first_num,all_num,path)
