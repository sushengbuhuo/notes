import re,requests,os,html,random
import traceback,urllib3,time,sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
num = 1
def str_to_time(text):
    if ':' in text:
        result = time.strptime(text, '%Y-%m-%d %H:%M:%S')
    else:
        result = time.strptime(text, '%Y-%m-%d')
    return time.mktime(result)
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def articles(user_id,page,tp,headers,since,over):
    url = f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page={page}'
    if int(tp) > 0:
        url = f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page={page}&type=2'
    res=requests.get(url, headers=headers, verify=False).json()
    global num
    if not res.get('statuses'):
        print(res.get('error_description'))
        return False
    if len(res["statuses"]) > 0:
        for v in res["statuses"]:
            date = time.strftime('%Y-%m-%d', time.localtime(v['created_at'] / 1000))
            # if num > 200:
            #     print('下载完成')
            #     return False
            if (v['created_at'] / 1000) > str_to_time(over):
                continue
            if v['mark'] == 0 and (v['created_at'] / 1000) < str_to_time(since):
                return False
            res = requests.get('https://xueqiu.com'+v['target'],verify=False, headers=headers)
            if not v['title']:
                v['title'] = str(v['id'])
            try:
                comments_html = re.search(r'<article class="article__bd">(.*)</article>', res.text).group(1)
                
                article_content = f'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div class="article-content">{comments_html}</article></div></body></html>'
                # article_content=res.text
                with open('xueqiu/'+date+'_'+trimName(v['title'])+'.html', 'w', encoding='utf-8') as f:
                    f.write(article_content)
            except Exception as err:
                print('出错了',err,'https://xueqiu.com'+v['target'])
                with open('xueqiu/'+date+'_'+str(random.randint(1,10000))+'.html', 'w', encoding='utf-8') as f:
                    f.write(res.text)
            print(f'开始下载第{num}条数据',date,trimName(v['title']),'https://xueqiu.com'+v['target'])
            num +=1
            with open(f'雪球文章数据.csv', 'a+', encoding='utf-8-sig') as f:
                f.write(date+','+trimName(v['title']) + ','+'https://xueqiu.com'+v['target']+ ','+trimName(v['description'])+ ','+str(v['like_count'])+ ','+str(v['retweet_count'])+ ','+str(v['reply_count'])+'\n')
    return True 
url = input('公众号苏生不惑提示你，请输入雪球主页链接：')
if not url:
	url = 'https://xueqiu.com/u/4104161666'
	sys.exit('链接为空')
cookie = input('公众号苏生不惑提示你，请输入雪球cookie：')
tp=input('公众号苏生不惑提示你，是否只下载长文：')
since=input('公众号苏生不惑提示你，输入开始时间：')
over=input('公众号苏生不惑提示你，输入结束时间：')
if not cookie:
    sys.exit('cookie为空')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 FirePHP/0.7.4",
    }

headers['Cookie'] = cookie
user_id = re.search('xueqiu.com/u/(\d+)',url).group(1)
if not os.path.exists('xueqiu'):
    os.mkdir('xueqiu')
page = 1

with open(f'雪球文章数据.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+','+'文章简介'+ ','+'点赞数'+ ','+'转发数'+ ','+'评论数'+'\n')
while True:
    print("页数：",page)
    res = articles(user_id,page,tp,headers,since,over)
    time.sleep(2)
    if not res:
        break
    page+=1


