import pandas as pd
import re,requests,jieba
f=input('请输入csv文件：')
if not f:
    f='公众号苏生不惑历史文章留言数据.csv'
# wechat=pd.read_csv(f,encoding='utf-8')
# pd.set_option('max_colwidth',1000)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_columns',None)

# print('文章数量：',len(wechat))
# print('原创和非原创：')
# print(wechat.是否原创.value_counts().sort_values(ascending=False).head(5))
# print('文章数量最多作者前5')

# print(wechat.文章作者.value_counts().sort_values(ascending=False).head(5))
# print(len(wechat[wechat.阅读数>100000]))
# print(wechat[wechat.阅读数>100000])
# print(wechat.阅读数.sum())

# wechat[['文章日期','文章标题','文章链接','阅读数']].sort_values(by='阅读数', ascending=False).head(10)
# wechat.sort_values(by='阅读数', ascending=False).head(10)

# wechat[['阅读数','点赞数','在看数','留言数']].mean()

# wechat[wechat.文章位置 == 1][['阅读数','点赞数','在看数','留言数']].mean()

# wechat.groupby('文章位置',as_index=False).agg({"阅读数":'count'}).sort_values(by=['阅读数'],ascending=False).head(5)

# wechat.文章位置.value_counts().sort_values(ascending=False).head(5)

# wechat.query('文章位置 == 2')
# wechat.groupby('是否原创').agg({"阅读数":'count'}).sort_values(by=['阅读数'],ascending=False).head(5)

# wechat[wechat["原文链接"].notnull()]

# len(wechat.query(f'文章日期 > "{date}"'))
import requests,re,csv,time,random,pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
import pandas as pd
from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image
wechat=pd.read_csv(f,encoding='utf-8')
print(wechat.评论昵称.value_counts().sort_values(ascending=False).head(10))
def data(df):
    df2=df.省份.value_counts().sort_values(ascending=False).head(10)
    ip = df2.index.tolist()
    counts = df2.values.tolist()
    bar = (
        Bar()
            .add_xaxis(ip)
            .add_yaxis("", counts)
    )
    pie = (
        Pie()
        .add("", [list(z) for z in zip(ip, counts)],radius=["40%", "75%"], )
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图",pos_left="center",pos_top="20"))
        .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"), )
    )
    pie.render('公众号留言统计数据.html')
# data(wechat)
def wordcloud_img(df):
    font = r'C:\Windows\Fonts\simhei.ttf'
    STOPWORDS = {"回复", '的','可以','吗','了','有','就','用','是','来','我','都','你','还','好'}#https://github.com/baipengyan/Chinese-StopWords https://github.com/elephantnose/characters
    # df = pd.read_csv(f"{mid}.csv",encoding='utf-8', usecols=[5])#取第5列
    df_copy = df.copy()
    df_copy['comment'] = df_copy['评论内容'].apply(lambda x: str(x).split())  # 去掉空格
    column_contents = df_copy.loc[:, 'comment'];df_list = column_contents.tolist()
    # df_list = df_copy.values.tolist();print(df_list)
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    # cloud_mask = np.array(Image.open("wangfei.jpg"))
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font,
                   stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    wc.generate(words)
    # image_colors = ImageColorGenerator(cloud_mask)#给词云上色
    # wc.recolor(color_func=image_colors)
    #看看词频高的有哪些,把无用信息去除 https://github.com/Brucepk/luoxiang/blob/master/bilibili_ciyun.py
    process_word = WordCloud.process_text(wc, words)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    print(sort[:50])
    wc.to_file(f"公众号留言统计数据.jpg")
# wordcloud_img(wechat)