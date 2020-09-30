import re
import time
import urllib3
import requests
from wordcloud import WordCloud
import numpy as np, jieba
from PIL import Image
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#http://www.justdopython.com/2020/08/13/aljx/  https://cloud.tencent.com/developer/article/1681133
# 爬取一页评论内容https://github.com/JustDoPython/python-examples/blob/master/yeke/py-aljx/wb_spd.py
#微博的爬虫的目的网站主要有四个，pc 站网页版weibo.com、移动端weibo.cn 以及对应的 m（mobile） 站 手机端 m.weibo.com（无法在电脑上浏览）、m.weibo.cn，总得来说，.cn 比 .com 更简单 UI 更丑，m 站比 pc 站更简单 UI 更丑。
def get_one_page(url):
    headers = {
        'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3880.4 Safari/537.36',
        'Host' : 'weibo.cn',
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cookie' : 'SCF=Aph8ikViMlbWbx23PuwU0wn8YRO76QhJQyqKmrnEYow9_DMoSFrKvwtDpeUWR8qKMho6tH6OtQ7CUPBa6jkyQQk.; SUB=_2A25yZrRcDeRhGeNG7FoQ9CjKyT6IHXVRqNwUrDV6PUJbktANLXXVkW1NSxKupBN_mebEfJhnohrBJFSTe8-nOX3K; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW99FVYO.z1mi3U4juCgVa-5JpX5K-hUgL.Fo-RS0npShqceoz2dJLoI0qLxKMLBK-L1--LxK-L1K.LBKnLxK-L1hnL1hqLxKBLB.2LB-zLxKnLB.-LB.-LxKBLB.2LB.2t; SUHB=0XDV8lHGdkiCEy; SSOLoginState=1600308236; ALF=1602900236; _T_WM=43c263fc3a28bfa4d8a9257c9cd93b15',
        'DNT' : '1',
        'Connection' : 'keep-alive'
    }
    # 获取网页 html
    response = requests.get(url, headers = headers, verify=False)
    # 爬取成功
    if response.status_code == 200:
        # 返回值为 html 文档，传入到解析函数当中
        return response.text
    return None

# 解析保存评论信息
def save_one_page(html):
    comments = re.findall('<span class="ctt">(.*?)</span>', html)
    for comment in comments[1:]:
        result = re.sub('<.*?>', '', comment)
        if '回复@' not in result:
            with open('微博评论.txt', 'a+', encoding='utf-8') as fp:
                fp.write(result+'\r')
def jieba_():
    stop_words = []
    # with open('stop_words.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         stop_words.append(line.strip())
    content = open('微博评论.txt', 'rb').read()
    # jieba 分词
    word_list = jieba.cut(content)
    words = []
    for word in word_list:
        if word not in stop_words:
            words.append(word)
    global word_cloud
    # 用逗号隔开词语
    word_cloud = '，'.join(words)

def cloud():
    # 打开词云背景图
    cloud_mask = np.array(Image.open('wangfei.jpg'))
    # 定义词云的一些属性
    wc = WordCloud(
        # 背景图分割颜色为白色
        background_color='white',
        # 背景图样
        mask=cloud_mask,
        # 显示最大词数
        max_words=300,
        width=2000,
         height=1800,contour_width=3, contour_color='steelblue',
        # 显示中文
        font_path='C:\Windows\Fonts\simhei.ttf',
        # 最大尺寸
        max_font_size=100
    )
    global word_cloud
    # 词云函数
    x = wc.generate(word_cloud)
    # 生成词云图片
    image = x.to_image()
    # 展示词云图片
    image.show()
    # 保存词云图片
    wc.to_file('weibo_comment.jpg')
#这可能是全网最强的微博爬虫项目 https://github.com/nghuyong/WeiboSpider
#[Pyhon疫情大数据分析] 四.微博话题抓取及新冠肺炎疫情文本挖掘和情感分析 https://blog.csdn.net/Eastmount/article/details/104995419
#最强微博爬虫，用户、话题、评论一网打尽。 https://github.com/Python3Spiders/WeiboSuperSpider
#邮件标题：【向猿人学投稿】+文章标题https://www.yuanrenxue.com/tricks/be-writer.html
for i in range(10):
    url = 'https://weibo.cn/comment/C8FqitZ9X?uid=2357213493&rl=0&page='+str(i)
    html = get_one_page(url)
    print('正在爬取第 %d 页评论' % (i+1))
    save_one_page(html)
    time.sleep(1)
#[Pyhon疫情大数据分析] 四.微博话题抓取及新冠肺炎疫情文本挖掘和情感分析 https://blog.csdn.net/Eastmount/article/details/104995419
#尝试使用情感分析系统。http://ictclas.nlpir.org/nlpir/
#网易云音乐评论https://mp.weixin.qq.com/s?__biz=MzA3Nzc4MzY2NA==&mid=2247485619&idx=1&sn=015c78f35acdb66da8d7bdab0194299e&chksm=9f4dffaca83a76bac9fc9b596510d6bdd313e130f3abb52ddca1e60a68e1ba4f0133a2ccee7c&scene=21#wechat_redirect
jieba_()
cloud()    