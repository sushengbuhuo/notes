import requests,re,csv,time,random,pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba,urllib3,sys
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def ip_detail(mid):
    df = pd.read_csv(f"{mid}.csv",encoding='utf-8',on_bad_lines='skip')
    df2=df.转发来源.value_counts().sort_values(ascending=False).head(10)
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
    pie.render(str(mid) +'.html')
    # df2.to_csv(str(mid) +".csv",encoding="utf_8_sig",index=False)
def wordcloud_img(mid):
    font = r'C:\Windows\Fonts\simhei.ttf'
    STOPWORDS = {"回复", '的','可以','吗','了','有'}#https://github.com/baipengyan/Chinese-StopWords https://github.com/elephantnose/characters
    df = pd.read_csv(f"{mid}.csv",encoding='utf-8',on_bad_lines='skip', usecols=[3])#取第3列
    df_copy = df.copy()
    df_copy['转发内容'] = df_copy['转发内容'].apply(lambda x: str(x).split())  # 去掉空格
    df_list = df_copy.values.tolist()#;print(df_copy)
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment);print(words)
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
    wc.to_file(f"{mid}.jpg")
def repost(mid,page,headers):
	url=f'https://www.weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page}&moduleID=feed&count=20'
	res=requests.get(url, headers=headers, verify=False).json()
	if not res["data"]:
		print(res)
		return False
	for v in res["data"]:
		parsed_datetime = datetime.strptime(v['created_at'], "%a %b %d %H:%M:%S %z %Y")#Mon Nov 06 14:06:06 +0800 2023
		formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
		try:
			soup = BeautifulSoup(v['source'], 'html.parser')
			source = soup.text#删除HTML标签
			with open(f'{mid}.csv', 'a+', encoding='utf-8-sig') as f:
				f.write(trimName(v['user']['screen_name'])+','+trimName(v['user']['idstr']) + ','+formatted_datetime+ ','+trimName(v['text_raw'])+ ','+v['region_name']+ ','+trimName(source)+ ','+str(v['reposts_count'])+ ','+str(v['comments_count'])+ ','+str(v['attitudes_count'])+'\n')
		except Exception as e:
			print(e)

	return True
page = 1
mid=input('请输入微博mid：')
if not mid:
	sys.exit('mid为空')
cookie=input('请输入微博cookie：')
if not cookie:
	sys.exit('cookie为空')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 FirePHP/0.7.4',
        'Cookie': cookie
               # 'Referer': 'https://m.weibo.cn/detail/4497103885505673',
               # 'Sec-Fetch-Mode': 'navigate'
    }
with open(f'{mid}.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('微博昵称'+','+'微博uid' + ','+'转发时间'+','+'转发内容'+','+'转发地区'+','+'转发来源'+','+'转发数'+','+'评论数'+','+'点赞数'+ '\n')
while True:
    if page > 10:
        break
    print("页数：",page)
    res = repost(mid,page,headers)
    time.sleep(1)
    if not res:
        break
    page+=1

# ip_detail(mid)
# wordcloud_img(mid)