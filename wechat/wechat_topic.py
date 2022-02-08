import requests,re,os,time,sys
from random import randint
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
biz = 'MzUyMzUyNzM4Ng=='
album_id = '2091728990028824579'
topic_url = f'https://mp.weixin.qq.com/mp/appmsgalbum?__biz={biz}&action=getalbum&album_id={album_id}&scene=173&from_msgid=2247507484&from_itemidx=1&count=3&nolastread=1'
# 音频话题 https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzkzNTI5NTc5NQ==&action=getalbum&album_id=2145881553845944326&scene=173&from_msgid=2247507484&from_itemidx=1&count=3&nolastread=1
# 文章话题 https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzUyMzUyNzM4Ng==&action=getalbum&album_id=2091728990028824579&scene=173&from_msgid=2247507484&from_itemidx=1&count=3&nolastread=1#wechat_redirect
# 整理文章 https://mp.weixin.qq.com/s/8_Us3Qe7HRsyMYvFWNHF4A
# url = 'https://mp.weixin.qq.com/s/8_Us3Qe7HRsyMYvFWNHF4A'
# response = requests.get(url, headers=headers)
# urls = re.findall('<a href="(https://mp.weixin.qq.com/s\?.*?)"',response.text)

# for mp_url in urls:
# 	#获取原文标题
# 	res = requests.get(mp_url,proxies={'http': None,'https': None},verify=False, headers=headers)
# 	content = res.text.replace('data-src', 'src')
# 	title = re.search(r'var msg_title = \'(.*)\'', content).group(1)
# 	ct = re.search(r'var ct = "(.*)";', content).group(1)
# 	date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
# 	try:
# 		with open(date+'_'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
# 			f.write(content)
# 	except Exception as err:
# 		with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
# 			f.write(content)
# sys.exit(1)
encoding = 'utf-8-sig'
fname = '公众号话题.csv'
with open(fname, 'a+', encoding=encoding) as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章封面'+'\n')
response = requests.get(topic_url, headers=headers)
print(topic_url)
voiceids = re.findall('data-voiceid="(.*)"',response.text)
msgids = re.findall('data-msgid="(.*)"',response.text)
links = re.findall('data-link="(.*)"',response.text)
titles = re.findall('data-title="(.*)" data-voiceid',response.text)
print(titles,len(voiceids))
# for i,j in zip(titles,voiceids):
# 	voice_url = f'https://res.wx.qq.com/voice/getvoice?mediaid={j}'
# 	# print(i,voice_url)
# 	audio_data = requests.get(voice_url,headers=headers)
# 	print('正在下载音频：'+i+'.mp3')
# 	with open(i+'.mp3','wb') as f:
# 		f.write(audio_data.content)
# sys.exit(1)
msgid = re.search('data-msgid="(.*)"',response.text).group(1)
link = re.search('data-link="(.*)"',response.text).group(1)
title = re.search('data-title="(.*)"',response.text).group(1)
titles = re.findall('data-title="(.*)"',response.text)
# print(msgid,link,title)
# print(msgids,links,titles)

for i,j,k in zip(msgids,links,titles):
	print(i,j,k)
	msgid = i
	res = requests.get(j,proxies={'http': None,'https': None},verify=False, headers=headers)
	content = res.text.replace('data-src', 'src')
	# #生成HTML 文件名不能有\/:*?"<>| 
	try:
		with open(trimName(k)+'.html', 'w', encoding='utf-8') as f:
			f.write(content)
	except Exception as err:
		with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
			f.write(content)
	with open(fname, 'a+', encoding=encoding) as f2:
		f2.write(''+','+k + ','+j+ ','+''+'\n')
def download(msgid):
	print('开始')
	url = f'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz={biz}&album_id={album_id}&count=10&begin_msgid={msgid}&begin_itemidx=1&uin=&key=&pass_ticket=&wxtoken=&devicetype=Windows10x64&clientversion=63040026&__biz=MzUyMzUyNzM4Ng%3D%3D&appmsg_token=&x5=0&f=json'
	response = requests.get(url, headers=headers)
	response_dict = response.json()
	# if response_dict.get('getalbum_resp').get('article_list'):
	print(url)
	# print(response_dict['getalbum_resp']['continue_flag'])
	for i in response_dict['getalbum_resp']['article_list']:
		msgid = i['msgid']
		date = time.strftime('%Y-%m-%d', time.localtime(int(i['create_time'])))
		print(i['url'],i['title'])
		res = requests.get(i['url'],proxies={'http': None,'https': None},verify=False, headers=headers)
		content = res.text.replace('data-src', 'src')
		# #生成HTML 文件名不能有\/:*?"<>| 
		try:
			with open(trimName(i['title'])+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
		except Exception as err:
			with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
		with open(fname, 'a+', encoding=encoding) as f2:
			f2.write(date+','+i['title'] + ','+i['url']+ ','+i['cover_img_1_1']+'\n')
	if response_dict['getalbum_resp']['continue_flag'] == '1':
		print(msgid)
		time.sleep(1)
		download(msgid)

download(msgid)