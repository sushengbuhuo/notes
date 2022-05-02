# 定义保存评论的函数https://www.52pojie.cn/thread-1623485-1-1.html  https://github.com/stay-leave/weibo-crawer
import requests,re,csv,time,random,pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image
def comments(mid, url, headers, number):
    url1=url
    count = 0  # 设置一个初始变量count为0来进行计数
    max_id=0
    # 当count数量小于预期的number时，进行循环
    while count < number:
        # 判断是不是第一组评论，如果是的话，第一组评论不需要加max_id，之后的需要加
        if count == 0:
            try:
                url3 = url + mid + '&mid=' + mid + '&max_id_type=0'
                time.sleep(random.randint(0, 5))
                web_data = requests.get(url3, headers=headers)  # F12查看data信息
                js_con = web_data.json()  # 转换一下数据格式
                # 获取连接下一页评论的max_id
                max_id = js_con['data']['max_id']  # max_id在[data]中
                max_tpye = js_con['data']['max_id_type']
                print(url3,max_id)
                comments = js_con['data']['data']  # 获得数据中[data]中的[data]
                for comment in comments:  # 依次循环获得comments中的数据
                    text = comment["text"]
                    create_time = time.strftime( '%Y-%m-%d %H:%M:%S',(time.strptime(comment['created_at'].replace('+0800',''))))
                    floor_number = comment['floor_number']
                    userid = comment['user']['id']
                    screen_name = comment['user']['screen_name']
                    source =comment['source']
                    like_count =comment['like_count']
                    child_comments =comment['comments']
                    label = re.compile(r'</?\w+[^>]*>', re.S)
                    text = re.sub(label, '', text)
                    count += 1
                    csv_save([count, create_time, userid, screen_name, floor_number, text,like_count,source],mid)
                    print([count, create_time, userid, screen_name, floor_number, text,like_count,source])
                    print("第{}条评论".format(count))
                    if child_comments:
                        for child_comment in child_comments:
                            text = child_comment["text"]
                            create_time = time.strftime( '%Y-%m-%d %H:%M:%S',(time.strptime(child_comment['created_at'].replace('+0800',''))))
                            floor_number = child_comment['floor_number']
                            userid = child_comment['user']['id']
                            screen_name = child_comment['user']['screen_name']
                            source =child_comment['source']
                            like_count =0
                            label = re.compile(r'</?\w+[^>]*>', re.S)
                            text = re.sub(label, '', text)
                            count += 1
                            csv_save([count, create_time, userid, screen_name, floor_number, text,like_count,source],mid)
                            # print([count, create_time, userid, screen_name, floor_number, text,like_count,source])
                            print("第{}条评论".format(count))
            except Exception as e:
                print("出错了", e)
                continue
        else:
            try:
                url2 = url1 + mid + '&mid=' + mid +'&max_id=' + str(max_id) + '&max_id_type='+str(max_tpye)
                time.sleep(random.randint(0, 6))
                web_data = requests.get(url2, headers=headers)
                js_con = web_data.json()
                max_id = js_con['data']['max_id']
                max_tpye=js_con['data']['max_id_type']
                comments = js_con['data']['data']
                print(url2,max_id)
                for comment in comments:
                    text = comment["text"]
                    create_time = time.strftime( '%Y-%m-%d %H:%M:%S',(time.strptime(comment['created_at'].replace('+0800',''))))
                    floor_number = comment['floor_number']
                    userid = comment['user']['id']
                    screen_name = comment['user']['screen_name']
                    source =comment['source']
                    like_count =comment['like_count']
                    child_comments =comment['comments']
                    label = re.compile(r'</?\w+[^>]*>', re.S)
                    text = re.sub(label, '', text)
                    count += 1
                    csv_save([count, create_time, userid, screen_name, floor_number, text,like_count,source],mid)
                    print([count, create_time, userid, screen_name, floor_number, text,like_count,source])
                    print("第{}条评论".format(count))
                    if child_comments:
                        for child_comment in child_comments:
                            text = child_comment["text"]
                            create_time = time.strftime( '%Y-%m-%d %H:%M:%S',(time.strptime(child_comment['created_at'].replace('+0800',''))))
                            floor_number = child_comment['floor_number']
                            userid = child_comment['user']['id']
                            screen_name = child_comment['user']['screen_name']
                            source =child_comment['source']
                            like_count =0
                            label = re.compile(r'</?\w+[^>]*>', re.S)
                            text = re.sub(label, '', text)
                            count += 1
                            csv_save([count, create_time, userid, screen_name, floor_number, text,like_count,source],mid)
                            # print([count, create_time, userid, screen_name, floor_number, text,like_count,source])
                            print("第{}条评论".format(count))
                if max_id == 0:
                    break
            except Exception as e:
                print("出错了", e)
                continue
def ip_detail(mid):
    df = pd.read_csv(f"{mid}.csv",encoding='utf-8',on_bad_lines='skip')
    df2=df.ip.value_counts().sort_values(ascending=False).head(10)
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
    df = pd.read_csv(f"{mid}.csv",encoding='utf-8',on_bad_lines='skip', usecols=[5])#取第5列
    df_copy = df.copy()
    df_copy['comment'] = df_copy['评论内容'].apply(lambda x: str(x).split())  # 去掉空格
    df_list = df_copy.values.tolist()
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
    wc.to_file(f"{mid}.jpg")
def csv_save(data,mid):
    with open(f"{mid}.csv", "a+",newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(data)
if __name__ == "__main__":
    data = ["id", "评论时间", "用户ID", "昵称", "评论楼层", "评论内容",'评论点赞数','ip']
    user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44",
    ]
    url = 'https://m.weibo.cn/comments/hotflow?id='
    mid = input('请输入微博mid:') # 要爬取的微博id  #https://m.weibo.cn/detail/xxx
    # 打开微博手机端网页https://m.weibo.cn，找到要爬取的微博id！
    number = int(input('请输入抓取的评论数:'))  # 设置爬取评论量,爬取量在第X组，爬取时会爬取下来该组的数据，所以最终数据可能会大于number，一般是个整10的数
    cookie = input('请输入微博cookie:')
    cookies = [
        cookie # 微博的cookie
        ]
    headers = {
    'User-Agent': random.choice(user_agent)
        , 'Cookie': random.choice(cookies)
               # 'Referer': 'https://m.weibo.cn/detail/4497103885505673',
               # 'Sec-Fetch-Mode': 'navigate'
    }  # 设置user-agent来进行伪装，突破微博反爬限制
    
    csv_save(data,mid)
    comments(mid, url, headers, number)
    ip_detail(mid)
    wordcloud_img(mid)