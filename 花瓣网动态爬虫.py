#coding:utf-8

import re
import os
import urllib.request

#### 获取网页源码
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')     #需要解码
    return html

x = 1 
#### 下载图片
def getImage(html,num):
    global x
    #### 获取HTML源码里面的app.page["pins"]部分，主要图片ID位于此部分
    app_page_pins_re = re.compile(r'app\.page\["pins"\](.*?);',re.S)
    app_page_pins_str = re.findall(app_page_pins_re,html)[0]
    #### 获取图片ID，保存在列表中
    pin_id_re = re.compile(r'"pin_id":(\d+)')
    pin_id_list = re.findall(pin_id_re,app_page_pins_str)
    path = 'E:\\Downloads'
    # 将图片保存到E:\\Downloads文件夹中，如果没有test文件夹则创建
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path+'\\'      #保存在Downloads路径下
    for pinid in pin_id_list:
        #### 获取跳转网页网址
        url_str = r'http://huaban.com/pins/%s/' % pinid
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
            urllib.request.urlretrieve(img_url,'{}{}.jpg'.format(paths,x))
        except:
            print("获取图片：%s失败，跳过，获取下一张。" % img_url)
            continue
        print("第%s张图片：" % x)
        print("%s获取成功！" % img_url)
        if x==num:
            print("图片保存成功！")
            exit()		
        x += 1
    return pin_id_list[-1]

def main(url,num):
    html = getHtml(url)
    new_id=getImage(html,num)
    while True:
        url=url+"/?&max=" + str(new_id) + '&limit=' + str(20) + '&wfl=1';
        html = getHtml(url)
        new_id=getImage(html,num)

if __name__ == '__main__':
    url="http://huaban.com/favorite/beauty/"   #下载图片的网址
    num=30          #下载图片的数量
    main(url,num)
