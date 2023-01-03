import datetime
import pandas as pd
import requests
import time
import random
import json
import json
import jieba
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import numpy as np
from os import path
#https://github.com/JustDoPython/python-examples/tree/master/xianhuan http://www.justdopython.com/2022/01/23/python-weibohot/
headers = {
        "Host": "google-api.zhaoyizhe.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

def scrapy(date):
    print('开始爬取%s' % date)
    url = 'https://google-api.zhaoyizhe.com/google-api/index/mon/sec?date=%s' % date
    try:
        time.sleep(random.randint(1, 3))
        res = requests.get(url, headers=headers).json()
        result = res['data']
        return result
    except Exception as err:
        print(err)
        return None

#获取时间段
def get_date_list(startdate, enddate, freq='1D', dformat='%Y-%m-%d'):
    tm_rng = pd.date_range(startdate, enddate, freq=freq)
    return [x.strftime(dformat) for x in tm_rng]


hot_list = []
date_list = get_date_list('2022-01-01', '2022-12-31')
# print(date_list)
for d in date_list:
    result = scrapy(d)
    if result:
        hot_list.extend(result)

with open(r"weibo_hot.txt",  'w', encoding='utf-8') as f:
    for r in hot_list:
        try:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
        except Exception as err:
            print(err)
            print('出错啦')
month_data = {}
with open(r"weibo_hot.txt", "r", encoding="utf-8") as f:
    for line in f:
        data_obj = json.loads(line)
        date = data_obj['date']
        month_str = date[3:5]
        data_list = []
        if month_str in month_data:
            data_list =  month_data[month_str]
        data_list.append(data_obj)
        month_data[month_str] = data_list


def gen_wc_split_text(data_list=[], max_words=None, background_color=None,
                      # font_path='/System/Library/Fonts/PingFang.ttc',
                      font_path=r'C:\Windows\Fonts\simhei.ttf',
                      output_path='', output_name='',
                      mask_path=None, mask_name=None,
                      width=400, height=200, max_font_size=100, axis='off'):
    stopwords = open(r'stopwords.txt', 'r', encoding='utf-8').read().split('\n')[:-1]
    words_dict = {}
    for data in data_list:
        text = data['topic']
        hotNumber = data['hotNumber']
        if hotNumber is None:
            hotNumber = 1
        all_seg = jieba.cut(text, cut_all=False)
        for seg in all_seg:
            if seg in stopwords or seg == 'unknow':
                continue
            if seg in words_dict.keys():
                words_dict[seg] += hotNumber
            else:
                words_dict[seg] = hotNumber

    # 设置一个底图
    mask = None
    if mask_path is not None:
        mask = np.array(Image.open(path.join(mask_path, mask_name)))

    wordcloud = WordCloud(background_color=background_color,
                          mask=mask,
                          max_words=max_words,
                          min_font_size=1,
                          max_font_size=50,
                          width=300,
                          height=400,
                          # 如果不设置中文字体，可能会出现乱码
                          font_path=font_path)
    myword = wordcloud.generate_from_frequencies(words_dict)
    # 展示词云图
    # plt.imshow(myword)
    # plt.axis(axis)
    # plt.show()

    # 保存词云图
    wordcloud.to_file(path.join(output_path, output_name))


for month in month_data:
    data_list = month_data[month]
    
    gen_wc_split_text(data_list, output_name=month+'.png',background_color='white',  
    mask_path=None, mask_name="0"+month+".jpg", max_words=2000, 
    output_path=r".")