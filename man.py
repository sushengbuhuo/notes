import requests
import time
import json
import pandas as pd
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
import jieba
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import numpy as np
from os import path
# 获取商品列表https://github.com/JustDoPython/python-examples/blob/master/xianhuan/yanxuanbriefs/briefs_man.py
def search_keyword(keyword):
    uri = 'https://you.163.com/xhr/search/search.json'
    query = {
        "keyword": keyword,
        "page": 1
    }
    try:
        res = requests.get(uri, params=query).json()
        result = res['data']['directly']['searcherResult']['result']
        product_id = []
        for r in result:
            product_id.append(r['id'])
        return product_id
    except:
        raise

# 获取评论
def details(product_id):
    url = 'https://you.163.com/xhr/comment/listByItemByTag.json'
    try:
        C_list = []
        for i in range(1, 5):
            query = {
                "itemId": product_id,
                "page": i,
            }
            res = requests.get(url, params=query).json()
            if not res['data']['commentList']:
                break
            print("爬取第 %s 页评论" % i)
            commentList = res['data']['commentList']
            C_list.extend(commentList)
            time.sleep(1)

        return C_list
    except:
        raise


# product_id = search_keyword('男士内裤')
# r_list = []
# for p in product_id:
#     r_list.extend(details(p))

# with open('man.txt', 'w', encoding='utf-8') as f:
#     for r in r_list:
#         try:
#             f.write(json.dumps(r, ensure_ascii=False) + '\n')
#         except:
#             print('出错啦')
color = []
size = []
comments = []
#https://github.com/JustDoPython/python-examples/blob/master/xianhuan/yanxuanbriefs/briefs_ana.py
#http://www.justdopython.com/2020/09/02/yanxuanbriefs/
with open("man.txt", "r", encoding="utf-8") as f:
    for line in f:
        data_obj = json.loads(line)
        comments.append(data_obj['content'])
        skuinfo = data_obj['skuInfo']
        for sku in skuinfo:
            if '颜色' in sku and '规格' not in sku:
                filter_sku = sku.replace("颜色:", "").strip().replace("（", "").replace("）3条", "").replace("四条装", "").replace("*2", "").replace("2条", "").replace("）", "")
                color.extend(filter_sku.split('+'))
            elif '尺码' in sku and '~' not in sku:
                size.append(sku.replace('尺码:', ""))

# 颜色可视化
df = pd.DataFrame(color, columns=['color'])
analyse_color = df['color'].value_counts()

bar = Bar()
bar.add_xaxis(analyse_color.index.values.tolist())
bar.add_yaxis("", analyse_color.values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
    title_opts=opts.TitleOpts(title="颜色分布"),
    # datazoom_opts=opts.DataZoomOpts(),
)
# bar.render_notebook()
bar.render('briefs_color.html')


# 尺码可视化
df2 = pd.DataFrame(size, columns=['size'])
analyse_size = df2['size'].value_counts()

bar = Bar()
bar.add_xaxis(analyse_size.index.values.tolist())
bar.add_yaxis("", analyse_size.values.tolist())
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
    title_opts=opts.TitleOpts(title="尺寸分布"),
    # datazoom_opts=opts.DataZoomOpts(),
)
bar.render('briefs_size.html')


# 评论可视化
text = " ".join(comments)
def gen_wc_split_text(text='There is no txt', max_words=None, background_color=None,
                      font_path='c:/windows/fonts/simhei.ttf',
                      output_path='', output_name='',
                      mask_path=None, mask_name=None,
                      width=400, height=200, max_font_size=100, axis='off'):
    all_seg = jieba.cut(text, cut_all=False)
    split_text = ' '
    for seg in all_seg:
        split_text = split_text + seg + ' '

    # 设置一个底图
    mask = None
    if mask_path is not None:
        mask = np.array(Image.open(path.join(mask_path, mask_name)))

    wordcloud = WordCloud(background_color=background_color,
                          mask=mask,
                          max_words=max_words,
                          max_font_size=max_font_size,
                          width=width,
                          height=height,
                          # 如果不设置中文字体，可能会出现乱码
                          font_path=font_path)
    myword = wordcloud.generate(str(split_text))
    # 展示词云图
    plt.imshow(myword)
    plt.axis(axis)
    plt.show()

    # 保存词云图
    wordcloud.to_file(path.join(output_path, output_name))

gen_wc_split_text(text, output_name='briefs_comments_wc.png', output_path='./')