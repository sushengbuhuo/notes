# -*- coding: utf-8 -*-
"""
微信好友性别及位置信息https://juejin.im/post/5aab23ef6fb9a028e25d4c47#heading-0
"""

#导入模块
from wxpy import Bot,Tuling,embed,ensure_one
import itchat
import matplotlib.pyplot as plt
from collections import Counter
import re,jieba
import jieba.analyse
import numpy as np
from PIL import Image
from snownlp import SnowNLP
from wordcloud import WordCloud


'''Q
微信机器人登录有3种模式，
(1)极简模式:robot = Bot()
(2)终端模式:robot = Bot(console_qr=True)
(3)缓存模式(可保持登录状态):robot = Bot(cache_path=True)
'''
#初始化机器人，选择缓存模式（扫码）登录
robot = Bot(cache_path=True)

#获取好友信息
robot.chats()
robot.mps()#获取微信公众号信息

#获取好友的统计信息
Friends = robot.friends()
print(Friends.stats_text())

my_friend = ensure_one(robot.search('郑凯'))  #想和机器人聊天的好友的备注
tuling = Tuling(api_key='你申请的apikey')
@robot.register(my_friend)  # 使用图灵机器人自动与指定好友聊天
def reply_my_friend(msg):
    tuling.do_reply(msg)
embed()

my_group = robot.groups().search('群聊名称')[0]  # 记得把名字改成想用机器人的群
tuling = Tuling(api_key='376cb2ca51d542c6b2e660f3c9ea3754')  # 一定要添加，不然实现不了
@robot.register(my_group, except_self=False)  # 使用图灵机器人自动在指定群聊天
def reply_my_friend(msg):
    print(tuling.do_reply(msg))
embed()
#朋友圈好友性别分布
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)
sexs = list(map(lambda x: x['Sex'], friends[1:]))
counts = list(map(lambda x: x[1], Counter(sexs).items()))
labels = ['Male','FeMale',   'Unknown']
colors = ['red', 'yellowgreen', 'lightskyblue']
plt.figure(figsize=(8, 5), dpi=80)
plt.axes(aspect=1)
plt.pie(counts,  # 性别统计结果
        labels=labels,  # 性别展示标签
        colors=colors,  # 饼图区域配色
        labeldistance=1.1,  # 标签距离圆点距离
        autopct='%3.1f%%',  # 饼图区域文本格式
        shadow=False,  # 饼图是否显示阴影
        startangle=90,  # 饼图起始角度
        pctdistance=0.6  # 饼图区域文本距离圆点距离
)
plt.legend(loc='upper right',)
plt.title('%s的微信好友性别组成' % friends[0]['NickName'])
plt.show()
#https://github.com/Snailclimb/Python
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)
def analyseSignature(friends):
    signatures = ''
    emotions = []
    for friend in friends:
        signature = friend['Signature']
        if(signature != None):
            signature = signature.strip().replace('span', '').replace('class', '').replace('emoji', '')
            signature = re.sub(r'1f(\d.+)','',signature)
            if(len(signature)>0):
                nlp = SnowNLP(signature)
                emotions.append(nlp.sentiments)
                signatures += ' '.join(jieba.analyse.extract_tags(signature,5))
    with open('signatures.txt','wt',encoding='utf-8') as file:
         file.write(signatures)

    # 朋友圈朋友签名的词云相关属性设置
    back_coloring = np.array(Image.open('alice_color.png'))
    wordcloud = WordCloud(
        font_path='simfang.ttf',
        background_color="white",
        max_words=1200,
        mask=back_coloring, 
        max_font_size=75,
        random_state=45,
        width=1250, 
        height=1000, 
        margin=15
    )
    
    #生成朋友圈朋友签名的词云
    wordcloud.generate(signatures)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('signatures.jpg')#保存到本地文件

    # Signature Emotional Judgment
    count_good = len(list(filter(lambda x:x>0.66,emotions)))#正面积极
    count_normal = len(list(filter(lambda x:x>=0.33 and x<=0.66,emotions)))#中性
    count_bad = len(list(filter(lambda x:x<0.33,emotions)))#负面消极
    labels = [u'负面消极',u'中性',u'正面积极']
    values = (count_bad,count_normal,count_good)
    plt.rcParams['font.sans-serif'] = ['simHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel(u'情感判断')#x轴
    plt.ylabel(u'频数')#y轴
    plt.xticks(range(3),labels)
    plt.legend(loc='upper right',)
    plt.bar(range(3), values, color = 'rgb')
    plt.title(u'%s的微信好友签名信息情感分析' % friends[0]['NickName'])
    plt.show()
analyseSignature(friends)
