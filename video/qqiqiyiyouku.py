import requests
import re
 
#https://www.52pojie.cn/thread-1636978-1-1.html
class get_list:
    def __init__(self,url):
        self.url = url
        self.type = ''
 
    def judge_type(self):
        if 'v.qq.com' in self.url:
            self.type = 'qq'
        elif 'iqiyi.com' in self.url:
            self.type = 'iqiyi'
        elif 'v.youku.com' in self.url:
            self.type = 'youku'
    def run(self):
        self.judge_type()
        if self.type == 'qq':
            return self.qq()
        elif self.type == 'iqiyi':
            return self.iqiyi()
        elif self.type == 'youku':
            return self.youku()
 
    def qq(self):
        def single(vid):
            single_title = f'https://vv.video.qq.com/getinfo?otype=ojson&vid={vid}'
            response2 = requests.get(single_title).json()  # vl.vi[0].ti
            title = response2['vl']['vi'][0]['ti']
            return title
 
        cid = re.findall('cover/(.+?).html', self.url)[0].split('/')[0]
 
        multi_title = f'http://data.video.qq.com/fcgi-bin/data?tid=431&idlist={cid}&appid=10001005&appkey=0d1a9ddd94de871b'
        response = requests.get(multi_title).text
        vids = re.findall('<video_ids>(.+?)</video_ids>', response)
        result = []
        for vid in vids:
            link = f'https://v.qq.com/x/cover/{cid}/{vid}.html'
            title = single(vid)
            info = {
                'url': link,
                'title': title
            }
            result.append(info)
 
        return result
    def iqiyi(self):
        def single(url):
            res = requests.get(url).text
            try:
                tvid = re.findall('"tvid":(\d+)', res)[0]
            except:
                tvid = re.findall('"tvId":(\d+)', res)[0]
            aid = re.findall('"albumId":(\d+)',res)[0]
            print(aid)
 
            infourl = f'http://mixer.video.iqiyi.com/mixin/videos/{tvid}'
            # https://pcw-api.iqiyi.com/video/video/playervideoinfo?tvid=8634212373749900
            response = requests.get(infourl).json()
            title = response['name']
            return title
 
        res = requests.get(self.url).text
 
        aid = re.findall('"albumId":(\d+)', res)[0]
 
        parse_url = f'https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid={aid}&page=1&size=200'
        response = requests.get(parse_url).json()
        Page = int(response['data']['page'])
        result = []
        for page in range(1,Page+1):
            parse_url = f'https://pcw-api.iqiyi.com/albums/album/avlistinfo?aid={aid}&page={page}&size=200'
            response = requests.get(parse_url).json()
            epsodelists = response['data']['epsodelist']
            for epsodelist in epsodelists:
                tvId = epsodelist['tvId']
                title = epsodelist['name']
                playUrl = epsodelist['playUrl']
                info = {
                    'url': playUrl,
                    'title': title
                }
                result.append(info)
        return result
    def youku(self):
        def single(url):
            vid = re.findall('id_(.+?).html',url)[0]
            parse_url = f'https://ups.youku.com/ups/get.json?vid={vid}&ccode=0532&client_ip=192.168.1.1&client_ts=1652685&utid=zugIG23ivx8CARuB3b823VC%2B'
            response = requests.get(parse_url).json()
            title = response['data']['video']['title']
            return title
 
        return single(self.url)
url = input('输入视频地址：')
result = get_list(url=url).run()
print(result)