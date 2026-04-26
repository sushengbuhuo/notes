import time,sys
import re
import os
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
        'origin': 'https://zhuanlan.zhihu.com',
        'referer': 'https://zhuanlan.zhihu.com/',
        'User-Agent': ('Mozilla/5.0'),
        'cookie':cookie
    }
def get_history():
    history = []
    with open('zhihu_history.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('zhihu_history.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
urls_history = get_history()
def downAnswer(url):
    try:
        if url in urls_history:
            print('已经下载过：',url)
            return ''
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='RichContent-inner').prettify()
        title = soup.find(class_='QuestionHeader-title').get_text()
        answer_time= soup.find(class_='ContentItem-time').get_text()
        match = re.search(r'\d{4}-\d{2}-\d{2}', answer_time)
        # datetime_obj = datetime.strptime(answer_time, "%Y-%m-%d %H:%M")
        # date_str = datetime_obj.strftime("%Y-%m-%d")
        answer_date = match.group()
        aid=re.search(r'answer/(\d+)',url).group(1)
        print('开始下载回答：',url,title,answer_date,aid)
        # title = re.sub('[\/:*?"<>|]','-',title)
        # content = content.replace('data-actual', '')
        # content = content.replace('h1>', 'h2>')
        # content = re.sub(r'<noscript>.*?</noscript>', '', content)
        # content = re.sub(r'src="data:image.*?"', '', content)
        content = content.replace('data-original', 'src')
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1><h3>%s</h3>%s</body></html>' % (
            title, url,content)
        with open(f'知乎专栏目录.md', 'a+', encoding='utf-8') as f2:
            f2.write('[{}]'.format(answer_date+'_'+title) + '({})'.format(url)+ '\n\n')
        with open('html/'+answer_date+'_'+replace_invalid_chars(title)+'_'+aid+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
        try:
             with open('知乎专栏.txt', 'a+', encoding='utf-8') as f:
                result_text = [line for line in soup.find(class_='RichContent-inner').find(class_='RichText').get_text().splitlines() if line.strip()]
                f.write('\n'.join(result_text)+ '\n\n'+ '\n\n')
        except Exception as err:
            print('下载txt出错了',err,url)
        save_history(url)
        return answer_date
    except Exception as e:
        with open(f'下载失败知乎回答文章列表.txt', 'a+', encoding='utf-8') as f:
            f.write(url+'\n')
        print('下载回答失败', url,e)
        return ''
def downArticle(url):
    try:
        if url in urls_history:
            print('已经下载过：',url)
            return ''
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='Post-RichText').prettify()
        title = soup.find(class_='Post-Title').get_text()
        answer_time= soup.find(class_='ContentItem-time').get_text()
        match = re.search(r'\d{4}-\d{2}-\d{2}', answer_time)
        answer_date = match.group()
        print('开始下载文章：',url,title,answer_date)
        # title = re.sub('[\/:*?"<>|]','-',title)
        # content = content.replace('data-actual', '')
        # content = content.replace('h1>', 'h2>')
        # content = re.sub(r'<noscript>.*?</noscript>', '', content)
        # content = re.sub(r'src="data:image.*?"', '', content)
        content = content.replace('data-original', 'src')
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1><h3>%s</h3>%s</body></html>' % (
            title,url, content)
        with open(f'知乎专栏目录.md', 'a+', encoding='utf-8') as f2:
            f2.write('[{}]'.format(answer_date+'_'+title) + '({})'.format(url)+ '\n\n')
        with open('html/'+answer_date+'_'+replace_invalid_chars(title)+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
        try:
             with open('知乎专栏.txt', 'a+', encoding='utf-8') as f:
                result_text = [line for line in soup.find(class_='Post-RichText').get_text().splitlines() if line.strip()]
                f.write('\n'.join(result_text)+ '\n\n'+ '\n\n')
        except Exception as err:
            print('下载txt出错了',err,url)
        save_history(url)
        return answer_date
    except Exception as e:
        with open(f'下载失败知乎回答文章列表.txt', 'a+', encoding='utf-8') as f:
            f.write(url+'\n')
        print('下载文章失败', url,e)#;raise Exception("抓取失败了："+url)
        return ''
def downPin(url):
    try:
        if url in urls_history:
            print('已经下载过：',url)
            return ''
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content=''
        content2=''
        title=re.search(r'/(\d+)$', url).group(1)
        remainContentRichText = soup.find(class_='PinItem-remainContentRichText')
        if remainContentRichText:
            imgs=re.findall(r'src="([^"]+)"', remainContentRichText.prettify())
            if imgs:
                for i in imgs:
                    content+=f'<img  src="{i}"><br>'
        RichContent = soup.find(class_='CopyrightRichText-richText')
        if RichContent:
            content2=RichContent.get_text()
            if content2 != '':
                title = content2[:30]
        answer_time= soup.find(class_='ContentItem-time').get_text()
        match = re.search(r'\d{4}-\d{2}-\d{2}', answer_time)
        answer_date = match.group()
        print('开始下载想法：',url,title,answer_date)
        # title = re.sub('[\/:*?"<>|]','-',title)
        # content = content.replace('data-actual', '')
        # content = content.replace('h1>', 'h2>')
        # content = re.sub(r'<noscript>.*?</noscript>', '', content)
        # content = re.sub(r'src="data:image.*?"', '', content)
        content = content.replace('data-original', 'src')+content2
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h3>%s</h3>%s</body></html>' % (
            url, content)
        with open(f'知乎专栏目录.md', 'a+', encoding='utf-8') as f2:
            f2.write('[{}]'.format(answer_date+'_'+title) + '({})'.format(url)+ '\n\n')
        with open('html/'+answer_date+'_'+replace_invalid_chars(title)+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
        try:
             with open('知乎专栏.txt', 'a+', encoding='utf-8') as f:
                result_text = [line for line in content2.splitlines() if line.strip()]
                f.write('\n'.join(result_text)+ '\n\n'+ '\n\n')
        except Exception as err:
            print('下载txt出错了',err,url)
        save_history(url)
    except Exception as e:
        with open(f'下载失败知乎想法列表.txt', 'a+', encoding='utf-8') as f:
            f.write(url+'\n')
        print('下载文章失败', url,e)#;raise Exception(e)

if not os.path.exists('html'):
    os.mkdir('html')

filename = input('请输入知乎回答文章文件名：')
with open(f'{filename}', encoding='utf-8') as f:
    contents = f.read()
urls=contents.split('\n')
for item in urls:
    if not item:
        continue
    if item in get_history():
        print('已经下载过：',item)
        continue
    if 'question' in item and 'answer' in item:
        downAnswer(item)
    elif 'pin' in item:
        downPin(item)
    else:
        downArticle(item)
    
    time.sleep(random.randint(1,2))
# for item in tqdm(urls, desc='下载进度'):
#     down(item)
#     time.sleep(random.randint(1,2))

