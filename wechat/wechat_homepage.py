import requests,re,os,time,sys,html,urllib3
from random import randint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }

def get_history():
    history = []
    with open('wechat_homepage_list.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('wechat_homepage_list.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def audio(res,headers,date,title):
    aids = re.findall(r'"voice_id":"(.*?)"',res.text)
    time.sleep(2)
    tmp = 0
    for id in aids:
        tmp +=1
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
        audio_data = requests.get(url,headers=headers)
        print('正在下载音频：'+title+'.mp3')
        with open(date+'___'+trimName(title)+'___'+str(tmp)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
def video(res, headers,date):
    vid = re.search(r'wxv_.{19}',res.text)
    # time.sleep(2)
    if vid:
        vid = vid.group(0)
        url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
        data = requests.get(url,headers=headers,timeout=1).json()
        video_url = data['url_info'][0]['url']
        video_data = requests.get(video_url,headers=headers)
        print('正在下载视频：'+trimName(data['title'])+'.mp4')
        with open(date+'___'+trimName(data['title'])+'.mp4','wb') as f:
            f.write(video_data.content)
urls = get_history()
encoding = 'utf-8-sig'
fname = f'公众号页面模板文章列表.csv'
if not os.path.exists(fname):
	with open(fname, 'a+', encoding=encoding) as f:
		f.write('文章日期'+','+'文章标题' + ','+'文章作者' + ','+'文章简介'+ ','+'文章链接'+ ','+'文章封面'+'\n')
url = ''
if len(sys.argv) > 1:
   url = sys.argv[1]
if not url:
   url = input('苏生不惑提示你，输入公众号页面模板地址：')
if not url:
	print('地址为空')
	sys.exit(1)
def down(begin,count):
	url2=url.replace('#wechat_redirect','')
	url_home = f'{url2}&begin={begin}&count={count}&action=appmsg_list&f=json&r=0.26146868035616433&appmsg_token='
	res = requests.post(url_home,headers=headers,verify=False).json()
	for i in res['appmsg_list']:
		
		if html.unescape(i['link']) in urls:
			print('已经下载过文章:'+html.unescape(i['link']))
			continue
		data = requests.get(i['link'],headers=headers,verify=False)
		content = data.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
		try:
			date = time.strftime('%Y-%m-%d', time.localtime(int(i['sendtime'])))
			title = i['title']
			print('正在下载文章：',title,i['link'])
			audio(data,headers,date,title)
			video(data,headers,date)
			with open(date+'_'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
				save_history(html.unescape(i['link']))
		except Exception as e:
			with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
			print('错误信息：',e)
		with open(fname, 'a+', encoding=encoding) as f2:
			f2.write(date+','+title + ','+i['author'] + ','+i['digest'] + ','+html.unescape(i['link'])+ ','+i['cover']+'\n')
	if res['appmsg_list']:
		down(begin+5,count)
down(0,5)
