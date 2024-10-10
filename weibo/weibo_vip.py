import requests,re,os,time,html,sys,csv
import random
import traceback,urllib3
from docx import Document
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ').replace('"', '“')
import csv


# 导出数据到 CSV 文件
# with open('data.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(data)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://weibo.com/1744395855/NkD5bjvPC',
        "Cookie":'',
    }
with open('峰哥谋略微博v+.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('时间' + ','+'标题' + ','+'链接'+ ','+'封面'+ '\n')
# https://vipclub.e.weibo.com/aj/vmember/contentlist?tab_type=0&content_type=0&page=2&page_size=20&vuid=2137412980&F=&weibo_client_from=&_lid=65889756106501001
def  vip2(page):
	if page > 10:
		return True
	url=f'https://vipclub.e.weibo.com/aj/vmember/contentlist?tab_type=0&content_type=0&page={page}&page_size=20&vuid=2137412980&F=&weibo_client_from=&_lid=65889756106501000'
	print('开始下载：',url)
	res = requests.get(html.unescape(url),proxies={'http': None,'https': None},verify=False, headers=headers).json()
	if not res['data']['list']:
		print('over')
		return True
	data=[]
	for item in res['data']['list']:
		# print(item['title'],item['url'],item['poster'])
		data.append([item['title'],'https:'+item['url'],'https:'+item['poster'],item['page_view']])
		# with open('峰哥谋略微博vip.csv', 'a+', encoding='utf-8-sig') as f:
			# f.write(trimName(item['title'])+','+'https:'+item['url'] + ','+'https:'+item['poster']+ ','+item['page_view']+'\n')
	print(data)
	with open('峰哥谋略微博v+.csv', 'a+', encoding='utf-8-sig') as file:
		writer = csv.writer(file)
		writer.writerows(data)
	page+=1
	time.sleep(1)
	vip(page)
# vip(1)
def  vip(page,uid):
	# if page > 5:
	# 	return True
	url=f'https://vipclub.weibo.com/aj/vmember/gfcontent?page={page}&type=0&cid=&vuid={uid}&sort=desc&page_size=8&weibo_client_from=&_lid=71632018307201019'
	print('开始下载：',url)
	res = requests.get(html.unescape(url),proxies={'http': None,'https': None},verify=False, headers=headers).json()
	if not res['data']['list']:
		print('over')
		return True
	data=[]
	for item in res['data']['list']:
		# print(item['title'],item['url'],item['poster'])
		poster = ''
		if item['poster']:
			poster = 'https:'+item['poster']
		title=item['title']
		mid=item['mid']
		created_at = item['date']
		url=f'https://weibo.com/ajax/statuses/show?id={mid}&locale=zh-CN'
		try:
			res = requests.get(html.unescape(url),proxies={'http': None,'https': None},verify=False, headers=headers).json()
			if res['ok'] == 1:
				dt_obj = datetime.strptime(res['created_at'], '%a %b %d %H:%M:%S %z %Y')
				created_at = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
				title=res['text_raw']
		except Exception as e:
			print('错误',e,item);raise Exception(e)
		data.append([created_at,title,'https:'+item['url'],poster])
		# with open('峰哥谋略微博v+.csv', 'a+', encoding='utf-8-sig') as f:
			# f.write(trimName(item['title'])+','+'https:'+item['url'] + ','+'https:'+item['poster']+ ','+item['page_view']+'\n')
	# print(data)
	with open('峰哥谋略微博v+.csv', 'a+', newline='', encoding='utf-8-sig') as file:
		writer = csv.writer(file)
		writer.writerows(data)
	page+=1
	time.sleep(random.randint(2, 6))
	vip(page)
vip(1,2137412980)