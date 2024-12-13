import requests,re,os,time,html,sys,csv
import random
# import pandas as pd
import traceback,urllib3
from os.path import basename
# from docx import Document, ImagePart
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62_encode(num, alphabet=ALPHABET):
    num = int(num)
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)
def remove_query_params(url):
    # 使用 split() 方法将 URL 按照问号分割成两部分
    url_parts = url.split('?')
    
    # 检查是否存在问号
    if len(url_parts) > 1:
        # 存在问号，只取问号前面的部分
        url_without_query = url_parts[0]
    else:
        # 不存在问号，保持原样
        url_without_query = url
    
    return url_without_query
def base62_decode(string, alphabet=ALPHABET):
    string = str(string)
    num = 0
    idx = 0
    for char in string:
        power = (len(string) - (idx + 1))
        num += alphabet.index(char) * (len(alphabet) ** power)
        idx += 1

    return num
def reverse_cut_to_length(content, code_func, cut_num=4, fill_num=7):
    content = str(content)
    cut_list = [content[i - cut_num if i >= cut_num else 0:i] for i in range(len(content), 0, (-1 * cut_num))]
    cut_list.reverse()
    result = []
    for i, item in enumerate(cut_list):
        s = str(code_func(item))
        if i > 0 and len(s) < fill_num:
            s = (fill_num - len(s)) * '0' + s
        result.append(s)
    return ''.join(result)
def get_cookie():
    cookie = ''
    if os.path.exists('cookie.txt'):
        with open('cookie.txt', encoding='utf-8') as f:
            cookie = f.read().replace('\n','')
    return cookie
cookie = get_cookie()
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://weibo.com/1744395855/NkD5bjvPC',
        "Cookie":cookie,
    }
from datetime import datetime
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def get_history():
    history = []
    with open('weibo_history.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('weibo_history.txt', 'a+') as f:
        f.write(url.strip() + '\n')
urls_history = get_history()
def main(file):
    # df=pd.read_excel('微博链接.xlsx')
    # print('列标题',df.columns)
    # print('行标题',df.index)
    num = 0
    history = get_history()
    data=[]
    urls=[]
    contents = ''
    ext=os.path.splitext(os.path.basename(file))[0]
    with open(f'{file}', encoding='utf-8') as f:
        contents = f.read()
    urls=contents.split('\n')
    for url in urls:
    # for index, row in df.iterrows():
        # url= remove_query_params(row['微博链接'])
        url= remove_query_params(url)
        if not url:
            continue
        if url in urls_history:
            print('已经下载过：',url)
            continue
        time.sleep(random.randint(1, 3))
        num +=1
        # if num > 100:
        #     break
        try:
            print('开始下载',num,url)
            if 'ttarticle' in url:
                # https://weibo.com/ttarticle/x/m/show#/id=2309405097366029205772&_wb_client_=1
                mid = re.search(r'https?://(www\.)?weibo.com/ttarticle/x/m/show/id/(\d+)', url).group(2)
                article_url=f'https://weibo.com/ttarticle/x/m/aj/detail?&id={mid}'
                res = requests.get(article_url,proxies={'http': None,'https': None},verify=False, headers=headers).json()
                soup = BeautifulSoup(res['data']['content'], 'html.parser')
                content = soup.get_text()# re.sub(r'<[^>]*>', '', html) 过滤html中的标签
                if not content:
                    with open(f'下载失败微博.txt', 'a+', encoding='utf-8') as f:
                        f.write(url+'\n')
                    continue
                print(res['data']['create_at'],content)
                data.append([url,content,res['data']['complete_create_at'],'0','0','0'])
                save_history(url)
            else: 
                m=re.search(r'https?://(www\.)?weibo\.com/\d+/(.*)',url)
                mid=''
                if m:
                    mid = m.group(2)
                    if not mid.isdigit():
                        mid=reverse_cut_to_length(m.group(2), base62_decode, 4, 7)
                if not mid:
                    m2=re.search(r'https?://m\.weibo\.cn/(detail|status)/(\d+)',remove_query_params(url))
                    if m2:
                        mid=m2.group(2)
                if not mid:
                    with open(f'下载失败微博.txt', 'a+', encoding='utf-8') as f:
                        f.write(url+'\n')
                    continue
                url2=f'https://weibo.com/ajax/statuses/show?id={mid}&locale=zh-CN'#https://www.weibo.com/ajax/statuses/extend?id=5049927780796644
                res = requests.get(html.unescape(url2),proxies={'http': None,'https': None},verify=False, headers=headers).json()
                if res['ok'] == 0:
                    with open(f'下载失败微博.txt', 'a+', encoding='utf-8') as f:
                        f.write(url+'\n')
                    continue
                content = res['text_raw']
                if res['isLongText']:
                    # https://weibo.com/1203726997/5096924988049671
                    content = requests.get(f'https://weibo.com/ajax/statuses/longtext?id={mid}',proxies={'http': None,'https': None},verify=False, headers=headers).json()['data']['longTextContent']
                dt_obj = datetime.strptime(res['created_at'], '%a %b %d %H:%M:%S %z %Y')
                created_at = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
                print(created_at,content)
                data.append([url,content,created_at,str(res['attitudes_count']),str(res['comments_count']),str(res['reposts_count'])])
                save_history(url)
        except Exception as e:
            print(url,e)#;raise Exception(e)
            with open(f'下载失败微博.txt', 'a+', encoding='utf-8') as f:
                f.write(url+'\n')
    with open(f'{ext}.csv', 'a+', newline='', encoding='utf-8-sig') as filecsv:
        writer = csv.writer(filecsv)
        writer.writerows(data)
print('本工具更新于2024年12月12日，获取最新版本请关注公众号苏生不惑')
file = input('公众号苏生不惑提示你，请输入微博链接txt文件名：')
ext=os.path.splitext(os.path.basename(file))[0]
with open(f'{ext}.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('微博链接'+','+'微博内容' +','+'微博发布时间' +','+'点赞数' +','+'评论数' +','+'转发数' + '\n')
main(file)

