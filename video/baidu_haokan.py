#encoding:utf-8
# 好看视频下载
 
import socket
from urllib.request import urlopen
import urllib
import re
import time
from pyquery import PyQuery as pq
import requests
from tqdm import tqdm # 打印进度条的库
import gzip
 
print('程序开始运行。。。')
requests.adapters.DEFAULT_RETRIES = 5
# connect to a URL
timeout = 30
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
sleep_download_time = 3
time.sleep(sleep_download_time) #这里时间自己设定
 
# 输入好看视频地址
haokanurl = input('请输入要下载的好看视频的网页地址：')
# haokanurl = 'https://haokan.baidu.com/v?vid=7448757459481911514&tab=yinyue_new'#示例地址
 
#为了避免出现403提示，这里伪装浏览器
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
req = urllib.request.Request(url=haokanurl, headers=headers)
website = urlopen(req,timeout = 90)
print('好看视频下载地址解析中')
 
# read html code
html = website.read().decode('UTF-8')
#html = website.read().decode()
#当使用上面的直接decode()出错时可以使用下面的方法
# html = website.read()
# buff = BytesIO(html)
# f = gzip.GzipFile(fileobj=buff)
# html = f.read().decode('utf-8')
website.close()

# use re.findall to get all the links
 
# 取得视频名称（标题）https://www.52pojie.cn/thread-1513652-1-1.html
videotitle = re.findall('<h1 class="videoinfo-title">(.*?)</h1>',html)[0]
print(videotitle)
# 默认地址
links = re.findall('"playurl":"(.*)","clarityUrl"',html)#默认地址
downurl = links[0]
downurl = downurl.replace('\\','')
print('视频实际地址：')
print(downurl)
print('现在开始下载该视频，请稍等。。。')
res = requests.get(downurl, headers={'user-agent': 'chrome'})
total_size = round(int(res.headers["Content-Length"])/1024/1024)
print('解析完成，视频大小为：' + str(total_size) + 'MB。现在开始下载。')
with open(f'{videotitle}down.mp4', 'wb') as f:
     for chunk in tqdm(iterable=res.iter_content(1024*1024), total=total_size, unit='KB'):\
         f.write(chunk)
     print('下载完成。')
 
sdlinks = re.findall('"key":"sd","rank":0,"title":"(.*?)","videoBps":',html)[0]#标清地址
sdlinks = re.findall('"url":"(.*)',sdlinks)
sdurl = sdlinks[0]
sdurl = sdurl.replace('\\','')
print('标清视频地址是：')
print(sdurl)
print('现在开始下载标清视频，请稍等。。。')
res = requests.get(sdurl, headers={'user-agent': 'chrome'})
total_size = round(int(res.headers["Content-Length"])/1024/1024)
print('解析完成，视频大小为：' + str(total_size) + 'MB。现在开始下载。')
with open(f'{videotitle}标清.mp4', 'wb') as f:
     for chunk in tqdm(iterable=res.iter_content(1024*1024), total=total_size, unit='KB'):\
         f.write(chunk)
     print('下载完成。')
 
 
hdlinks = re.findall('"key":"hd","rank":1,"title":"(.*?)","videoBps":',html)[0]#高清地址
hdlinks = re.findall('"url":"(.*)',hdlinks)
hdurl = hdlinks[0]
hdurl = hdurl.replace('\\','')
print('高清视频地址是：')
print(hdurl)
print('现在开始下载高清视频，请稍等。。。')
res = requests.get(hdurl, headers={'user-agent': 'chrome'})
total_size = round(int(res.headers["Content-Length"])/1024/1024)
print('解析完成，视频大小为：' + str(total_size) + 'MB。现在开始下载。')
with open(f'{videotitle}高清.mp4', 'wb') as f:
     for chunk in tqdm(iterable=res.iter_content(1024*1024), total=total_size, unit='KB'):\
         f.write(chunk)
     print('下载完成。')
 
 
sclinks = re.findall('"key":"sc","rank":2,"title":"(.*?)","videoBps":',html)[0]#超清地址
sclinks = re.findall('"url":"(.*)',sclinks)
scurl = sclinks[0]
scurl = scurl.replace('\\','')
print('超清视频地址是：')
print(scurl)
print('现在开始下载超清视频，请稍等。。。')
res = requests.get(scurl, headers={'user-agent': 'chrome'})
total_size = round(int(res.headers["Content-Length"])/1024/1024)
print('解析完成，视频大小为：' + str(total_size) + 'MB。现在开始下载。')
with open(f'{videotitle}超清.mp4', 'wb') as f:
     for chunk in tqdm(iterable=res.iter_content(1024*1024), total=total_size, unit='KB'):\
         f.write(chunk)
     print('下载完成。')
 
 
p1080links = re.findall('"key":"1080p","rank":3,"title":"(.*?)","videoBps":',html)[0]#蓝光地址
p1080links = re.findall('"url":"(.*)',p1080links)
p1080url = p1080links[0]
p1080url = p1080url.replace('\\','')
print('蓝光视频地址是：')
print(p1080url)
print('现在开始下载蓝光视频，请稍等。。。')
res = requests.get(p1080url, headers={'user-agent': 'chrome'})
total_size = round(int(res.headers["Content-Length"])/1024/1024)
print('解析完成，视频大小为：' + str(total_size) + 'MB。现在开始下载。')
with open(f'{videotitle}蓝光.mp4', 'wb') as f:
     for chunk in tqdm(iterable=res.iter_content(1024*1024), total=total_size, unit='KB'):\
         f.write(chunk)
     print('下载完成。')
 
print('所有格式视频下载完成，请检查是否正确。')