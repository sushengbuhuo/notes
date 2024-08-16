import requests,re,os,time,sys,html,urllib3
from random import randint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://mp.weixin.qq.com',
    }
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ')
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
    if not aids:
        aids = re.findall(r'voiceid\s*:\s*"(.*?)"',res.text)
    time.sleep(2)
    tmp = 0
    if not os.path.exists('audio'):
        os.mkdir('audio')
    for id in aids:
        tmp +=1
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
        audio_data = requests.get(url,headers=headers)
        if not audio_data.content:
            continue
        print('正在下载音频：'+title+'.mp3')
        with open('audio/'+date+'_'+replace_invalid_chars(title)+'_'+str(tmp)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
def video(res, headers,date,title,article_url):
    # vids = re.findall(r'wxv_\d{19}',res.text)
    if not os.path.exists('video'):
        os.mkdir('video')
    vinfo = re.findall(r'window\.__mpVideoTransInfo\s+\=\s+([\s\S]*?)\];',res.text,flags=re.S)
    if not vinfo:
        vinfo = re.findall(r'mp_video_trans_info:\s+([\s\S]*?)\],',res.text,flags=re.S)
    videos = re.findall(r"source_link\: xml \? getXmlValue\(\'video_page_info\.source_link\.DATA\'\) : \'http://v\.qq\.com/x/page/(.*?)\.html\'\,",res.text)
    if not videos:
        videos = re.findall(r"source_link\: \'http://v\.qq\.com/x/page/(.*?)\.html\' \|\| \'\'\,",res.text)
    num = 0
    for v in vinfo:
        v_url = re.search(r"url:\s+'(.*?)',",v)
        if not v_url:
            v_url = re.search(r"url:\s+\('(.*?)'\)",v)
        # print(v,v_url)
        if v_url:
            video_url = html.unescape(v_url.group(1).replace(r'\x26','&'))
            # vids = list(set(vids)) #去重
            num+=1
            print('正在下载视频：'+trimName(title)+'.mp4')
            video_data = requests.get(video_url,headers=headers)
            with open('视频链接合集.csv','a+') as f4:
                f4.write(date+','+trimName(title)+','+video_url+','+article_url+'\n')
            with open('video/'+date+'_'+replace_invalid_chars(title)+'_'+str(num)+'.mp4','wb') as f:
                f.write(video_data.content)
        
    time.sleep(1)
    for i in videos:
        print(f'腾讯视频地址：http://v.qq.com/x/page/{i}.html')
        with open('视频链接合集.csv','a+') as f4:
            f4.write(date+','+trimName(title)+','+f'http://v.qq.com/x/page/{i}.html'+','+article_url+'\n')
    # for vid in vids:
    #     # vid = vid.group(0)
    #     print('视频id',vid)
    #     url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
    #     data = requests.get(url,headers=headers,timeout=1).json()
    #     video_url = data['url_info'][0]['url']
    #     video_data = requests.get(video_url,headers=headers)
    #     with open('视频链接合集.csv','a+') as f4:
    #         f4.write(date+','+trimName(data['title'])+','+video_url+','+article_url+'\n')
    #     print('正在下载视频：'+trimName(data['title'])+'.mp4')
    #     with open('video/'+date+'_'+trimName(data['title'])+'.mp4','wb') as f:
    #         f.write(video_data.content)
topic_url = ''
# print('本工具更新于2024年8月16日，获取最新版本请关注公众号苏生不惑')
if len(sys.argv) > 1:
   topic_url = sys.argv[1]
if not topic_url:
   topic_url = input('公众号苏生不惑提示你，请输入公众号话题链接：')
# 纯音频 topic_url='https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NjAxOTU4MA==&action=getalbum&album_id=1777378132866465795&scene=173#wechat_redirect'
# 纯文章 topic_url = 'https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NjAxOTU4MA==&action=getalbum&album_id=1681628721901830149&scene=173&from_msgid=3009294038&from_itemidx=1&count=3&nolastread=1'
# 纯视频 topic_url = 'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&album_id=1333036982024585217&__biz=MzU1OTgyMzQzNw==#wechat_redirect'
# 苏生不惑话题 topic_url='https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyMjg2ODExMA==&action=getalbum&album_id=2267160702144708611&scene=173&from_msgid=2247502369&from_itemidx=2&count=3&nolastread=1#wechat_redirect'
biz=re.search(r'__biz=(.*?)[&#]',topic_url).group(1)
album_id=re.search(r'album_id=(.*?)[&#]',topic_url).group(1)
response = requests.get(html.unescape(topic_url), headers=headers)
mp_name=re.search(r'<div class="album__author-name">(.*?)</div>',response.text)
if mp_name:
   mp_name = mp_name.group(1)
else:
   mp_name = ''
voiceids = re.findall('data-voiceid="(.*)"',response.text)
if voiceids:
	msgids = re.findall('data-msgid="(.*)"',response.text)
	links = re.findall('data-link="(.*)"',response.text)
	titles = re.findall('data-title="(.*)"',response.text)
	voice_urls = get_history()
	print('音频数量:',len(voiceids))
	if not os.path.exists('audio'):
		os.mkdir('audio')
	# print('音频标题列表:',titles)
	for i,j in zip(titles,voiceids):
		voice_url = f'https://res.wx.qq.com/voice/getvoice?mediaid={j}'
		if voice_url in voice_urls:
			print('已经下载过音频：'+i+'.mp3')
			continue
		# print(i,voice_url)
		audio_data = requests.get(voice_url,headers=headers)
		print('正在下载音频：'+i+'.mp3')
		with open('audio/'+replace_invalid_chars(i)+'.mp3','wb') as f:
			f.write(audio_data.content)
			save_history(voice_url)
	print('下载完成')
	sys.exit(1)

urls = get_history()
encoding = 'utf-8-sig'
fname = f'公众号{mp_name}话题文章.csv'
with open(fname, 'a+', encoding=encoding) as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章封面'+'\n')
msgids = re.findall('data-msgid="(.*)"',response.text)
links = re.findall('data-link="(.*)"',response.text)
titles = re.findall('data-title="(.*)"',response.text)
itemidxs = re.findall('data-itemidx="(.*)"',response.text)
# print(msgids,links,titles)
# if not os.path.exists('cover'):
# 	os.mkdir('cover')
if not os.path.exists('html'):
	os.mkdir('html')
for i,j,k,g in zip(msgids,links,titles,itemidxs):
	msgid = i
	itemidx = g
	if html.unescape(j) in urls:
		print('已经下载过文章:'+html.unescape(j))
		continue
	print('开始下载',html.unescape(j),k)
	res = requests.get(html.unescape(j),proxies={'http': None,'https': None},verify=False, headers=headers)
	content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
	try:
		title = re.search(r'var msg_title = \'(.*)\'', content) or re.search(r'window.title = "(.*)"', content)
		ct = re.search(r'var ct = "(.*)";', content) or re.search(r"d\.ct = xml \? getXmlValue\('ori_create_time\.DATA'\) \: '(.*)'",content)
		cover = re.search(r'<meta property="og:image" content="(.*)"\s?/>', content)
		if not title:
			title = re.search(r'window\.msg_title = \'(.*?)\'', content)
		if not ct:
			ct = re.search(r'window\.ct = \'(.*?)\'', content)
		cover = cover.group(1)
		title = title.group(1)
		ct = ct.group(1)
		date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
		date2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(ct)))
		# cover_data = requests.get(cover,headers=headers)
		# with open('cover/'+date+'_'+replace_invalid_chars(k)+'.jpg','wb') as f:
			# f.write(cover_data.content)
		# audio(res,headers,date,title)
		# video(res,headers,date,title,j)
		with open('html/'+mp_name+'_'+date+'_'+replace_invalid_chars(k)+'.html', 'w', encoding='utf-8') as f:
			f.write(content)
		with open(fname, 'a+', encoding=encoding) as f2:
			f2.write(date2+','+k + ','+html.unescape(j)+ ','+cover+'\n')
		save_history(html.unescape(j))
	except Exception as err:
		with open(f'{mp_name}下载失败文章.txt', 'a+', encoding=encoding) as f5:
			f5.write(html.unescape(j)+'\n');print(err,html.unescape(j))
		# with open('html/'+mp_name+'_'+str(randint(10,100000))+'.html', 'w', encoding='utf-8') as f:
		# 	f.write(content);print(err,j);raise Exception("抓取失败了："+j)
def download(msgid,mp_name,itemidx):
	url = f'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz={biz}&album_id={album_id}&count=10&begin_msgid={msgid}&begin_itemidx={itemidx}&uin=&key=&pass_ticket=&wxtoken=&devicetype=Windows10x64&clientversion=63040026&__biz=MzUyMzUyNzM4Ng%3D%3D&appmsg_token=&x5=0&f=json'
	response = requests.get(url, headers=headers)
	response_dict = response.json()
	if not response_dict.get('getalbum_resp').get('article_list'):
		return False
		sys.exit(1)
	#最后一条是对象，前面是数组
	articles = response_dict['getalbum_resp']['article_list']
	if isinstance(articles,dict):
		articles = [articles]
	for i in articles:
		# print(response_dict)
		msgid = i['msgid']
		itemidx = i['itemidx']
		if html.unescape(i['url']) in urls:
			print('已经下载过文章:'+html.unescape(i['url']))
			continue
		date = time.strftime('%Y-%m-%d', time.localtime(int(i['create_time'])))
		date2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i['create_time'])))
		print('开始下载',html.unescape(i['url']),i['title'])
		res = requests.get(html.unescape(i['url']),proxies={'http': None,'https': None},verify=False, headers=headers)
		content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
		try:
			title = re.search(r'var msg_title = \'(.*)\'', content) or re.search(r'window.title = "(.*)"', content)
			ct = re.search(r'var ct = "(.*)";', content) or re.search(r"d\.ct = xml \? getXmlValue\('ori_create_time\.DATA'\) \: '(.*)'",content)
			cover = re.search(r'<meta property="og:image" content="(.*)"\s?/>', content)
			if not title:
				title = re.search(r'window\.msg_title = \'(.*?)\'', content)
			if not ct:
				ct = re.search(r'window\.ct = \'(.*?)\'', content)
			cover = cover.group(1)
			title = title.group(1)
			ct = ct.group(1)
			date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
			# cover_data = requests.get(cover,headers=headers)
			# with open('cover/'+date+'_'+replace_invalid_chars(i['title'])+'.jpg','wb') as f:
				# f.write(cover_data.content)
			# audio(res,headers,date,title)
			# video(res,headers,date,title,i['url'])
			with open('html/'+mp_name+'_'+date+'_'+replace_invalid_chars(i['title'])+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
			save_history(html.unescape(i['url']))
		except Exception as err:
			# with open(f'{mp_name}下载失败文章.txt', 'a+', encoding=encoding) as f6:
			# 	f6.write(html.unescape(i['url'])+'\n');
			print(err,html.unescape(i['url']))
			# with open('html/'+mp_name+'_'+date+'_'+str(randint(100,100000))+'.html', 'w', encoding='utf-8') as f:
			# 	f.write(content);print(err,i['url']);raise Exception("抓取失败了："+i['url'])
		with open(fname, 'a+', encoding=encoding) as f2:
			f2.write(date2+','+i['title'] + ','+html.unescape(i['url'])+ ','+i['cover_img_1_1']+'\n')
	if response_dict['getalbum_resp']['continue_flag'] == '1':
		# print(msgid)
		time.sleep(randint(2, 5))
		download(msgid,mp_name,itemidx)
download(msgid,mp_name,itemidx)