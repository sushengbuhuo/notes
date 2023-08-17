import time,sys
import re
import os
import requests,json
from bs4 import BeautifulSoup
import asyncio,os
from pyppeteer import launch
import tkinter,time
import pandas as pd
from tqdm import tqdm
headers = {
        'origin': 'https://zhuanlan.zhihu.com',
        'referer': 'https://zhuanlan.zhihu.com/',
        'User-Agent': ('Mozilla/5.0'),
        'cookie':''
    }
def down(url):
    try:
        print('开始下载文章',url)
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='Post-RichText').prettify()
        title = soup.find(class_='Post-Title').get_text()
        # title = re.sub('[\/:*?"<>|]','-',title)
        # content = content.replace('data-actual', '')
        # content = content.replace('h1>', 'h2>')
        # content = re.sub(r'<noscript>.*?</noscript>', '', content)
        # content = re.sub(r'src="data:image.*?"', '', content)
        content = content.replace('data-actualsrc', 'src')
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1>%s</body></html>' % (
            title, content)
        with open('html/'+title+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
        # res = requests.get(url, headers=headers)
        # contents = re.search(r'<div class="Post-RichText">(.*?)</div>',res.text).group(1)
        # with open('zzz.html', 'w', encoding='utf-8') as f:
        # 	f.write(contents)
    except:
        print('下载文章 %s 失败', url)

if not os.path.exists('html'):
    os.mkdir('html')

filename = input('请输入excel文件名：')
filename='zhuhu_article.xlsx'
if not os.path.exists(filename):
    sys.exit('文件不存在')
df=pd.read_excel(filename)
# https://www.cnblogs.com/flyup/p/15264897.html 
# 所有数据df.values 二维数组 df.values[i , j]，第i行第j列的值 df.values[[i1 , i2 , i3]]，第i1、i2、i3行数据 df.values[: , j]，第j列数据df.iloc[:, j].values
# df.loc[A, B]和iloc[A, B]。其中A表示对行的索引，B表示对列的索引，B可缺省
# loc将参数当作标签处理，iloc将参数当作索引号处理。也就是说，在有表头的方式中，当列索引使用str标签时，只可用loc，当列索引使用索引号时，只可用iloc；在无表头的方式中，索引向量也是标签向量，loc和iloc均可使用；在切片中，loc是闭区间，iloc是半开区间。
# print(df['知乎链接'].tolist()) df.loc[: , :].values
# df.columns = ['col_one', 'col_two']  df.columns = df.columns.str.replace(' ', '_') df.astype({'col_one':'float', 'col_two':'float'}).dtypes
# df = df.apply(pd.to_numeric, errors='coerce').fillna(0) 仅需一行代码就完成了我们的目标，因为现在所有的数据类型都转换成float
# stock_files = sorted(glob('data/stocks*.csv')) df = pd.read_clipboard()
# movies[movies.name.isin(['Action', 'Drama', 'Western'])].head() counts = movies.name.value_counts() counts.nlargest(3).index
# movies[movies.name.isin(counts.nlargest(3).index)].head()
# 格式化 format_dict = {'Date':'{:%m/%d/%y}', 'Close':'${:.2f}', 'Volume':'{:,}'}
# df['city'] = df.location.str.split(', ', expand=True)[0]
# 对order_id使用groupby()，再对每个group的item_price进行求和。 df.groupby('order_id').item_price.sum().head() df.groupby('order_id').item_price.agg(['sum', 'count']).head()
# stocks.style.format(format_dict)
print('列标题',df.columns)
print('行标题',df.index)
# for indexs in df.index:
#     print('数据',df.loc[indexs].values[0:-1])
# down('https://zhuanlan.zhihu.com/p/454939476')
# asyncio.get_event_loop().run_until_complete(down('https://zhuanlan.zhihu.com/p/454939476'))
for i in tqdm(df['知乎链接'].tolist(), desc='下载进度'):
    down('https:'+i)