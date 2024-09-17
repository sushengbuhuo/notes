import requests
import time
import json,html
import random,re,os,csv
requests.packages.urllib3.disable_warnings()
#热榜 
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://api.oioweb.cn/api/common/HotList',
    }
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

fname='新闻早报'
with open(f'{fname}.md', 'w') as file:
    file.truncate(0)

with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
    file.write('### 新闻早报\n\n')
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
with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
    file.write('### 百度热搜\n\n')
num=0
for item in response['result']['百度']:
	num+=1
	if num > 15:
		continue
	with open(f'{fname}.md', 'a+', encoding='utf-8') as f:
		f.write(str(num)+'、[{}]'.format(html.unescape(item['title'])) + '({})'.format(item['href'])+ '\n\n')
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
fname2='历史上的今天'
with open(f'{fname2}.md', 'w') as file:
    file.truncate(0)
url='https://api.oioweb.cn/api/common/history'
with open(f'{fname2}.md', 'a+', encoding='utf-8') as file:
    file.write('### 历史上的今天\n\n')
response = requests.get(url,headers=headers).json()
print('历史上的今天',response['code'])
num=0
for item in response['result']:
	num+=1
	with open(f'{fname2}.md', 'a+', encoding='utf-8') as f:
		f.write(str(num)+'、'+item['year']+'年'+item['title']+ '\n\n'+remove_html_tags(item['desc'])+ '。。。\n\n')
with open(f'{fname}.md', 'a+', encoding='utf-8') as file:
    file.write('来源:央视、人民日报、腾讯、新浪、新华网、微博、知乎\n\n')