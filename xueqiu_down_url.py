import re,requests,os,html,random
import traceback,urllib3,time,sys,json
import pandas as pd
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
num = 1
def get_history():
    history = []
    with open('xueqiu_history.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('xueqiu_history.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def get_cookie():
    cookie = ''
    if os.path.exists('cookie.txt'):
        with open('cookie.txt', encoding='utf-8') as f:
            cookie = f.read().replace('\n','')
    return cookie
urls_history = get_history()
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def str_to_time(text):
    if ':' in text:
        result = time.strptime(text, '%Y-%m-%d %H:%M:%S')
    else:
        result = time.strptime(text, '%Y-%m-%d')
    return time.mktime(result)
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def down(url):
    try:
        if url in urls_history:
            print('已经下载过：',url)
            return ''
        res = requests.get(url, headers=headers)
        try:
            timestamp = re.search(r'data-created_at="(.*?)"', res.text).group(1)
            date = time.strftime('%Y-%m-%d %H%M%S', time.localtime(int(timestamp) / 1000))
            date2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp) / 1000))
            soup = BeautifulSoup(res.text, 'html.parser')
            titlesoup = soup.find("h1", {"class": "article__bd__title"})
            article_json = re.findall(r'<script>window\.SNOWMAN_STATUS = (.*?);\n',res.text,flags=re.S)
            data = json.loads(article_json[0])
            title = data['title']
            # if titlesoup:
            #     title = titlesoup.get_text()
            article_html = re.search(r'<article class="article__bd">(.*)</article>', res.text).group(1)#.replace('.png!800.jpg','.png!raw.jpg') #data['text']
            if not title:
                # title = soup.find("article", {"class": "article__bd"}).get_text() 
                title = re.sub(r'<.*?>', '', data['description'])
            if len(title) > 100:
                title = title[0:64]
            retweeted = ''
            if data['retweeted_status']:
                user_id = data['retweeted_status']['user_id']
                user_name = data['retweeted_status']['user']['screen_name']
                timeBefore = data['retweeted_status']['timeBefore']
                retweet_count =  data['retweeted_status']['retweet_count']
                reply_count =  data['retweeted_status']['reply_count']
                like_count =  data['retweeted_status']['like_count']
                retweeted = f'<br><div class="timeline__item__forward__hd"><a href="https://xueqiu.com/{user_id}" target="_blank" data-tooltip="{user_id}" analytics-data="&quot;&quot;" class="user-name-link"><span class="user-name">@{user_name}</span><span><h-char unicode="ff1a" class="biaodian cjk bd-end bd-jiya"><h-inner>：</h-inner></h-char></span></a></div><div class="timeline__item__forward__content">'+data['retweeted_status']['text']+f'</div><br><div class="timeline__item__forward__ft"><span class="timestamp">{timeBefore}</span><span class="retweet-count"> <h-char unicode="b7" class="biaodian cjk bd-middle bd-jiya"><h-inner>·</h-inner></h-char> 转发 {retweet_count}</span><a href="/8852934528/312437395#comment" target="_blank" class="replay-count"> <h-char unicode="b7" class="biaodian cjk bd-middle bd-jiya"><h-inner>·</h-inner></h-char> 讨论 {reply_count}</a><span class="like-count"> <h-char unicode="b7" class="biaodian cjk bd-middle bd-jiya"><h-inner>·</h-inner></h-char> 赞 {like_count}</span><!----></div>'
                image = ''
                # 转发图片?
                if data['retweeted_status']['pic']:
                    pics = data['retweeted_status']['pic'].split(',')
                    for pic in pics:
                        imageUrl = pic.replace('thumb.jpg','raw.jpg')
                        image += f'<br><img data-src="{imageUrl}" src="{imageUrl}" lazy="loaded">'
                retweeted += image
            if not title:
                title = re.search(r'https://xueqiu.com/\d+/(\d+)', url).group(1)
            image = ''
            # 分享图片帖子
            if data['pic'] and not data['title']:
                pics = data['pic'].split(',')
                for pic in pics:
                    imageUrl = pic.replace('thumb.jpg','raw.jpg')
                    image += f'<br><img data-src="{imageUrl}" src="{imageUrl}" lazy="loaded">'
            article_html = '<h4 class="">发布时间：'+date2+'</h4>'+article_html+retweeted+image
            article_content = f'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div class="article-content">{article_html}</article></div></body></html>'
            # article_content=res.text
            print('开始下载',url,title)
            save_history(url)
            with open(f'雪球帖子目录.md', 'a+', encoding='utf-8') as f2:
                f2.write('[{}]'.format(date+'_'+html.unescape(title)) + '({})'.format(url)+ '\n\n')
            with open(f'html/'+date+'_'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
                f.write(article_content.replace('<p style="display:none;">','<p style="">'))
        except Exception as err:
            print('出错了',err,url);raise Exception("抓取失败了："+url)
        return ''
    except Exception as e:
        with open(f'下载失败雪球列表.txt', 'a+', encoding='utf-8') as f:
            f.write(url+'\n')
        print('下载雪球失败', url,e);raise Exception("抓取失败了："+url)
        return ''

cookie = get_cookie()
if not cookie:
    cookie = input('公众号玩转互联网达人提示你，请输入雪球cookie：')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 FirePHP/0.7.4",
    'cookie':cookie
    }
if not os.path.exists('html'):
    os.mkdir('html')
# 正则替换 /1505944393/(\d{8,9}).* /1505944393/\1 断网调试：点击network，勾选offline即可断开网络 修改成No throttling无限速模式再刷新恢复网络document.querySelector('a.pagination__next').click();
filename = input('请输入雪球excel文件名：')
with open(f'{filename}.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('时间'+','+'链接' + ','+'转发数'+ ','+'点赞数'+ ','+'评论数'+'\n')
# filename='xueqiu.xlsx'
if not os.path.exists(filename):
    sys.exit('文件不存在')
file_name, file_extension = os.path.splitext(filename)
if file_extension == '.xlsx':
    df=pd.read_excel(filename)
    print('列标题',df.columns)
    print('行标题',df.index)
    for index, row in df.iterrows():
        if not row['雪球链接']:
            continue
        if 'https://xueqiu.com'+row['雪球链接'] in get_history():
            print('已经下载过：','https://xueqiu.com'+row['雪球链接'])
            continue
        time.sleep(1)
        t=down('https://xueqiu.com'+row['雪球链接'])
        repost=str(row['转发数'])
        fav = str(row['点赞数'])
        comment = str(row['评论数'])
        itemtime = str(row['雪球时间'])
        if comment == 'nan':
            comment = '0'
        if fav == 'nan':
            fav='0'
        if itemtime == 'nan':
            itemtime='0'
        with open(f'{filename}.csv', 'a+', encoding='utf-8-sig') as f:
            f.write(itemtime+','+'https://xueqiu.com'+row['雪球链接'] + ','+repost+ ','+fav+ ','+comment+'\n')
    # for i in tqdm(df['雪球链接'].tolist(), desc='下载进度'):
    #     t=down('https:'+i)
        # break
elif file_extension == '.txt':
    with open(f'{filename}', encoding='utf-8') as f:
        contents = f.read()
    urls=contents.split('\n')
    for item in urls:
        if 'https://xueqiu.com' not in item:
            item = 'https://xueqiu.com'+item
        if item in get_history():
            print('已经下载过：',item)
            continue
        down(item)
        time.sleep(random.randint(1,2))

