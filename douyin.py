import re,time
from urllib.parse import urlparse
import requests

headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Mobile Safari/537.36'
        }
domains = ['www.douyin.com',
           'v.douyin.com',
           'www.snssdk.com',
           'www.amemv.com',
           'www.iesdouyin.com',
           'aweme.snssdk.com']
#https://zuoshouzz.github.io/archives/
#https://github.com/lzjun567/python_scripts/blob/master/douyin.py
## 处理返回Url的内容 https://www.didaho.com/#/watermark https://github.com/moyada/stealer
#https://mp.weixin.qq.com/s/kRUoNTu7avc8t6slQS-e2w
#下载指定的 火山小视频https://github.com/loadchange/hotsoon-crawler
url = input("请输入你要去水印的抖音短视频链接：")
#url =' https://v.douyin.com/oXbjfe/'
response = requests.get(url,headers=headers,allow_redirects=False)
true_url =response.headers['location']
#print(true_url)
parse_url = urlparse(true_url)
if parse_url.netloc not in domains:
    raise Exception("无效的链接")

vid = re.findall(r'\/share\/video\/(\d*)', parse_url.path)[0]
#print(vid)
response = requests.get('https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids='+str(vid))
result = response.json()
#print(result)
item = result.get("item_list")[0]
author = item.get("author").get("nickname")
mp4 = item.get("video").get("play_addr").get("url_list")[0]
cover = item.get("video").get("cover").get("url_list")[0]
mp4 = mp4.replace("playwm", "play")
res = requests.get(mp4, headers=headers, allow_redirects=True)
mp4url = res.url#http://v5-dy-d.ixigua.com/aa21024d9f51deaa2e8ce9ba4f6447f5/5f4cb46c/video/n/tosedge-tos-agsy-ve-0015/ed75a5dbbddf483a8c1382162d31d52f/?a=1128&br=2016&bt=672&cr=0&cs=0&cv=1&dr=0&ds=3&er=&l=202008311526410101980621631104B96C&lr=&mime_type=video_mp4&qs=0&rc=ajM7azNqOXk4dTMzOmkzM0ApOzY6NjZoZWQ6N2UzNjlmNmdpYi0zbnEvMi5fLS1iLS9zczUzLi40NmBhXjEyLzAzYWA6Yw%3D%3D&vl=&vr=
#print(mp4url)
desc = item.get("desc")
mp3 = item.get("music").get("play_url").get("url_list")[0]
#name = input("===>正在下载保存视频,请输入视频名称：")
video = requests.get(url=mp4url, headers=headers)
audio = requests.get(url=mp3, headers=headers)
data = dict()
data['mp3'] = mp3
data['mp4'] = mp4url
data['cover'] = cover
data['nickname'] = author
data['desc'] = desc
data['duration'] = item.get("duration")
print(data)
with open(desc+".mp4", 'wb') as f, open(desc+".mp3", 'wb') as f2:
    #f.write(video.content)#text为网页源码 content响应内容的二进制形式 content.decode('utf-8')
    #f.close()
    #f2.write(audio.content)
    #f2.close()
    print("===>音频和视频下载完成")
#time.sleep(int(format(random.randint(2,8)))) # 设置随机等待时间
#wget.download(url, './image/logo.png')
def downloader(url,path):
    start = time.time() # 开始时间
    size = 0
    headers = {
        'User-Agent': 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    response = requests.get(url,headers=headers,stream=True) # stream属性必须带上 https://github.com/AngelKitty/bilibili-smallvideo/blob/master/bilibili_smallvideo.py
    chunk_size = 1024 # 每次下载的数据大小
    content_size = int(response.headers['content-length']) # 总大小
    if response.status_code == 200:
        print('[文件大小]:%0.2f MB' %(content_size / chunk_size / 1024)) # 换算单位
        with open(path,'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data) # 已下载的文件大小