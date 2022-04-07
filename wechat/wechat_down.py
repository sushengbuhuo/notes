import requests,re,os,time,sys,html
from random import randint
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')

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
def video(res, headers,date):
    vid = re.search(r'wxv_.{19}',res.text)
    # time.sleep(2)
    if vid:
        vid = vid.group(0)
        print('视频id',vid)
        url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
        data = requests.get(url,headers=headers,timeout=1).json()
        video_url = data['url_info'][0]['url']
        video_data = requests.get(video_url,headers=headers)
        print('正在下载视频：'+trimName(data['title'])+'.mp4')
        with open(date+'___'+trimName(data['title'])+'.mp4','wb') as f:
            f.write(video_data.content)
url = input('公众号苏生不惑提示你，请输入文章链接：')# https://mp.weixin.qq.com/s/uzRSOhiH3XbS3Vwr7jGLWg  https://mp.weixin.qq.com/s/2OvCryS7ROyRQqVFkyFtdg
response = requests.get(url, headers=headers)
urls = re.findall('<a target="_blank" href="(https?://mp.weixin.qq.com/s\?.*?)"',response.text)
urls.append(url)
print('文章总数',len(urls))
for mp_url in urls:
    res = requests.get(html.unescape(mp_url),proxies={'http': None,'https': None},verify=False, headers=headers)
    content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
    
    try:
        title = re.search(r'var msg_title = \'(.*)\'', content).group(1)
        ct = re.search(r'var ct = "(.*)";', content).group(1)
        date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
        print(date,title)
        audio(res,headers,date,title)
        video(res,headers,date)
        with open(date+'_'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as err:
        with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
            f.write(content);print(err)
