from moviepy.editor import VideoFileClip,concatenate_videoclips
import json
import os
import re
import requests
import sys
import re,hashlib
import time
import requests
from m3u8download_hecoter import m3u8download

md5 = lambda value: hashlib.md5(value.encode('utf-8')).hexdigest()

def get_info_url(url):
    # url = 'https://tv.cctv.com/2022/04/20/VIDE7Ng1fymNZG5fNGKhXWsL220420.shtml?spm=C31267.PhFb97MzMZUk.EoLaAz312Pxz.1'
    headers = {
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/100.0.4896.127"
    }
    response = requests.get(url=url, headers=headers).content.decode('utf-8')

    if 'v.cctv.com' in url:
        guid = re.findall('var guid = "(.+?)"', response)[0]
    elif 'webapp.cctv.com' in url:
        guid = re.findall('data-guid="(.+?)"',response)[0]
    else:
        guid = ''

    tai = 'ipad'
    client = 'html5'
    staticCheck = "47899B86370B879139C08EA3B5E88267"
    im = '1'
    tsp = str(int(time.time()))
    vn = '2049'
    vdn_uid = ''
    vc = md5((tsp + vn + staticCheck + vdn_uid))
    vnData = f"pid={guid}&tai={tai}&client={client}&im={im}&tsp={tsp}&vn={vn}&vc={vc}&uid={vdn_uid}&wlan="
    info_url = 'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?' + vnData
    return info_url

def run(url):
    infourl = get_info_url(url)
    headers = {
        'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/100.0.4896.127"
    }
    response = requests.get(url=infourl,headers=headers).json()
    # video.chapters4[0].url  hls_url
    title = response['title']
    m3u8url = response['hls_url']
    m3u8download(m3u8url=m3u8url,title=title,base_uri_parse='https://hls.cntv.myhwcdn.cn',headers=headers)

if __name__ == '__main__':
    print('cctv视频解析: https://tv.cctv.com/2022/04/20/VIDE7Ng1fymNZG5fNGKhXWsL220420.shtml')
    while True:
        # url = 'https://tv.cctv.com/2022/04/20/VIDE7Ng1fymNZG5fNGKhXWsL220420.shtml?spm=C31267.PhFb97MzMZUk.EoLaAz312Pxz.1'
        url = input('输入cctv视频网址：')
        try:
            run(url)
        except:
            pass

# https://www.52pojie.cn/thread-1618341-1-1.html  pip install moviepy
class cctv_ts:
    def init(self,url,rate=3):  #url 播放视频的网页url
        self.rate=int(rate)
        self.url=url                #cctv播放视频网页链接
        self.video_url_format='https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=guid'   # 视频文件信息模板的链接，guid是视频对应的编号
        self.videoUrlList=[]                                                                  # 视频的真实链接
        self.videoFileName=''                                                             # 视频的文件名称
        self.rateNameList=['流畅','标清','高清','超清','超高清']                            # 视频分辨率列表
        self.videoSectionNameList=[]                                    # 保存分段视频中各段视频的名称   
 
#获取视频的链接https://github.com/hecoter/videoParse
cctv=cctv_ts(url,rate)
cctv.run()