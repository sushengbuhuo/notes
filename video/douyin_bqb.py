import urllib.request
import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import socket
#设置超时时间为30s
socket.setdefaulttimeout(30)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
#请求头https://www.52pojie.cn/thread-1586239-1-1.html
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 aweme_19.4.0 JsSdk/2.0 NetType/4G Channel/App Store ByteLocale/zh Region/CN AppTheme/light BytedanceWebview/d8a21c6 Aweme/19.4.0 Mobile ToutiaoMicroApp/2.40.0.1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://tmaservice.developer.toutiao.com/?appid=ttca16bcab552fe68201&version=2.0.0',
    'Connection': 'keep-alive',
    'Host': 'zaza.guojiangdong.com.cn',
}
 
#通过标题搜索
# def SearchByTitle():
#     keyword = input("请输入表情包标题：\n")
#     data = {
#         'do': 'sousuo',
#         'keyword': keyword,
#         'page': '1',
#         'i': '2',
#         'c': 'entry',
#         'a': 'toutiaoapp',
#         'v': '1.0.0',
#         'm': 'mm_qu'
#     }
#     search_result = requests.post('https://zaza.guojiangdong.com.cn/app/index.php', headers=headers, data=data)
#     js = json.loads(search_result.text)
 
 
#通过id搜索，我直接遍历所有，你也可以改一下获取指定作者的表情包
def SearchById():
    # upid = input("请输入表情包up主编号：\n")
    for upid in range(0, 999):
        i = 0
        while i != -1:
            data = {
                'do': 'upimage',
                'upid': upid,
                'tid': '0',
                'page': i,
                'i': '2',
                'c': 'entry',
                'a': 'toutiaoapp',
                'v': '1.0.0',
                'm': 'mm_qu'
            }
            search_result = requests.post('https://zaza.guojiangdong.com.cn/app/index.php', headers=headers, data=data)
            js = json.loads(search_result.text)
             
            #实测第一页和其他页返回的json结构不一样
            try:
                listimg = js[0]['listimg']
            except:
                listimg = js
 
            try:
                i += 1
                GetGifById(upid, listimg)
            except:
                #报错就说明到底了
                i = -1
 
#获取gif地址
def GetGifById(upid, js):
    i = 0
    #这句代码是用来判断js是否为空的,不然为空不报错
    code=js[i]['img']
    for name in js:
        img = js[i]['img']
        name = js[i]['name']
        if "https" in img:
            url = img
        else:
            url = "https://zhage1.yayashijue.com/" + img
 
        GifDownload(upid, name, url)
        i += 1
 
#获取桌面文件夹
def get_desk_p():
    return os.path.join(os.path.expanduser('~'), "Desktop")
 
# 在桌面创建表情包文件夹，根据作者编号创建子文件夹，然后下载至该文件夹
def GifDownload(upid, name, url):
    desktop = get_desk_p() + "\\" + "表情包"
    folder_name = str(upid)
    filepath = os.path.join(desktop, folder_name)
    if not os.path.isdir(filepath):
        os.makedirs(filepath)
    img_name = name + ".gif"
    filename = filepath + "\\" + img_name
 
    try:
        urllib.request.urlretrieve(url, filename)
    except socket.timeout:
        count = 1
        while count <= 2:
            try:
                urllib.request.urlretrieve(url, filename)
                break
            except socket.timeout:
                count += 1
        if count > 2:
            print("downloading this gif fialed!")
 
 
if __name__ == "__main__":
    SearchById()