import requests
import re
import time
from node_vm2 import NodeVM
from m3u8download_hecoter import m3u8download
#https://www.52pojie.cn/thread-1630248-1-1.html
class IQIYI:
    def __init__(self,url,title='',Cookie=''):
        self.title = title
        self.Cookie = 'P00001=dbDGm3tbOctQELNen4XiwyzaLzc3Sm1AaLjdhrwm24bgKivBbMNXyv0YLxOSkdKlwEPUl2d'
        self.Cookie_P00003 = ''
        self.Cookie_QC005 = ''
        self.Cookie_dfp = ''
        self.url = url

    def get_vf(self,url):

        with open('iqiyi_down.js', 'r', encoding='utf-8') as f:
            js = f.read()
        module = NodeVM.code(js)
        vf = module.call_member('cmd5x', url)
        return f'{url}&vf={vf}'

    def getm3u8(self,shareurl):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75',
            'cookie': self.Cookie
        }
        response = requests.get(url=shareurl, headers=headers).text
        m3u8 = re.findall('"m3u8":"(.+?)"', response)[0].replace('/', '').replace('\\', '/')
        m3u8s = m3u8.split('/n')
        m3u8 = '\n'.join(m3u8s)

        vsizes = re.findall('"vsize":(\d+)', response)
        vs = []
        for vsize in vsizes:
            vs.append(int(int(vsize) / 1024 / 1024))
        vssize = str(max(vs)) + 'MB'
        scrsz = re.findall('"scrsz":"(.+?)"', response)[0]

        title = self.title + '_' + scrsz + '_' + vssize

        with open(f'{title}.m3u8', 'w', encoding='utf-8') as f:
            f.write(m3u8)
        ## 下载部分
        m3u8download(m3u8url=f'{title}.m3u8',title=title)

    def parse(self):
        response = requests.get(self.url).text
        try:
            self.title = re.findall('<meta  name="irTitle" content="(.+?)" />', response)[0]
        except:
            self.title = ''

        tvid = re.findall('"tvId":(\d+)', response)[0]

        vid = re.findall('"vid":"(.+?)"', response)[0]

        tm = int(time.time() * 1000)
        # k_ft2 = 8191
        url_with_dash_but_vf2 = f'/jp/dash?tvid={tvid}&bid=860&vid={vid}&src=03020031010000000000&vt=0&rs=1&uid={self.Cookie_P00003}&ori=pcw&ps=0&k_uid={self.Cookie_QC005}&pt=0&d=0&s=&lid=&cf=&ct=&k_tag=1&ost=0&ppt=0&dfp={self.Cookie_dfp}&locale=zh_cn&k_err_retries=0&qd_v=2&tm={tm}&qdy=a&qds=0&k_ft2=8191&callback=hecoter&ut=1'
        vf = self.get_vf(url_with_dash_but_vf2)

        infourl = 'https://cache.video.iqiyi.com' + vf

        self.getm3u8(infourl)
url=input("请输入视频地址：")
iqiyi = IQIYI(url=url,Cookie='').parse()