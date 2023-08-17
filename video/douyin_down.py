# -*- coding: utf-8 -*-
import requests
import time
import json,html
import random,re,os,csv
requests.packages.urllib3.disable_warnings()
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
fname=input("请输入文件名：")
# 油猴脚本抓取视频地址 https://greasyfork.org/scripts/471880
# https://v.douyin.com/rWa6bh8/
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xea in position 0: invalid continuation byte gb18030 ISO-8859-1
f = open(f'{fname}', encoding='gbk')
csv_reader = csv.reader(f)
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
def down(title,date,url):
	try:
		if not os.path.exists('douyin'):
			os.mkdir('douyin')
		print('开始下载视频：',date,title)
		video_data = requests.get(url,headers=headers)
		with open('douyin/'+date.replace('/','-').replace(' ','')+'_'+trimName(title)+'.mp4','wb') as f:
			f.write(video_data.content)
	except Exception as e:
		print('出错了',e)
for line in csv_reader:
    # print(line)
    if len(line) == 0:
       continue
    if line[6] == "年龄" or line[6] == "" or line[6] == "下载链接":
        continue
    res = down(line[0],line[5][0:10],line[6])
    if not res:
       continue
    if res == "error":
       break
