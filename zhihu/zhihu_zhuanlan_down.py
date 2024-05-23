import time,sys
import re
import os
import requests,json
from bs4 import BeautifulSoup
#https://gitee.com/crossin/snippet/blob/master/get_zhihu/get_zhihu.py p/44918640
#https://segmentfault.com/a/1190000042751896 https://blog.csdn.net/Harden13_/article/details/121895009
##爬虫 https://github.com/srx-2000/spider_collection https://github.com/13060923171/Crawl-Project3
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ').replace('"', '“')
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def video(vid,title):
    url = f'https://www.zhihu.com/zvideo/{vid}'
    if not os.path.exists('video'):
        os.mkdir('video')
    try:
        resp = requests.get(url, headers=headers,timeout=5).text
        data = re.search(r'<script id="js-initialData" type="text/json">(.*?)</script>',resp).group(1)
        play = json.loads(data)
        playdata = requests.get(play['initialState']['entities']['zvideos'][vid]['video']['playlist']['hd']['playUrl'], headers=headers)
        print('下载视频:',title)
        with open('video/'+title+'.mp4','wb') as f:
            f.write(playdata.content)
    except Exception as e:
        print(vid,e)
def answer(content,title,updated_time):
    if not os.path.exists('html'):
        os.mkdir('html')
    print('下载回答:',title)
    content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1>%s</body></html>' % (
            title, content)
    with open(os.path.join("html/", time.strftime('%Y-%m-%d', time.localtime(updated_time))+f"-{title}.html"), 'w', encoding='utf-8') as f:
        f.write(content)
def articles(content,title,updated_time):
    if not os.path.exists('html'):
        os.mkdir('html')
    print('下载文章:',title)
    content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1>%s</body></html>' % (
            title, content)
    with open(os.path.join("html/", time.strftime('%Y-%m-%d', time.localtime(updated_time))+f"-{title}.html"), 'w', encoding='utf-8') as f:
        f.write(content)
def get_list():
    # url = 'https://www.zhihu.com/api/v4/columns/%s/articles?include=data[*].topics&limit=10' % author
    url = f'https://www.zhihu.com/api/v4/columns/{author}/items?limit=10&offset=0'
    article_dict = {}
    encoding = 'utf-8-sig'
    while True:
        # print('抓取中', url)
        try:
            ts=str(int(time.time()))
            resp = requests.get(url, headers=headers)#;print(headers,url,resp.json())
            content = resp.content.decode("utf-8")
            j = json.loads(content)
            #j = resp.json()
            data = j['data']
        except:
            print('抓取失败')

        for article in data:
            aid = article['id']
            akeys = article_dict.keys()
            # if aid not in akeys and article['type'] == 'article':
                # article_dict[aid] = article['title']
            if article['type'] == 'zvideo':
               video(article['id'],replace_invalid_chars(article['title']))
               with open('知乎专栏列表.csv', 'a+', encoding=encoding) as f:
                    f.write('视频' + ','+trimName(article['title']) + ','+'https://www.zhihu.com/zvideo/'+str(article['id'])+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['created_at']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['updated_at']))+','+article['description']+','+str(article['comment_count'])+ ','+str(article['voteup_count'])+'\n')
            if article['type'] == 'answer':
               answer(article['content'], replace_invalid_chars(article['question']['title']), article['updated_time'])
               with open('知乎专栏列表.csv', 'a+', encoding=encoding) as f:
                    f.write('回答' + ','+trimName(article['question']['title']) + ','+'https://www.zhihu.com/question/'+str(article['question']['id'])+'/answer/'+str(article['id'])+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['created_time']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['updated_time']))+','+article['excerpt']+','+str(article['comment_count'])+ ','+str(article['voteup_count'])+'\n')
            if article['type'] == 'article':
               articles(article['content'], replace_invalid_chars(article['title']), article['updated'])
               with open('知乎专栏列表.csv', 'a+', encoding=encoding) as f:
                    f.write('文章' + ','+trimName(article['title']) + ','+article['url']+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['created']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['updated']))+','+article['excerpt']+','+str(article['comment_count'])+ ','+str(article['voteup_count'])+'\n')
        if j['paging']['is_end']:
            break
        url = j['paging']['next'].replace('http','https')
        time.sleep(2)

    # with open('zhihu_ids.txt', 'w', encoding='utf-8') as f:
    #     items = sorted(article_dict.items())
    #     for item in items:
    #         f.write('%s %s\n' % item)
def get_top_list():
    # url = 'https://www.zhihu.com/api/v4/columns/%s/articles?include=data[*].topics&limit=10' % author
    url = f'https://www.zhihu.com/api/v4/columns/{author}/pinned-items'
    article_dict = {}
    encoding = 'utf-8-sig'
    while True:
        # print('抓取中', url)
        try:
            resp = requests.get(url, headers=headers)
            content = resp.content.decode("utf-8")
            j = json.loads(content)
            #j = resp.json()
            data = j['data']
        except:
            print('抓取失败')

        for article in data:
            aid = article['id']
            akeys = article_dict.keys()
            # if aid not in akeys and article['type'] == 'article':
                # article_dict[aid] = article['title']
            if article['type'] == 'zvideo':
               video(article['id'],replace_invalid_chars(article['title']))
               with open('知乎专栏列表.csv', 'a+', encoding=encoding) as f:
                    f.write('视频' + ','+trimName(article['title']) + ','+'https://www.zhihu.com/zvideo/'+str(article['id'])+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['created_at']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['updated_at']))+','+article['description']+','+str(article['comment_count'])+ ','+str(article['voteup_count'])+'\n')
            if article['type'] == 'answer':
               answer(article['content'], replace_invalid_chars(article['question']['title']), article['updated_time'])
               with open('知乎专栏列表.csv', 'a+', encoding=encoding) as f:
                    f.write('回答' + ','+trimName(article['question']['title']) + ','+'https://www.zhihu.com/question/'+str(article['question']['id'])+'/answer/'+str(article['id'])+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['created_time']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['updated_time']))+','+article['excerpt']+','+str(article['comment_count'])+ ','+str(article['voteup_count'])+'\n')
            if article['type'] == 'article':
               articles(article['content'], replace_invalid_chars(article['title']), article['updated'])
               with open('知乎专栏列表.csv', 'a+', encoding=encoding) as f:
                    f.write('文章' + ','+trimName(article['title']) + ','+article['url']+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['created']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['updated']))+','+article['excerpt']+','+str(article['comment_count'])+ ','+str(article['voteup_count'])+'\n')
        break
        time.sleep(2)
def get_html(aid, title, index):
    if not os.path.exists('html'):
        os.mkdir('html')
    title = title.replace('/', '／')
    title = title.replace('\\', '＼')
    file_name = f'html/{title}.html'
    if os.path.exists(file_name):
        print(title, '已经存在')
        return
    else:
        print('下载文章:', title)
    try:
        url = 'https://zhuanlan.zhihu.com/p/' + aid
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='Post-RichText').prettify()
        content = content.replace('data-actual', '')
        content = content.replace('h1>', 'h2>')
        content = re.sub(r'<noscript>.*?</noscript>', '', content)
        content = re.sub(r'src="data:image.*?"', '', content)
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1>%s</body></html>' % (
            title, content)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
    except:
        print('下载文章 %s 失败', title)
    time.sleep(2)

def get_details():
    with open('zhihu_ids.txt', encoding='utf-8') as f:
        i = 1
        for line in f:
            lst = line.strip().split(' ')
            aid = lst[0]
            title = '_'.join(lst[1:])
            get_html(aid, title, i)
            i += 1

def to_pdf():
    import pdfkit
    print('合成PDF：')
    htmls = []
    # os.system('cd html')
    for root, dirs, files in os.walk('./html'):
        htmls += ['html/'+name for name in files if name.endswith(".html")]
    htmls.sort(reverse = True)
    print(htmls)
    pdfkit.from_file(htmls, '知乎专栏合集.pdf')

if __name__ == '__main__':
    print('本工具更新于2024年5月25日，获取最新版本请关注公众号苏生不惑')
    url = input('公众号苏生不惑提示你输入知乎专栏链接:')
    if not url:
        url = 'https://www.zhihu.com/column/c_1721130763582382082'#https://www.zhihu.com/column/c_161945759
    cookie = input('公众号苏生不惑提示你输入知乎cookie:')
    author = re.search(r'https?://www.zhihu.com/column/(.*)',url).group(1)
    headers = {
        'origin': 'https://zhuanlan.zhihu.com',
        'referer': 'https://zhuanlan.zhihu.com/%s' % author,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 FirePHP/0.7.4',
        'cookie':cookie
    }

    with open('知乎专栏列表.csv', 'a+', encoding='utf-8-sig') as f:
        f.write('类型' + ','+'标题' + ','+'链接'+ ','+'创建时间'+ ','+'更新时间'+','+'简介'+','+'评论数'+ ','+'赞同数'+'\n')
    get_top_list()
    get_list()
    to_pdf()