import time,sys
import re
import os
import requests,json,time,random
from bs4 import BeautifulSoup
import asyncio,os
from pyppeteer import launch
import tkinter,time
import pandas as pd
from tqdm import tqdm
from datetime import datetime
headers = {
        'origin': 'https://zhuanlan.zhihu.com',
        'referer': 'https://zhuanlan.zhihu.com/',
        'User-Agent': ('Mozilla/5.0'),
        'cookie':''
    }
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n']
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    return filename
def down(url):
    try:
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='RichContent-inner').prettify()
        title = soup.find(class_='QuestionHeader-title').get_text()
        answer_time= soup.find(class_='ContentItem-time').get_text()
        match = re.search(r'\d{4}-\d{2}-\d{2}', answer_time)
        # datetime_obj = datetime.strptime(answer_time, "%Y-%m-%d %H:%M")
        # date_str = datetime_obj.strftime("%Y-%m-%d")
        answer_date = match.group()
        print('开始下载回答：',url,title,answer_date)
        # title = re.sub('[\/:*?"<>|]','-',title)
        # content = content.replace('data-actual', '')
        # content = content.replace('h1>', 'h2>')
        # content = re.sub(r'<noscript>.*?</noscript>', '', content)
        # content = re.sub(r'src="data:image.*?"', '', content)
        content = content.replace('data-actualsrc', 'src')
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1><h3>%s</h3>%s</body></html>' % (
            title, url,content)
        with open('html/'+answer_date+'_'+replace_invalid_chars(title)+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
        # res = requests.get(url, headers=headers)
        # contents = re.search(r'<div class="Post-RichText">(.*?)</div>',res.text).group(1)
        # with open('zzz.html', 'w', encoding='utf-8') as f:
        # 	f.write(contents)
    except Exception as e:
        with open(f'下载失败知乎回答列表.txt', 'a+', encoding='utf-8') as f:
            f.write(url+'\n')
        print('下载回答失败', url,e)

if not os.path.exists('html'):
    os.mkdir('html')

filename = input('请输入知乎回答excel文件名：')
# filename='zhihu_answer.xlsx'
if not os.path.exists(filename):
    sys.exit('文件不存在')
file_name, file_extension = os.path.splitext(filename)
if file_extension == '.xlsx':
    df=pd.read_excel(filename)
    print('列标题',df.columns)
    print('行标题',df.index)
    for i in tqdm(df['知乎问题链接'].tolist(), desc='下载进度'):
        time.sleep(random.randint(1, 2))
        down('https:'+i)
        # break
elif file_extension == '.txt':
    with open(f'{filename}', encoding='utf-8') as f:
        contents = f.read()
    urls=contents.split('\n')
    for item in tqdm(urls, desc='下载进度'):
        down(item)

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

# for indexs in df.index:
#     print('数据',df.loc[indexs].values[0:-1])
# down('https://zhuanlan.zhihu.com/p/')
# asyncio.get_event_loop().run_until_complete(down('https://zhuanlan.zhihu.com/p/'))

