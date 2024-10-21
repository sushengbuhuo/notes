import requests
import time
import json,html
import random,re,os,csv
requests.packages.urllib3.disable_warnings()
#热榜 每天60秒api 新闻早报api
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://api.oioweb.cn/api/common/HotList',
    }
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
# https://www.zhihu.com/people/mt36501/posts  https://xlog.viki.moe/60s?locale=zh https://api.zxki.cn/ https://api.southerly.top/ https://api.vvhan.com
fname='新闻早报'
with open(f'{fname}.md', 'w') as file:
    file.truncate(0)

with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
    file.write('### 新闻早报\n\n')
fname2='历史上的今天'
with open(f'{fname2}.md', 'w') as file:
    file.truncate(0)
with open(f'{fname2}.md', 'a+', encoding='utf-8') as file:
    file.write('### 历史上的今天\n\n')
def oioweb():
	url='https://api.oioweb.cn/api/common/today'
	response = requests.get(url,headers=headers).json()
	print('新闻早报',response['code'])
	for item in response['result']['news']:
		with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
			f.write(item[:-1]+ '\n\n')
	with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
	    file.write('### 微博热搜\n\n')
	url='https://api.oioweb.cn/api/common/HotList'
	response = requests.get(url,headers=headers).json()
	print('微博热搜',response['code'])
	num=0
	for item in response['result']['微博']:
		num+=1
		if num > 15:
			continue
		with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
			f.write(str(num)+'、[{}]'.format(html.unescape(item['title'])) + '({})'.format(item['href'])+ '\n\n')
	# for item in response['result']['微信']:
	# 	with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
	# 		f.write('[{}]'.format(html.unescape(item['title'])) + '({})'.format(item['href'])+ '\n\n')
	with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
	    file.write('### 知乎热搜\n\n')
	num=0
	for item in response['result']['知乎']:
		num+=1
		with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
			f.write(str(num)+'、'+html.unescape(item['title'])+ ' '+item['href']+ '\n\n')

	url='https://api.oioweb.cn/api/bing'
	response = requests.get(url,headers=headers).json()
	print('今日壁纸',response['code'])
	with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
		f.write('### 今日壁纸\n\n')
		f.write(response['result'][0]['url']+ '\n\n')
	url='https://api.oioweb.cn/api/SoulWords'
	response = requests.get(url,headers=headers).json()
	print('今日段子',response['code'])
	with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
		f.write('### 今日段子\n\n')
		# f.write("https://tool.lu/timestamp/"+ '\n\n')
		f.write(response['result']['content']+ '\n\n')

	url='https://api.oioweb.cn/api/common/history'
	response = requests.get(url,headers=headers).json()
	print('历史上的今天',response['code'])
	num=0
	for item in response['result']:
		num+=1
		with open(f'{fname2}.md', 'a+', encoding='utf-8') as f:
			f.write(str(num)+'、'+item['year']+'年'+item['title']+ '\n\n'+remove_html_tags(item['desc'])+ '。。。\n\n')
def vvhan():
	url='https://api.zxki.cn/api/mrzb' # https://api.southerly.top/api/60s?format=json alapi.cn https://github.com/vikiboss/60s  https://60s.viki.moe/60s?v2=1
	response = requests.get(url,headers=headers).json()
	print('新闻早报',response['code'])
	for item in response['data']['news']:
		with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
			f.write(item[:-1]+ '\n\n')
	with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
	    file.write('### 微博热搜\n\n')
	url='https://api.vvhan.com/api/hotlist/all'
	response = requests.get(url,headers=headers).json()
	print('微博热搜',response['success'])
	if response['data'][0]['name'] == '微博':
		num=0
		for item in response['data'][0]['data']:
			num+=1
			if num > 15:
				continue
			with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
				f.write(str(num)+'、[{}]'.format(html.unescape(item['title'])) + '({})'.format(item['url'])+ '\n\n')
	with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
	    file.write('### 知乎热搜\n\n')
	if response['data'][3]['name'] == '知乎热榜':
		num=0
		for item in response['data'][3]['data']:
			num+=1
			with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
				f.write(str(num)+'、'+html.unescape(item['title'])+ ' '+item['url']+ '\n\n')
	with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
	    file.write('### 百度热搜\n\n')
	if response['data'][7]['name'] == '百度热点':
		num=0
		for item in response['data'][7]['data']:
			num+=1
			if num > 15:
				continue
			with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
				f.write(str(num)+'、[{}]'.format(html.unescape(item['title'])) + '({})'.format(item['url'])+ '\n\n')
	url='https://api.vvhan.com/api/bing?type=json' # 
	response = requests.get(url,headers=headers).json()
	print('今日壁纸',response['success'])
	with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
		f.write('### 今日壁纸\n\n')
		f.write(response['data']['url']+ '\n\n')
	url='https://api.vvhan.com/api/text/joke?type=json'
	response = requests.get(url,headers=headers).json()
	print('今日段子',response['success'])
	with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
		f.write('### 今日段子\n\n')
		# f.write("https://tool.lu/timestamp/"+ '\n\n')
		f.write(response['data']['content']+ '\n\n')

	url='https://60s.viki.moe/today_in_history' # https://api.southerly.top/api/today?format=json https://60s.coolsong.com/today_in_history
	response = requests.get(url,headers=headers).json()
	print('历史上的今天',response['status'])
	num=0
	for item in response['data']:
		num+=1
		with open(f'{fname2}.md', 'a+', encoding='utf-8') as f:
			f.write(str(num)+'、'+item['year']+'年'+item['title']+ '\n\n'+remove_html_tags(item['desc'])+ '。。。\n\n')
vvhan()
with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
    file.write('\n\n来源:央视、人民日报、腾讯、新浪、新华网、微博、知乎\n\n')
   