import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import jieba
import pandas as pd
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
#https://github.com/zhouwei713/data_analysis/blob/master/weibo_mayili_wenzhang/get_comment.py
Headers = {'Cookie': '_s_tentry=www.dewen.net.cn; login_sid_t=c156816173137ad768184b9cd42c414e; cross_origin_proto=SSL; TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517; Apache=1797960551813.34.1534477014971; SINAGLOBAL=1797960551813.34.1534477014971; WBtopGlobal_register_version=9744cb1b8d390b27; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20; TC-V-WEIBO-G0=35846f552801987f8c1e8f7cec0e2230; XSRF-TOKEN=ZDkGVSSD_1ZCVFl8PoxwM1D8; SSOLoginState=1596435574; ULV=1597285705096:1:1:1:1797960551813.34.1534477014971:; wvr=6; UOR=www.dewen.net.cn,widget.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW99FVYO.z1mi3U4juCgVa-5JpX5KMhUgL.Fo-RS0npShqceoz2dJLoI0qLxKMLBK-L1--LxK-L1K.LBKnLxK-L1hnL1hqLxKBLB.2LB-zLxKnLB.-LB.-LxKBLB.2LB.2t; SUHB=0pHBOdN6AeBLRw; ALF=1631782804; SCF=Aph8ikViMlbWbx23PuwU0wn8YRO76QhJQyqKmrnEYow9cgo-80-faLQjJHko1bi6TQFO6ToThP0oLndsLLxyZeI.; SUB=_2A25yZaRFDeRhGeNG7FoQ9CjKyT6IHXVREpKNrDV8PUNbmtAKLWOnkW9NSxKupDQJZ73blxm8gefNggM9omREORE_; wb_view_log_5878146622=1920*10801; webim_unReadCount=%7B%22time%22%3A1600246724406%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A42%2C%22msgbox%22%3A0%7D; TC-Page-G0=ab398e55b03eff607e8d521e56f494bd|1600246831|1600246817; Ugrow-G0=1ac418838b431e81ff2d99457147068c'}

def mayili(page):
    mayili = []
    for i in range(0, page):
        print("page: ", i)
        url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=3820658587146613&page=%s' % int(i)
        # url = 'https://m.weibo.cn/api/comments/show?id=3820658587146613&page=%s' % int(i)4467107636950632
        req = requests.get(url, headers=Headers,verify=False).text
        html = json.loads(req)['data']['html']
        content = BeautifulSoup(html, "html.parser")
        # comment = content.find_all('div', attrs={'class': 'list_li S_line1 clearfix'})
        comment_text = content.find_all('div', attrs={'class': 'WB_text'})
        # comment_text = json.loads(req)['data']['data']
        print(comment_text)
        for c in comment_text:
            mayili_text = c.text.split("：")[1]
            # mayili_text = c.get('text')
            mayili.append(mayili_text)
        time.sleep(1)

    return mayili


#历年的足球俱乐部得分和排名 footballdatabase.com/ranking/world/1
#世界各国历年的 GDP 总值和增长率数据  data.worldbank.org/ https://zhuanlan.zhihu.com/p/92541935
def wordcloud_m():
    font = r'C:\Windows\Fonts\simhei.ttf'
    STOPWORDS = {"回复", }
    df = pd.read_csv('李文亮.csv', usecols=[1])
    df_copy = df.copy()
    df_copy['comment'] = df_copy['comment'].apply(lambda x: str(x).split())  # 去掉空格
    df_list = df_copy.values.tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    cloud_mask = np.array(Image.open("wangfei.jpg"))
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font,
                   stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    wc.generate(words)
    # image_colors = ImageColorGenerator(cloud_mask)#给词云上色
    # wc.recolor(color_func=image_colors)
    #看看词频高的有哪些,把无用信息去除 https://github.com/Brucepk/luoxiang/blob/master/bilibili_ciyun.py
    process_word = WordCloud.process_text(wc, words)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    print(sort[:50])
    wc.to_file('王菲3.jpg')

if __name__ == '__main__':
    print("start")
    ma_comment = mayili(1)
    mayili_pd = pd.DataFrame(columns=['comment'], data=ma_comment)
    mayili_pd.to_csv('wb.csv', encoding='utf_8_sig')
    # wordcloud_m()