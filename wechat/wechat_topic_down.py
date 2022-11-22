import requests,re,os,time,sys,html,urllib3
from random import randint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
def get_history():
    history = []
    with open('wechat_topic_list.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('wechat_topic_list.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def audio(res,headers,date,title):
    aids = re.findall(r'"voice_id":"(.*?)"',res.text)
    time.sleep(2)
    tmp = 0
    if not os.path.exists('audio'):
        os.mkdir('audio')
    for id in aids:
        tmp +=1
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
        audio_data = requests.get(url,headers=headers)
        print('正在下载音频：'+title+'.mp3')
        with open('audio/'+date+'___'+trimName(title)+'___'+str(tmp)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
def video(res, headers,date):
    vid = re.search(r'wxv_.{19}',res.text)
    if not os.path.exists('video'):
        os.mkdir('video')
    # time.sleep(2)
    if vid:
        vid = vid.group(0)
        url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
        data = requests.get(url,headers=headers,timeout=1).json()
        video_url = data['url_info'][0]['url']
        video_data = requests.get(video_url,headers=headers)
        print('正在下载视频：'+trimName(data['title'])+'.mp4')
        with open('video/'+date+'___'+trimName(data['title'])+'.mp4','wb') as f:
            f.write(video_data.content)
topic_url = ''
if len(sys.argv) > 1:
   topic_url = sys.argv[1]
if not topic_url:
   topic_url = input('公众号苏生不惑提示你，请输入话题地址：')
# topic_url='https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NjAxOTU4MA==&action=getalbum&album_id=1777378132866465795&scene=173#wechat_redirect'

biz=re.search(r'__biz=(.*?)&',topic_url).group(1)
album_id=re.search(r'album_id=(.*?)&',topic_url).group(1)
response = requests.get(topic_url, headers=headers)
mp_name=re.search(r'<div class="album__author-name">(.*?)</div>',response.text)
if mp_name:
   mp_name = mp_name.group(1)
else:
   mp_name = ''
# voiceids = re.findall('data-voiceid="(.*)"',response.text)
# msgids = re.findall('data-msgid="(.*)"',response.text)
# links = re.findall('data-link="(.*)"',response.text)
# titles = re.findall('data-title="(.*)" data-voiceid',response.text)
# print(titles,len(voiceids))
# for i,j in zip(titles,voiceids):
# 	voice_url = f'https://res.wx.qq.com/voice/getvoice?mediaid={j}'
# 	# print(i,voice_url)
# 	audio_data = requests.get(voice_url,headers=headers)
# 	print('正在下载音频：'+i+'.mp3')
# 	with open(i+'.mp3','wb') as f:
# 		f.write(audio_data.content)
# sys.exit(1)
urls = get_history()
encoding = 'utf-8-sig'
fname = f'公众号{mp_name}话题文章列表.csv'
with open(fname, 'a+', encoding=encoding) as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章封面'+'\n')
msgids = re.findall('data-msgid="(.*)"',response.text)
links = re.findall('data-link="(.*)"',response.text)
titles = re.findall('data-title="(.*)"',response.text)
print(msgids,links,titles)

for i,j,k in zip(msgids,links,titles):
	msgid = i
	if html.unescape(j) in urls:
		print('已经下载过文章:'+html.unescape(j))
		continue
	print('开始下载',j,k)
	res = requests.get(j,proxies={'http': None,'https': None},verify=False, headers=headers)
	content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
	
	try:
		title = re.search(r'var msg_title = \'(.*)\'', content).group(1)
		ct = re.search(r'var ct = "(.*)";', content).group(1)
		date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))

		audio(res,headers,date,title)
		video(res,headers,date)
		with open(mp_name+'_'+date+'_'+trimName(k)+'.html', 'w', encoding='utf-8') as f:
			f.write(content)
			save_history(html.unescape(j))
	except Exception as err:
		with open(mp_name+'_'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
			f.write(content);print(err)
	with open(fname, 'a+', encoding=encoding) as f2:
		f2.write(''+','+k + ','+html.unescape(j)+ ','+''+'\n')
def download(msgid,mp_name):
	url = f'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz={biz}&album_id={album_id}&count=10&begin_msgid={msgid}&begin_itemidx=1&uin=&key=&pass_ticket=&wxtoken=&devicetype=Windows10x64&clientversion=63040026&__biz=MzUyMzUyNzM4Ng%3D%3D&appmsg_token=&x5=0&f=json'
	response = requests.get(url, headers=headers);print(111,url)
	response_dict = response.json()
	if not response_dict.get('getalbum_resp').get('article_list'):
		url = f'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz={biz}&album_id={album_id}&count=10&begin_msgid={msgid}&begin_itemidx=2&uin=&key=&pass_ticket=&wxtoken=&devicetype=Windows10x64&clientversion=63040026&__biz=MzUyMzUyNzM4Ng%3D%3D&appmsg_token=&x5=0&f=json'
		response = requests.get(url, headers=headers)
		response_dict = response.json();print(url)
		if not response_dict.get('getalbum_resp').get('article_list'):
			url = f'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz={biz}&album_id={album_id}&count=10&begin_msgid={msgid}&begin_itemidx=6&uin=&key=&pass_ticket=&wxtoken=&devicetype=Windows10x64&clientversion=63040026&__biz=MzUyMzUyNzM4Ng%3D%3D&appmsg_token=&x5=0&f=json'
			response = requests.get(url, headers=headers)
			response_dict = response.json();print(url)
			if not response_dict.get('getalbum_resp').get('article_list'):
				sys.exit(1)
	# print(response_dict['getalbum_resp']['continue_flag'])
	for i in response_dict['getalbum_resp']['article_list']:
		msgid = i['msgid']
		if html.unescape(i['url']) in urls:
			print('已经下载过文章:'+html.unescape(i['url']))
			continue
		date = time.strftime('%Y-%m-%d', time.localtime(int(i['create_time'])))
		print('开始下载',i['url'],i['title'])
		res = requests.get(i['url'],proxies={'http': None,'https': None},verify=False, headers=headers)
		content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
		cover = re.search(r'<meta property="og:image" content="(.*)"\s?/>', content)
		try:
			title = re.search(r'var msg_title = \'(.*)\'', content).group(1)
			ct = re.search(r'var ct = "(.*)";', content).group(1)
			cover = cover.group(1)
			date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
			cover_data = requests.get(cover,headers=headers)
			if not os.path.exists('cover'):
				os.mkdir('cover')
			with open('cover/'+date+'_'+trimName(i['title'])+'_封面.jpg','wb') as f:
				f.write(cover_data.content)
			audio(res,headers,date,title)
			video(res,headers,date)
			if not os.path.exists('html'):
				os.mkdir('html')
			with open('html/'+mp_name+'_'+date+'_'+trimName(i['title'])+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
				save_history(html.unescape(i['url']))
		except Exception as err:
			with open(mp_name+'_'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
				f.write(content);print(err)
		with open(fname, 'a+', encoding=encoding) as f2:
			f2.write(date+','+i['title'] + ','+html.unescape(i['url'])+ ','+i['cover_img_1_1']+'\n')
	if response_dict['getalbum_resp']['continue_flag'] == '1':
		# print(msgid)
		time.sleep(1)
		download(msgid,mp_name)

download(msgid,mp_name)