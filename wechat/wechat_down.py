import requests,re,os,time,sys,html,sys
from random import randint
import traceback,urllib3,demjson
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://mp.weixin.qq.com',
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
def get_history():
    history = []
    with open('wechat_history.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('wechat_history.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def images(res,headers,date,title):
    imgs=re.findall('data-src="(.*?)"',res.text)
    imgs2= re.findall("cdn_url: '(.*?)',",res.text)
    imgs.extend(imgs2)
    time.sleep(1)
    num = 0
    if not os.path.exists('image'):
        os.mkdir('image')
    for i in imgs:
        if not re.match(r'^https?://.*',i):
            continue
        num+=1
        img_data = requests.get(i,headers=headers)
        print('正在下载图片：'+i)
        with open('image/'+date+'_'+trimName(title)+'_'+str(num)+'.jpg','wb') as f:
            f.write(img_data.content)
def cover(res,headers,date,title):
    cover_url = re.search(r'<meta property="og:image" content="(.*)"\s?/>', res.text)
    if not cover_url:
        return False
    cover_url = cover_url.group(1)
    if not cover_url:
        return False
    cover_data = requests.get(cover_url,headers=headers)
    with open('cover/'+date+'_'+trimName(title)+'.jpg','wb') as f:
        f.write(cover_data.content)
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
        print('正在下载音频：'+title+'.mp3')
        with open('audio/'+date+'_'+trimName(title)+'_'+str(tmp)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
def video(res, headers,date,title,article_url,duration):
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
        # duration_ms = re.search(r"duration_ms: '(.*?)'\s+\*",v)
        # if duration_ms:
        #     duration_ms = duration_ms.group(1)
        #     if int(duration_ms) > duration*60000:
        #         continue
        v_url = re.search(r"url:\s+'(.*?)',",v)
        if not v_url:
            v_url = re.search(r"url:\s+\('(.*?)'\)",v)
        if v_url:
            video_url = html.unescape(v_url.group(1).replace(r'\x26','&'))
            # vids = list(set(vids)) #去重
            num+=1
            print('正在下载视频：'+trimName(title)+'.mp4')
            video_data = requests.get(video_url,headers=headers)
            with open('视频链接合集.csv','a+') as f4:
                f4.write(date+','+trimName(title)+','+video_url+','+article_url+'\n')
            with open('video/'+date+'_'+trimName(title)+'_'+str(num)+'.mp4','wb') as f:
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
print('本工具更新于2024年2月18日，获取最新版本请关注公众号苏生不惑')
url = ''
if len(sys.argv) > 1:
   url = sys.argv[1]
if not url:
   url = input('公众号苏生不惑 提示你，请输入公众号文章链接或者文件名：')# https://mp.weixin.qq.com/s/uzRSOhiH3XbS3Vwr7jGLWg  https://mp.weixin.qq.com/s/goqAKIypCsI4vVLjdhmXSg
# duration = input('公众号苏生不惑 提示你，请输入需要下载视频的时长，单位分钟：')
duration='0'
if not duration:
    duration = '0'
if os.path.exists(url):
    contents = ''
    with open(url, encoding='utf-8') as f:
        contents = f.read()
    urls=contents.split('\n')
else:
    response = requests.get(url, headers=headers)
    urls = re.findall('<a.*?href="(https?://mp.weixin.qq.com/s\?.*?)"',response.text)
    urls.insert(0,url)
urls = [x for x in urls if x != '']
print('文章数量：',len(urls))
num=0
if not os.path.exists('html'):
    os.mkdir('html')
if not os.path.exists('cover'):
    os.mkdir('cover')
for mp_url in urls:
    urls_history = get_history()
    if html.unescape(mp_url) in urls_history:
        print('已经下载过文章:'+html.unescape(mp_url))
        continue
    res = requests.get(html.unescape(mp_url),proxies={'http': None,'https': None},verify=False, headers=headers)
    content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
    num+=1
    time.sleep(randint(1, 2))
    # with open('html/'+str(num)+'.html', 'w', encoding='utf-8') as f:
    #     f.write(content)
    try:
        title = re.search(r'var msg_title = \'(.*)\'', content) or re.search(r'window.title = "(.*)"', content)
        ct = re.search(r'var ct = "(.*)";', content) or re.search(r"d\.ct = xml \? getXmlValue\('ori_create_time\.DATA'\) \: '(.*)'",content)
        if not title:
           title = re.search(r'window\.msg_title = \'(.*?)\'', content)
        if not ct:
           ct = re.search(r'window\.ct = \'(.*?)\'', content)
        # print(cover,title,ct)
        title = title.group(1)
        ct = ct.group(1)
        date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
        print(f'开始下载第{num}篇：',date,title,html.unescape(mp_url))
        cover(res,headers,date,title)
        audio(res,headers,date,title)
        video(res,headers,date,title,mp_url,int(duration))
        images(res,headers,date,title)
        save_history(html.unescape(mp_url))
        with open('html/'+date+'_'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
            f.write(content+'<p style="display:none">下载作者：公众号苏生不惑 微信：sushengbuhuo</p>')
    except Exception as err:
        with open('html/'+str(randint(1000,10000))+'.html', 'w', encoding='utf-8') as f2:
            f2.write(content);print(err,mp_url)#;raise Exception("出错了"+mp_url)
        with open(f'下载失败文章列表.txt', 'a+', encoding='utf-8') as f5:
            f5.write(html.unescape(mp_url)+'\n')
