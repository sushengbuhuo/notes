import time,sys,random
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
    url = f'https://www.zhihu.com/api/v4/collections/{collection_id}/items?limit=10&offset=0'
    article_dict = {}
    encoding = 'utf-8-sig'
    num = 0
    while True:
        # print('抓取中', url)
        try:
            ts=str(int(time.time()))
            resp = requests.get(url, headers=headers)#;print(headers,url,resp.json())
            content = resp.content.decode("utf-8")
            j = json.loads(content)
            #j = resp.json()
            data = j['data']
        except Exception as e:
            print('抓取失败',e)
        num = num+len(data)
        if num > 2000:
            break
        for article in data:
            aid = article['content']['id']
            akeys = article_dict.keys()
            # if aid not in akeys and article['type'] == 'article':
                # article_dict[aid] = article['title']
            if article['content']['type'] == 'zvideo':
               video(article['content']['id'],replace_invalid_chars(article['content']['title']))
               with open('知乎收藏夹列表目录.csv', 'a+', encoding=encoding) as f:
                    f.write('视频' + ','+trimName(article['content']['title']) + ','+'https://www.zhihu.com/zvideo/'+str(article['content']['id'])+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['content']['created_at']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['content']['updated_at']))+','+article['content']['description']+','+str(article['content']['comment_count'])+ ','+str(article['content']['voteup_count'])+'\n')
            if article['content']['type'] == 'answer':
               answer(article['content']['content'], replace_invalid_chars(article['content']['question']['title']), article['content']['updated_time'])
               with open('知乎收藏夹列表目录.csv', 'a+', encoding=encoding) as f:
                    f.write('回答' + ','+trimName(article['content']['question']['title']) + ','+'https://www.zhihu.com/question/'+str(article['content']['question']['id'])+'/answer/'+str(article['content']['id'])+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['content']['created_time']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['content']['updated_time']))+','+article['content']['excerpt']+','+str(article['content']['comment_count'])+ ','+str(article['content']['voteup_count'])+'\n')
            if article['content']['type'] == 'article':
               articles(article['content']['content'], replace_invalid_chars(article['content']['title']), article['content']['updated'])
               with open('知乎收藏夹列表目录.csv', 'a+', encoding=encoding) as f:
                    f.write('文章' + ','+trimName(article['content']['title']) + ','+article['content']['url']+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['content']['created']))+ ','+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(article['content']['updated']))+','+article['content']['excerpt_title']+','+str(article['content']['comment_count'])+ ','+str(article['content']['voteup_count'])+'\n')
        if j['paging']['is_end']:
            break
        url = j['paging']['next']
        time.sleep(random.randint(3,6))

    # with open('zhihu_ids.txt', 'w', encoding='utf-8') as f:
    #     items = sorted(article_dict.items())
    #     for item in items:
    #         f.write('%s %s\n' % item)

def to_pdf():
    import pdfkit
    print('合成PDF：')
    htmls = []
    # os.system('cd html')
    for root, dirs, files in os.walk('./html'):
        htmls += ['html/'+name for name in files if name.endswith(".html")]
    htmls.sort(reverse = True)
    print(htmls)
    pdfkit.from_file(htmls, '知乎收藏夹合集.pdf')

if __name__ == '__main__':
    print('本工具更新于2024年6月6日，获取最新版本请关注公众号苏生不惑')
    url = input('公众号苏生不惑提示你输入知乎收藏夹链接:')
    if not url:
        url = 'https://www.zhihu.com/collection/40047806'
    cookie = input('公众号苏生不惑提示你输入知乎cookie:')
    collection_id = re.search(r'https?://www.zhihu.com/collection/(.*)',url).group(1)
    headers = {
        'origin': 'https://zhuanlan.zhihu.com',
        'referer': 'https://www.zhihu.com/collection/%s' % collection_id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 FirePHP/0.7.4',
        'cookie':cookie
    }

    with open('知乎收藏夹列表目录.csv', 'a+', encoding='utf-8-sig') as f:
        f.write('类型' + ','+'标题' + ','+'链接'+ ','+'创建时间'+ ','+'更新时间'+','+'简介'+','+'评论数'+ ','+'赞同数'+'\n')
    get_list()
    to_pdf()