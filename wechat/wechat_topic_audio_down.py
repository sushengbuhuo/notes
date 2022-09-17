import requests,re,os,time,sys,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
def get_history():
    history = []
    with open('wechat_topic_audio_list.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('wechat_topic_audio_list.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
topic_url = input('公众号苏生不惑提示你，请输入音频话题地址：')
# topic_url='https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NjAxOTU4MA==&action=getalbum&album_id=1777378132866465795&scene=173#wechat_redirect'
if not topic_url:
	print('地址不能为空')
	sys.exit(1) 
biz=re.search(r'__biz=(.*?)&',topic_url).group(1)
album_id=re.search(r'album_id=(.*?)&',topic_url).group(1)
response = requests.get(topic_url, headers=headers)
voiceids = re.findall('data-voiceid="(.*)"',response.text)
msgids = re.findall('data-msgid="(.*)"',response.text)
links = re.findall('data-link="(.*)"',response.text)
titles = re.findall('data-title="(.*)" data-voiceid',response.text)
voice_urls = get_history()
print('音频数量:',len(voiceids))
# print('音频标题列表:',titles)
for i,j in zip(titles,voiceids):
	voice_url = f'https://res.wx.qq.com/voice/getvoice?mediaid={j}'
	if voice_url in voice_urls:
		print('已经下载过音频：'+i+'.mp3')
		continue
	# print(i,voice_url)
	audio_data = requests.get(voice_url,headers=headers)
	print('正在下载音频：'+i+'.mp3')
	with open(trimName(i)+'.mp3','wb') as f:
		f.write(audio_data.content)
		save_history(voice_url)