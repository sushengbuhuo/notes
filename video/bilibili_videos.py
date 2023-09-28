import requests,re,os,time,sys,html,urllib3,time
from random import randint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 FirePHP/0.7.4",
        "cookie":""
}
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')    
encoding = 'utf-8-sig'
fname = f'哔哩哔哩视频列表.csv'
with open(fname, 'a+', encoding=encoding) as f:
    f.write('日期'+','+'标题' + ','+'链接'+ ','+'封面'+ ','+'播放数'+ ','+'评论数'+ ','+'简介'+ ','+'长度'+'\n')
def download(uid,page,headers):
	t=time.time()
	url=f'https://api.bilibili.com/x/space/wbi/arc/search?mid={uid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=07c9a7ac20586118a75a5e314a4602f5&wts={t}'
	print(url)
	page+=1
	try:
		res=requests.get(url,headers=headers).json()
		# print(res)
		if not res['data']['list']['vlist']:
			return True
		for item in res['data']['list']['vlist']:
			date = time.strftime('%Y-%m-%d', time.localtime(item['created']))
			vid = item['bvid']
			with open(fname, 'a+', encoding=encoding) as f:
				f.write(date+','+trimName(item['title'])+','+f'https://www.bilibili.com/video/{vid}/'+','+item['pic']+','+str(item['play'])+','+str(item['comment'])+','+trimName(item['description'])+','+item['length']+'\n')
		time.sleep(1)
		download(uid,page,headers)
	except Exception as e:
		print(url,e)
# https://space.bilibili.com/927587/video https://www.52pojie.cn/thread-1761801-1-1.html
url=input("公众号苏生不惑提示你，请输入b站up主链接：")
if not url:
	sys.exit("链接为空")
uid=re.search(r'https://space.bilibili.com/(\d+)',url).group(1)
download(uid,1,headers)