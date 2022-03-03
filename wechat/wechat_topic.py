import requests,re,os,time,sys,html
from random import randint
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
biz = 'MjM5NDA5NDcyMA=='
album_id = '1379064498056822787'
topic_url = f'https://mp.weixin.qq.com/mp/appmsgalbum?__biz={biz}&action=getalbum&album_id={album_id}&scene=173&from_msgid=2247507484&from_itemidx=1&count=3&nolastread=1'
# 音频话题 https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzkzNTI5NTc5NQ==&action=getalbum&album_id=2145881553845944326&scene=173&from_msgid=2247507484&from_itemidx=1&count=3&nolastread=1
# 文章话题 https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzUyMzUyNzM4Ng==&action=getalbum&album_id=2091728990028824579&scene=173&from_msgid=2247507484&from_itemidx=1&count=3&nolastread=1#wechat_redirect
# 整理文章 https://mp.weixin.qq.com/s/8_Us3Qe7HRsyMYvFWNHF4A
url = 'https://mp.weixin.qq.com/s/yu0MK1t6pYS8nvc5C1DYuA'
response = requests.get(url, headers=headers)
urls = re.findall('<a target="_blank" href="(https?://mp.weixin.qq.com/s\?.*?)"',response.text)
print(urls)
for mp_url in urls:
	#获取原文标题
	res = requests.get(mp_url,proxies={'http': None,'https': None},verify=False, headers=headers)
	content = res.text.replace('data-src', 'src')
	title = re.search(r'var msg_title = \'(.*)\'', content).group(1)
	ct = re.search(r'var ct = "(.*)";', content).group(1)
	date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
	try:
		with open(date+'_'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
			f.write(content)
	except Exception as err:
		with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
			f.write(content)
sys.exit(1)
encoding = 'utf-8-sig'
fname = '公众号话题文章.csv'
with open(fname, 'a+', encoding=encoding) as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章封面'+'阅读数' + ','+'在看数'+ ','+'点赞数'+'\n')
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
def view(url):
    # with open('公众号文章.txt', 'a', encoding='utf-8') as f3:
        # f3.write(content +'\n')
    # biz=re.search('var biz = "" \|\| "(.*?)"\;',content,re.M).group(1)
    biz=re.search('biz=(.*?)&',url).group(1)
    sn=re.search('sn=(.*?)&',url).group(1)
    mid=re.search('mid=(.*?)&',url).group(1)
    idx=re.search('idx=(.*?)&',url).group(1)
    time.sleep(2)
    data = {
    "is_only_read": "1",
    "is_temp_url": "0",                
    "appmsg_type": "9", # https://www.its203.com/article/wnma3mz/78570580 https://github.com/wnma3mz/wechat_articles_spider
    }
    #appmsg_token和cookie变化
    appmsg_token='1153_PO2U%2BX03ENWHDrtVhj_hQ2tZsAo8zqwuch5AFDM9ndmm9ssfBvY9IQd24IBHmWjgMi2TDoWSEmLNqrXB'
    headers = {
    "Cookie": 'pgv_pvid=3462479730;sd_userid=26861634200545809;sd_cookie_crttime=1634200545809;tvfe_boss_uuid=2462cb91e2efc262;ua_id=BbSW7iXpRV9kLjy3AAAAAJnbZGccv_XAw3N3660mGLU=;pac_uid=0_d6687c556b618;rewardsn=;wxtokenkey=777;wxuin=1541436403;lang=zh_CN;devicetype=Windows10x64;version=6305002e;pass_ticket=VTep/678fnGQ2mu6L00eSO8PnJ+ymPIWdEflAZ0MN3HAafchbjdTKT5UdFSYeRXb;appmsg_token=1153_PO2U%2BX03ENWHDrtVhj_hQ2tZsAo8zqwuch5AFDM9ndmm9ssfBvY9IQd24IBHmWjgMi2TDoWSEmLNqrXB;wap_sid2=CPPngd8FEooBeV9IQzN3ZTAxc3VRMEhXQzNJZHVNbWNNYVlVZzltWDg1N3NudUhxYU9RSUs5ei14a3RoczhsakVnUkFDVXE1aVVqczJmUks0VTkyTmYzLUs0LW5Sc3V3b0lqOTEzSUJkZjVNOUdxb0tISHRxRU1RdFA0Y2lyQnd0UTJfdlJqOFByNXRGOFNBQUF+MO+T15AGOA1AAQ==;',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)"
    }
    origin_url = "https://mp.weixin.qq.com/mp/getappmsgext?"
    appmsgext_url = origin_url + "__biz={}&mid={}&sn={}&idx={}&appmsg_token={}&x5=1".format(biz, mid, sn, idx, appmsg_token)
    # print(requests.post(appmsgext_url, headers=headers, data=data).status_code);sys.exit()
    res = requests.post(appmsgext_url, headers=headers, data=data).json()
    print('阅读数',res["appmsgstat"]["read_num"])
    return str(res["appmsgstat"]["read_num"]), str(res["appmsgstat"]["like_num"]), str(res["appmsgstat"]["old_like_num"])
for i,j,k in zip(msgids,links,titles):
	print(i,j,k)
	msgid = i
	res = requests.get(j,proxies={'http': None,'https': None},verify=False, headers=headers)
	content = res.text.replace('data-src', 'src')
	read_num,like_num,old_like_num = view(html.unescape(j))
	# #生成HTML 文件名不能有\/:*?"<>| 
	# try:
	# 	with open(trimName(k)+'.html', 'w', encoding='utf-8') as f:
	# 		f.write(content)
	# except Exception as err:
	# 	with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
	# 		f.write(content)
	with open(fname, 'a+', encoding=encoding) as f2:
		f2.write(''+','+k + ','+j+ ','+''+ ','+read_num+ ','+like_num+ ','+old_like_num+'\n')
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
		read_num,like_num,old_like_num = view(html.unescape(i['url']))
		# #生成HTML 文件名不能有\/:*?"<>| 
		# try:
		# 	with open(trimName(i['title'])+'.html', 'w', encoding='utf-8') as f:
		# 		f.write(content)
		# except Exception as err:
		# 	with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
		# 		f.write(content)
		with open(fname, 'a+', encoding=encoding) as f2:
			f2.write(date+','+i['title'] + ','+i['url']+ ','+i['cover_img_1_1']+ ','+read_num+ ','+like_num+ ','+old_like_num+'\n')
	if response_dict['getalbum_resp']['continue_flag'] == '1':
		print(msgid)
		time.sleep(1)
		download(msgid)

download(msgid)