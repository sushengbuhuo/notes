import time,sys
import re
import os,json
import requests,json,random
from bs4 import BeautifulSoup
import asyncio,os
#from pyppeteer import launch
#import tkinter,time
import pandas as pd
from tqdm import tqdm
from datetime import datetime
def get_cookie():
    cookie = ''
    if os.path.exists('cookie.txt'):
        with open('cookie.txt', encoding='utf-8') as f:
            cookie = f.read().replace('\n','')
    return cookie
cookie = get_cookie()
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 FirePHP/0.7.4',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
        'cookie':''
    }
def get_history():
    history = []
    with open('eastmoney_history.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history
def remove_html_tags(text):
    # 匹配所有HTML标签的正则表达式
    clean = re.compile('<.*?>')
    # 替换匹配到的标签为空字符串
    return re.sub(clean, '', text)
def remove_html_tags2(text):
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(text, "html.parser")
    # 获取纯文本
    return soup.get_text()
def save_history(url):
    with open('eastmoney_history.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
urls_history = get_history()
def down(url):
    try:
        if url in urls_history:
            print('已经下载过：',url)
            return ''
        cookies = {
            'qgqp_b_id': '41a43a50e371d4c17faa9f2f2c044c04',
            'fullscreengg': '1',
            'fullscreengg2': '1',
            'st_si': '13604433675777',
            'st_asi': 'delete',
            'cdcfh': '3825336190592976',
            'st_pvi': '28039354014226',
            'st_sp': '2024-02-26%2009%3A44%3A58',
            'st_inirUrl': 'https%3A%2F%2Femcreative.eastmoney.com%2Fapp_fortune%2Fperson%2Findex.html',
            'st_sn': '12',
            'st_psi': '20250616182459833-119101302791-4917162286',
        }
        html = requests.get(url, headers=headers,timeout=10).text;print(html)
        soup = BeautifulSoup(html, 'lxml')
        if 'guba.eastmoney.com' in url:
            content = re.search(r'<script>var post_article=(.*?)</script>',html).group(1)
            data=json.loads(content.replace('undefined','""'))
            content = data['post_content']
            date=data['post_publish_time'][0:10]
            content = re.sub(r'alt', 'height="500"', content)
            title = data['post_title']
            if not title:
                title=remove_html_tags(data['post_content'])[:20]
        else:
            match=re.search(r'<span class="txt">.*?(\d{4})年(\d{2})月(\d{2})日.*?</span>',html,re.DOTALL)## 使用re.DOTALL让.匹配包括换行符在内的所有字符
            year, month, day = match.groups()
            date = f"{year}-{month}-{day}"
            content = re.search(r'var articleTxt = "(.*)"',html).group(1).replace('\\', '')
            title = soup.find(class_='article-title').get_text().replace('\r', '').replace('\n', '').replace('\r\n', '').replace(' ', '')
            content = re.sub(r'height=".*"', 'height="500"', content)
        
        print('开始下载：',url,title)
        # title = re.sub('[\/:*?"<>|]','-',title)
        # content = content.replace('data-actual', '')
        # content = content.replace('h1>', 'h2>')
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1><h3>%s</h3>%s</body></html>' % (
            title, url,content)
        with open(f'帖子目录.md', 'a+', encoding='utf-8') as f2:
            f2.write('[{}]'.format(title) + '({})'.format(url)+ '\n\n')
        with open('html/'+date+'_'+replace_invalid_chars(title)+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
        save_history(url)
        return ''
    except Exception as e:
        with open(f'下载失败列表.txt', 'a+', encoding='utf-8') as f:
            f.write(url+'\n')
        print('下载失败', url,e);raise Exception("抓取失败了："+url)
        return ''

if not os.path.exists('html'):
    os.mkdir('html')

filename = input('请输入文件名：');filename='eastmoney.txt'
# with open(f'{filename}.csv', 'a+', encoding='utf-8-sig') as f:
    # f.write('时间'+','+'标题' + ','+'链接'+ ','+'赞同数'+ ','+'评论数'+'\n')
# filename='zhihu_answer.xlsx'
if not os.path.exists(filename):
    sys.exit('文件不存在')
file_name, file_extension = os.path.splitext(filename)
if file_extension == '.txt':
    with open(f'{filename}', encoding='utf-8') as f:
        contents = f.read()
    urls=contents.split('\n')
    num = 0
    for item in urls:
        # if num > 1:
        #     continue
        if not item:
            continue
        if item in get_history():
            print('已经下载过：',item)
            continue
        down(item)
        time.sleep(random.randint(1,5))
        num+=1
    # for item in tqdm(urls, desc='下载进度'):
    #     down(item)
    #     time.sleep(random.randint(1,2))
