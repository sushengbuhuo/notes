import re,requests,os,html
import traceback,urllib3,time,sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)",
    "Cookie":""
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def articles(user_id,page):
    url = f'https://xueqiu.com/statuses/original/timeline.json?user_id={user_id}&page={page}'
    res=requests.get(url, headers=headers, verify=False).json()
    if not res.get('list'):
        print(res)
        return False
    if len(res["list"]) > 0:
        for v in res["list"]:
            date = v['timeBefore']
            res = requests.get('https://xueqiu.com'+v['target'],verify=False, headers=headers)
            try:
                comments_html = re.search(r'<article class="article__bd">(.*)</article>', res.text).group(1)
                
                article_content = f'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div class="article-content">{comments_html}</article></div></body></html>'
                with open('html/'+date[0:10]+trimName(v['title'])+'.html', 'w', encoding='utf-8') as f:
                    f.write(article_content)
            except Exception as err:
                print('出错了',err,'https://xueqiu.com'+v['target'])
                with open('html/'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                    f.write(article_content)
            with open(f'雪球专栏文章数据.csv', 'a+', encoding='utf-8-sig') as f:
                f.write(v['timeBefore']+','+trimName(v['title']) + ','+'https://xueqiu.com'+v['target']+ ','+trimName(v['description'])+ ','+str(v['view_count'])+'\n')
    return True 
url = input('请输入雪球专栏链接：')
if not url:
	url = 'https://xueqiu.com/1758860965/column'
	# sys.exit('链接为空')
user_id = re.search('xueqiu.com/(\d+)',url).group(1)
if not os.path.exists('html'):
    os.mkdir('html')
page = 1
with open(f'雪球专栏文章数据.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+','+'文章简介'+ ','+'阅读数'+'\n')
while True:
    print("页数：",page)
    res = articles(user_id,page)
    time.sleep(1)
    if not res:
        break
    page+=1


