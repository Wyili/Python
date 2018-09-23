# Python-for-huaban
# 此文件主要是用于动态爬取花瓣网的图片，之前用python+selenium+PhantomJS爬取网页动态加载内容，结果发现下载图片十分缓慢。
# 于是此次直接用原库中的urllib函数进行静态读取，下载速度快了很多，但是由于无法模拟网页读取，最多一次只读取到20个pin的图片。
# 为了额外实现动态爬取的功能，深入分析网页读取中json的关系，直接用每一批pin中最后的pinid来调用下一批共20个pin的图片，从而实现不断地读取图片的网址。
# 此次，将函数细致的模块化分类，可以在最下方直接修改url，first_num，all_num，path，这四个参数，从而简单实现在网址为url的网页上，下载第一张以first_num命名，共all_num张图片，到本地path路径下。
# 其中，url可以是"http://huaban.com/"+"favorite/beauty/"或者"explore/luoli/"等，具体可参考"http://huaban.com/categories/"下的分类。
