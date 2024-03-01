import requests,re,csv,time,random,urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def count_csv_rows(filename):
    with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        row_count = sum(1 for row in csv_reader)
    return row_count
def repost(mid,page,headers):
	num=count_csv_rows(f'{mid}微博转发.csv')
	if num > 5000:
		return False
	url=f'https://www.weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page}&moduleID=feed&count=20'
	res=requests.get(url, headers=headers, verify=False).json()
	if page > 100 and not res["data"]:
		print(res,url)
		return False
	for v in res["data"]:
		parsed_datetime = datetime.strptime(v['created_at'], "%a %b %d %H:%M:%S %z %Y")#Mon Nov 06 14:06:06 +0800 2023
		formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
		try:
			soup = BeautifulSoup(v['source'], 'html.parser')
			source = soup.text#删除HTML标签
			with open(f'{mid}微博转发.csv', 'a+', encoding='utf-8-sig') as f:
				f.write(trimName(v['user']['screen_name'])+','+trimName(v['user']['idstr']) + ','+formatted_datetime+ ','+trimName(v['text_raw'])+ ','+v['region_name']+ ','+trimName(source)+ ','+str(v['reposts_count'])+ ','+str(v['comments_count'])+ ','+str(v['attitudes_count'])+'\n')
		except Exception as e:
			print(e)

	return True
page = 1
mid=input('请输入微博mid：')
if not mid:
	sys.exit('mid为空')
cookie=input('请输入微博cookie：')
if not cookie:
	sys.exit('cookie为空')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 FirePHP/0.7.4',
        'Cookie': cookie
               # 'Referer': 'https://m.weibo.cn/detail/4497103885505673',
               # 'Sec-Fetch-Mode': 'navigate'
    }
with open(f'{mid}微博转发.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('微博昵称'+','+'微博uid' + ','+'转发时间'+','+'转发内容'+','+'转发地区'+','+'转发来源'+','+'转发数'+','+'评论数'+','+'点赞数'+ '\n')
while True:
    print(f"开始抓取第{page}页")
    res = repost(mid,page,headers)
    time.sleep(1)
    if not res:
        break
    page+=1
print('抓取结束')