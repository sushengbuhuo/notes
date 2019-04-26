import itchat
from wxpy import *
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.font_manager as fm
import os
from os import path
import re, jieba
bot = Bot()
#https://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud pip install wordcloud-1.5.0-cp37-cp37m-win32.whl
#pip install matplotlib jieba
my_friends = bot.friends(update=False)

print(my_friends.stats_text())
stopwords_path='stopwords.txt'

#定义个函数式用于分词
def jiebaclearText(text):
    #定义一个空的列表，将去除的停用词的分词保存
    mywordList=[]
    #进行分词
    seg_list=jieba.cut(text,cut_all=False)
    #将一个generator的内容用/连接
    listStr='/'.join(seg_list)
    listStr = listStr.replace("class","")
    listStr = listStr.replace("span", "")
    listStr = listStr.replace("emoji", "")
    #打开停用词表
    f_stop=open(stopwords_path,encoding="utf8")
    #读取
    try:
        f_stop_text=f_stop.read()
    finally:
        f_stop.close()#关闭资源
    #将停用词格式化，用\n分开，返回一个列表
    f_stop_seg_list=f_stop_text.split("\n")
    #对默认模式分词的进行遍历，去除停用词
    for myword in listStr.split('/'):
        #去除停用词
        if not(myword.split()) in f_stop_seg_list and len(myword.strip())>1:
            mywordList.append(myword)
    return ' '.join(mywordList)
# 生成词云图
def make_wordcloud(text1,i):
	bg = plt.imread("love.jpg")
	# 生成
	wc = WordCloud(# FFFAE3
		background_color="#FFFFFF",  # 设置背景为白色，默认为黑色
		width=990,  # 设置图片的宽度
		height=440,  # 设置图片的高度
		mask=bg,
		margin=10,  # 设置图片的边缘
		max_font_size=70,  # 显示的最大的字体大小
		random_state=20,  # 为每个单词返回一个PIL颜色
		font_path='simkai.ttf'  # 中文处理，用系统自带的字体
	).generate(text1)
	# 为图片设置字体
	my_font = fm.FontProperties(fname='simkai.ttf')
	# 图片背景
	bg_color = ImageColorGenerator(bg)
	# 开始画图
	plt.imshow(wc.recolor(color_func=bg_color))
	# 为云图去掉坐标轴
	plt.axis("off")
	# 画云图，显示
	# 保存云图
	wc.to_file("render_0%d.png"%i)
# 微信昵称
nick_name = ''
# 微信个性签名
wx_signature = ''
for friend in my_friends:
	# 微信昵称：NickName
	nick_name = nick_name + friend.raw['NickName']
	# 个性签名：Signature
	wx_signature = wx_signature + friend.raw['Signature']

nick_name = jiebaclearText(nick_name)
wx_signature = jiebaclearText(wx_signature)
make_wordcloud(nick_name,5)
make_wordcloud(wx_signature,6)
wx_public_name = ''
# 公众号简介https://gitee.com/ShaErHu/wxpy_matplotlib_learning
wx_pn_signature = ''
# 获取微信公众号列表
my_wx_pn = bot.mps(update=False)
for wx_pn in my_wx_pn:
	wx_public_name = wx_public_name + wx_pn.raw['NickName']
	wx_pn_signature = wx_pn_signature + wx_pn.raw['Signature']

wx_public_name = jiebaclearText(wx_public_name)
make_wordcloud(wx_public_name,7)
wx_pn_signature = jiebaclearText(wx_pn_signature)
make_wordcloud(wx_pn_signature,8)
# labels = ['男性', '女性', '其他']
# sizes = [57.1, 32.2, 10.7]
# explode = (0, 0.1, 0)
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# # 纵横相等，画成一个圆
# ax1.axis('equal')
# plt.legend()
# plt.show()
"""
Login successfully as 风吹麦浪
风吹麦浪 共有 138 位微信好友

男性: 75 (54.3%)
女性: 36 (26.1%)

TOP 10 省份
北京: 22 (15.94%)
广东: 17 (12.32%)
上海: 11 (7.97%)
浙江: 4 (2.90%)
河南: 4 (2.90%)
福建: 3 (2.17%)
安徽: 3 (2.17%)
四川: 3 (2.17%)
辽宁: 3 (2.17%)
江苏: 3 (2.17%)

TOP 10 城市
深圳: 13 (9.42%)
海淀: 10 (7.25%)
朝阳: 8 (5.80%)
杭州: 4 (2.90%)
广州: 4 (2.90%)
成都: 3 (2.17%)
浦东新区: 3 (2.17%)
黄浦: 2 (1.45%)
合肥: 2 (1.45%)
大连: 2 (1.45%)

梦想旅程 共有 1123 位微信好友

男性: 690 (61.4%)
女性: 317 (28.2%)

TOP 10 省份
北京: 305 (27.16%)
广东: 106 (9.44%)
上海: 80 (7.12%)
浙江: 55 (4.90%)
江西: 44 (3.92%)
江苏: 33 (2.94%)
福建: 16 (1.42%)
河北: 16 (1.42%)
四川: 14 (1.25%)
河南: 12 (1.07%)

TOP 10 城市
朝阳: 103 (9.17%)
海淀: 87 (7.75%)
深圳: 72 (6.41%)
杭州: 48 (4.27%)
吉安: 28 (2.49%)
浦东新区: 24 (2.14%)
广州: 23 (2.05%)
南京: 15 (1.34%)
成都: 12 (1.07%)
西安: 12 (1.07%)
"""