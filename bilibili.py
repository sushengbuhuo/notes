import requests,jieba,os,re
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
import wordcloud
from matplotlib import pyplot as plt
from pyquery import PyQuery as pq
import imageio#进行图像的输入和输出  https://zhuanlan.zhihu.com/p/157205114
from wordcloud import STOPWORDS,ImageColorGenerator#用来取色
# text = open("zhihu.txt",encoding='utf-8')
# txt = text.read()
# mk = imageio.imread("jay.jpg")
# mk = np.array(Image.open('jay.jpg'))
# w = wordcloud.WordCloud(mask=mk,background_color="white",scale=20,font_path='c:/windows/fonts/simhei.ttf')
# w.generate(txt)
# w.to_file('wd.jpg')
# image_colors = ImageColorGenerator(mk)#给词云上色
# w_color=w.recolor(color_func=image_colors)
# w_color.to_file('wd2.png')
#https://github.com/HenryLau7/WordCloud/blob/master/Wordcloud.py

#根据时间段获取弹幕  url = f'https://api.bilibili.com/x/v2/dm/history?type=1&oid=120004475&date={date}'

# b站弹幕  https://github.com/unlimitbladeworks/python-tools/blob/cccd8946c8ede31c698ed2de0469b1e9ef547b3e/spider/bilibili_10.1/ganbei.py#L35
#抓取罗翔所有视频弹幕 https://github.com/Brucepk/luoxiang/blob/master/luo_ciyun.py
#os._exit()
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        }
url = input('请输入b站地址：')#https://www.bilibili.com/video/BV1JE411N7UD
response = requests.get(url, headers=headers)
match_rule = r'cid=(.*?)&aid'
cid = re.search(match_rule, response.text).group(0).replace('cid=', '').replace('&aid', '')
url = "http://comment.bilibili.com/{}.xml".format(cid)
print(url)
req = requests.get(url)
html = req.content
html_doc = str(html, "utf-8")  # 修改成utf-8
# req.encoding = 'utf-8'
# p = pq(req.text.encode('utf-8'))
# words_list=[]
# for content in p('d').contents():
	# words_list.append(content)
# 解析 b站 微博 豆瓣弹幕 https://zhuanlan.zhihu.com/p/139216132  https://zhuanlan.zhihu.com/p/166651429
word_cloud = ''
soup = BeautifulSoup(html_doc, "lxml")
results = soup.find_all('d')
contents = [x.text for x in results]
stopwords = set(STOPWORDS)
stopwords.update({'了','吧','哦'})
# stop_words = ["https", "co", "RT"] + list(STOPWORDS)
word_list = jieba.cut(','.join(contents))
words = []
for word in word_list:
	if word not in stopwords:
		words.append(word)
    # 用逗号隔开词语
	word_cloud = '，'.join(words)
cloud_mask = np.array(Image.open("xiyou.jpg"))
wc = WordCloud(background_color='white',stopwords=stopwords,mask=cloud_mask,max_words=500,font_path='c:/windows/fonts/simhei.ttf',max_font_size=60,repeat=True)
# 词云函数
x = wc.generate(word_cloud)#从字典生成词云
x.to_file('bi.jpg')
# 看看词频高的有哪些,把无用信息去除https://github.com/Brucepk/Kris-noodles/blob/master/bilibili-noodles-jieba.py
process_word = WordCloud.process_text(wc, word_cloud)
sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
print(sort[:50])

image_colors = ImageColorGenerator(cloud_mask)#给词云上色 从背景图建立颜色方案
w=wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
w.to_file('bi2.jpg')
# 生成词云图片
image = x.to_image()
# 展示词云图片
image.show()
# 保存词云图片
#wc.to_file('bili.png')
plt.imshow(wc, interpolation='bilinear')  # 显示词云
plt.axis('off')  # 关闭坐标轴
plt.show()  # 显示图像
# 保存结果
dic = {"contents": contents}
df = pd.DataFrame(dic)
df["contents"].to_csv("bilibili.csv", encoding="utf_8_sig", index=False)

def jieba_():
    # 打开评论数据文件
    content = open("bili.csv", "rb").read()
    # jieba 分词
    word_list = jieba.cut(content)
    words = []
    # 过滤掉的词
    #stopwords = open("stopwords.txt", "r", encoding="utf-8").read().split("\n")[:-1]
    stopwords = []
    for word in word_list:
        if word not in stopwords:
            words.append(word)
    global word_cloud
    # 用逗号隔开词语
    word_cloud = '，'.join(words)
# jieba_()
def cloud():
    # 打开词云背景图
    cloud_mask = np.array(Image.open("xiyou.jpg"))
    # 定义词云的一些属性
    wc = WordCloud(
        # 背景图分割颜色为白色
        background_color='white',
        stopwords=stopwords,
        # 背景图样
        mask=cloud_mask,
        # 显示最大词数
        max_words=500,
        # 显示中文
        font_path='c:/windows/fonts/simhei.ttf',
        # 最大尺寸
        max_font_size=60,
        repeat=True
    )
    global word_cloud
    # 词云函数
    x = wc.generate(word_cloud)
    # 生成词云图片
    image = x.to_image()
    # 展示词云图片
    image.show()
    # 保存词云图片
    #wc.to_file('bili.png')
# cloud()   