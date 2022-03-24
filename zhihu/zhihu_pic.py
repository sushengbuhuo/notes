import urllib
import requests
from pyquery import PyQuery as pq
#from pymongo import MongoClient
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#python爬取知乎回答图片 https://zhuanlan.zhihu.com/p/43408400  https://www.zhihu.com/question/310335618/answer/602970433


# url = 'https://www.zhihu.com/api/v4/answers/602970433?include=is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,collapsed_counts,reviewing_comments_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_author,voting,is_thanked,is_nothelp,upvoted_followees;author.is_blocking,is_blocked,is_followed,voteup_count,message_thread_token,badge[?(type=best_answerer)].topics'
headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Referer': 'https://www.zhihu.com/api/v4/questions/38485891',
        'x-requested-with': 'fetch',
    }
# res = requests.get(url,headers=headers,verify=False).json()
# print(res['content'])
# content = pq(res['content'])  # content 内容为 xml 格式的网页，用pyquery解析
# imgs_url = []
# imgs = content('figure noscript img').items()
# for img_url in imgs:
#     imgs_url.append(img_url.attr('src'))
"""
有哪部电影让你受益良多？ https://www.zhihu.com/question/303835412
有没有什么演员演技炸裂的电视剧或电影？ https://www.zhihu.com/question/337052769
有哪些演员颜值特别高的电影或电视剧？ https://www.zhihu.com/question/337052769
好看的黑帮片有哪些？ https://www.zhihu.com/question/20181715
有哪些看完可以让人热血沸腾的动作片推荐？ https://www.zhihu.com/question/27855422
除了迪士尼和宫崎骏，还有哪些值得一看的动画电影？ https://www.zhihu.com/question/37236484
有没好看的动漫电影https://www.zhihu.com/question/353249199
有哪些场面宏大，气势恢宏的战争片 https://www.zhihu.com/question/23360742
哪些战争片值得推荐？https://www.zhihu.com/question/23809684
你心中的最佳恐怖片是哪部？ https://www.zhihu.com/question/27701620
有没有好一点的恐怖片推荐一下？https://www.zhihu.com/question/316293494
有没有一部电影让你在深夜中痛哭 https://www.zhihu.com/question/37206525
让你感动到哭的电影是什么 https://www.zhihu.com/question/24946395
迄今为止哪部电影最感动你？https://www.zhihu.com/question/366245943
有没有一部可以让人痛哭流涕的电影https://www.zhihu.com/question/343259251
有哪些值得一看的爱情电影https://www.zhihu.com/question/28119032
让你感动的爱情片有哪些 https://www.zhihu.com/question/20689411
有哪些好看的悬疑片或者神反转的电影 https://www.zhihu.com/question/326959870
有哪些好看的高智商悬疑电影https://www.zhihu.com/question/35811067
有哪些类似《看不见的客人》这样好看的推理悬疑电影或电视剧 https://www.zhihu.com/question/57661988
有哪些笑点密集的喜剧电影 https://www.zhihu.com/question/28049735
你认为最搞笑的电影是哪部 https://www.zhihu.com/question/24530726
有哪些爆笑恶搞能把人笑爆炸的电影值得推荐 https://www.zhihu.com/question/36918815
有哪些搞笑又发人深省的电影https://www.zhihu.com/question/49560603
有什么特别搞笑的国产华语电影https://www.zhihu.com/question/50338370
你认为哪些华语电影是被严重低估的 https://www.zhihu.com/question/20826845
有哪些值得一看的中国电影 https://www.zhihu.com/question/325544586
有哪些好看的韩国电影值得推荐 https://www.zhihu.com/question/35685110
有什么好看的美国电影么？ https://www.zhihu.com/question/275049443
你心目中的香港电影十佳是哪些？https://www.zhihu.com/question/19809033
 有哪些画面超美的小众电影？ https://www.zhihu.com/question/21286139
 有哪些好看的国产电影值得推荐？ https://www.zhihu.com/question/19804920
有哪些优秀的、「燃到爆」的电影？ https://www.zhihu.com/question/48035752
有哪些震撼心灵的好电影值得推荐 https://www.zhihu.com/question/353914676
有哪些好看的负能量电影https://www.zhihu.com/question/30994199
有哪些爆笑恶搞能把人笑爆炸的电影值得推荐 https://www.zhihu.com/question/36918815
有哪些适合恋人一起看的电影？ https://www.zhihu.com/question/24309989
如果只能推荐两部电影你会推荐哪两部https://www.zhihu.com/question/368550554
有什么高分好看的电影推荐？https://www.zhihu.com/question/342727398
你想推荐给别人哪些很爽无尿点的高分电影？https://www.zhihu.com/question/267317643
你有哪些看过五遍以上的经典电影 https://www.zhihu.com/question/353072809
如果让你向别人推荐十部电影，你会推荐哪十部？https://www.zhihu.com/question/281185483
有哪些好看到让人无法自拔、久久不忘的电影？https://www.zhihu.com/question/38485891
有哪些电影一定要趁年轻看？https://www.zhihu.com/question/25699277
有哪些你看过五遍以上的电影？https://www.zhihu.com/question/31537241
如果给你30秒让你说出三部你觉得最好的电影，会是哪三部 https://www.zhihu.com/question/369042910
#电影 https://www.zhihu.com/topic/19550429/hot
df3=pd.concat([df1[['name','counts']],df2[['name','counts']]])


import os
import pandas as pd
import numpy as np
 
dir = "D:\\merge"#设置工作路径
#新建列表，存放文件名（可以忽略，但是为了做的过程能心里有数，先放上）
filename_excel = []
#新建列表，存放每个文件数据框（每一个excel读取后存放在数据框）
frames = []
for root, dirs, files in os.walk(dir):
for file in files:
#print(os.path.join(root,file))
filename_excel.append(os.path.join(root,file))
df = pd.read_excel(os.path.join(root,file)) #excel转换成DataFrame
frames.append(df)
#打印文件名
print(filename_excel)
#合并所有数据
result = pd.concat(frames)
#查看合并后的数据
result.head()
result.shape
 
result.to_csv('D:\\merge\\a12.csv',sep=',',index = False)#保存合并的数据到电脑D盘的merge文件夹中，并把合并后的文件命名为a12.csv
"""

def getAnswers(qid):
    # 获取所有书籍和回答数据
    offset = 0
    book_data = {}
    while True:
        qid = qid
        print('Offset =', offset)
        # 知乎api请求
        url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=content&limit=20&offset={}&platform=desktop&sort_by=default".format(
            qid, offset)
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        data = res.json()
        if len(data['data']) == 0:
            break
        for line in data['data']:
            # 保存回答数据
            content = line['content']
            # print(content)
            result = re.findall(r'《(.*?)》', content)#re.findall(r'(https?://bilibili.com(.*))',content)
            for name in result:
                book_data[name] = book_data.get(name, 0) + 1
        offset += 20
    # 保存爬取的内容
    pandas_data=[]
    for i in book_data.keys():
        new_data = {}
        if i:
            new_data['name'] = re.sub(r'</?\w+[^>]*>','',i)#from pyquery import PyQuery doc = PyQuery('<div><span>toto</span><span>tata</span></div>') print doc.text()
            new_data['counts'] = book_data[i]
            pandas_data.append(new_data)
    df2 = pd.DataFrame(pandas_data, columns=['name', 'counts'])
    df2.sort_values(by=['counts'], ascending=False, inplace=True)
    books = df2['name'].head(50).tolist()#索引
    counts = df2['counts'].head(50).tolist()#值
    print(',  '.join(books))
    # print(',  '.join(counts))
    bar = (
        Bar()
            .add_xaxis(books)
            .add_yaxis("", counts)
    )
    # bar.render('books.html')
    pie = (
        Pie()
        .add("", [list(z) for z in zip(books, counts)],radius=["40%", "75%"], )
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图",pos_left="center",pos_top="20"))
        .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"), )
    )
    pie.render(str(qid) +'.html')
    df2.to_csv(str(qid) +".csv",encoding="utf_8_sig")
getAnswers(303835412)#https://www.zhihu.com/topic/19550429/top-answers https://www.zhihu.com/topic/19550429/index
#https://github.com/zhangzhe532/icodebugs/blob/master/DataAnalysis/%E8%8E%B7%E5%8F%96%E7%9F%A5%E4%B9%8E%E5%9B%BE%E7%89%87/zhihu_get_pic%26ans.py
def get_page(offset, referer):
    param = {
        'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
        'limit': '20',  # 限制当页显示的回答数，知乎最大20
        'offset': offset,  # 偏移量
        'platform': 'desktop',
        'sort_by': 'default',
    }
    headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Referer': referer,  # 问题的 url 地址
        'x-requested-with': 'fetch',
    }
    base_URL = 'https://www.zhihu.com/api/v4/questions/310335618/answers?include='  # 基础 url 用来构造请求url
    url = base_URL + urllib.parse.urlencode(param)  # 构造请求地址
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        print('请求失败')
        return None


def get_answer(json):
    for answer in json['data']:
        answer_info = {}
        # 获取作者信息
        author_info = answer['author']
        author = {}
        author['follower_count'] = author_info['follower_count']  # 作者被关注数量
        author['headline'] = author_info['headline']  # 个性签名
        author['name'] = author_info['name']  # 昵称
        author['index_url'] = author_info['url']  # 主页地址
        # 获取回答信息
        voteup_count = answer['voteup_count']  # 赞同数
        comment_count = answer['comment_count']  # 评论数
        # 解析回答内容
        content = pq(answer['content'])  # content 内容为 xml 格式的网页，用pyquery解析
        imgs_url = []
        imgs = content('figure noscript img').items()
        for img_url in imgs:
            imgs_url.append(img_url.attr('src'))  # 获取每个图片地址
        # 获取回答内容引用的其他相似问题
        question_info = content('a').items()
        questions = {}
        for que in question_info:
            url = que.attr('href')
            question = que.text()
            questions['url'] = question + ' ' + url  # 其他相似问题标题及地址
        # 字典映射存储回答信息
        answer_info['author'] = author
        answer_info['voteup_count'] = voteup_count
        answer_info['comment_count'] = comment_count
        answer_info['imgs_url'] = imgs_url
        answer_info['questions'] = questions
        answer_info['answer_url'] = 'https://www.zhihu.com/answer/'+str(answer['id'])
        yield answer_info  # yield 关键字把函数变成迭代器


# 存储在mongoDB
# client = MongoClient(host='localhost')
# db = client['zhihu']
# collection = db['zhihu']
# def save_to_mongodb(answer_info):
#     if collection.insert(answer_info):
#         print('已存储一条回答到MongoDB')

def save_to_img(imgs_url, author_name, base_path):
    path = base_path + author_name
    if not os.path.exists(path):  # 判断路径文件夹是否已存在
        os.mkdir(path)

        for url in imgs_url:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    img_path = '{0}/{1}.{2}'.format(path,
                                                    md5(response.content).hexdigest(), 'jpg')  # 以图片的md5字符串命名防止重复图片
                    if not os.path.exists(img_path):
                        with open(img_path, 'wb') as jpg:
                            jpg.write(response.content)
                    else:
                        print('图片已存在，跳过该图片')
            except requests.ConnectionError:
                print('图片链接失效，下载失败，跳过该图片')
                import traceback
                traceback.print_exc()
        print('已保存答主：' + author_name + ' 回答内容的所有图片')


def main(offset):
    path = 'zhihu'  # 指定图片存储路径
    json = get_page(offset, "https://www.zhihu.com/question/310335618")  # referer 地址，如果有需要可以根据获取的其他相似问题，继续抓取其他问题的图片。
    for answer in get_answer(json):
        # save_to_mongodb(answer)
        save_to_img(answer['imgs_url'], answer['author']['name'], path)




# START = 0  # 开始
# END = 40  # 结束
# if __name__ == "__main__":
#     pool = Pool()  # 线程池
#     #groups = [i * 20 for i in range(START, END)]  # 偏移量每次增大20
#     groups = [0]
#     pool.map(main, groups)
#     pool.close()
#     pool.join()