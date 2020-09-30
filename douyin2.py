import re
from urllib.parse import urlparse
import requests
import json
import wget

"""
作者：刘志军https://github.com/lzjun567/python_scripts/blob/master/douyin.py
公众号：Python之禅
任何问题可以加我微信：go2071  进行交流，备注“github”
"""
#https://mp.weixin.qq.com/s/kRUoNTu7avc8t6slQS-e2w

 
#share = input("请输入你要去水印的抖音短视频链接：")
# share='https://v.douyin.com/oXbjfe/'
# pat = '(https://v.douyin.com/.*?/)' #https://v.douyin.com/oXbjfe/
# url = re.compile(pat).findall(share)[0]  #正则匹配分享链接
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3904.108 Safari/537.36'
# }
# r = requests.get(url, headers=headers,allow_redirects=False)

# pat = 'playAddr: "(.*?)",'
# print(re.compile(pat).findall(r.text))
# play = re.compile(pat).findall(r.text)[0].replace("playwm", "play")
# headers = {
#     'user-agent': 'Android',
# }
# r = requests.get(play, headers=headers, allow_redirects=False)
# playurl = r.headers['location']
 

# name = input("===>正在下载保存视频,请输入视频名称：")
# video = requests.get(url=playurl, headers=headers)
# with open(name+".mp4", 'wb')as file:
#     file.write(video.content)
#     file.close()
#     print("===>视频下载完成！")

#获取真正的原始url https://zuoshouzz.github.io/2020/03/11/%E6%8A%96%E9%9F%B3%E5%8E%BB%E6%B0%B4%E5%8D%B0%E8%A7%86%E9%A2%91%E8%AF%A6%E7%BB%86%E6%AD%A5%E9%AA%A4%E5%8F%8A%E6%8E%A5%E5%8F%A3%E7%BC%96%E5%86%99/
#https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6847790700554177805
#https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200fc30000bs43pp80c78p0q1l80gg&ratio=720p&line=0
#https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200fc30000bs43pp80c78p0q1l80gg&ratio=720p&line=0
#http://v9-dy-x.ixigua.com/e1e0d74c47aa1cea4f088f31bfe9cd12/5f4c8373/video/tos/cn/tos-cn-ve-15/c2dd660d7be34f79827378888d9b5caf/?a=1128&br=5757&bt=1919&cr=0&cs=0&cv=1&dr=0&ds=3&er=&l=2020083111570401019806215314031D2D&lr=&mime_type=video_mp4&qs=0&rc=ajNvdHM6M3M2djMzNmkzM0ApN2k7aGg1aWQ7NzY6PDY3PGdkNS4tNWA1bTFfLS1gLS9zc2M2Ni8yYzNhNi5eLjViMDY6Yw%3D%3D&vl=&vr=
# 处理返回Url的内容 https://www.didaho.com/#/watermark https://github.com/moyada/stealer
# input("===>press enter key to exit!")

class DY(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Mobile Safari/537.36'
        }

        self.domain = ['www.douyin.com',
                       'v.douyin.com',
                       'www.snssdk.com',
                       'www.amemv.com',
                       'www.iesdouyin.com',
                       'aweme.snssdk.com']

    def init_app(self, app):
        self.app = app

    def parse(self, url):
        share_url = self.get_share_url(url)
        share_url_parse = urlparse(share_url)
        if share_url_parse.netloc not in self.domain:
            raise Exception("无效的链接")
        dytk = None
        vid = re.findall(r'\/share\/video\/(\d*)', share_url_parse.path)[0]
        match = re.search(r'\/share\/video\/(\d*)', share_url_parse.path)
        if match:
            vid = match.group(1)
        response = requests.get(share_url, headers=self.headers, allow_redirects=False)
        match = re.search('dytk: "(.*?)"', response.text)
        print(vid)
        return self.get_data(vid,'')
        if match:
            dytk = match.group(1)

        if vid and dytk:
            return self.get_data(vid, dytk)
        else:
            raise Exception("解析失败")

    def get_share_url(self, url):
        response = requests.get(url,
                                headers=self.headers,
                                allow_redirects=False)
        if 'location' in response.headers.keys():
            return response.headers['location']
        else:
            raise Exception("解析失败")

    def format_duration(duration):
        """
        格式化时长
        :param duration 毫秒
        """

        total_seconds = int(duration / 1000)
        minute = total_seconds // 60
        seconds = total_seconds % 60
        return f'{minute:02}:{seconds:02}'

    def get_data(self, vid, dytk):
        url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={vid}"
        print(url)
        response = requests.get(url)
        #print(response.content)
        result = response.json()
        if not response.status_code == 200:
            raise Exception("解析失败")
        item = result.get("item_list")[0]
        author = item.get("author").get("nickname")
        mp4 = item.get("video").get("play_addr").get("url_list")[0]
        cover = item.get("video").get("cover").get("url_list")[0]
        mp4 = mp4.replace("playwm", "play")
        res = requests.get(mp4, headers=self.headers, allow_redirects=True)
        mp4url = res.url#res.headers['location']
        desc = item.get("desc")
        mp3 = item.get("music").get("play_url").get("url_list")[0]
        #name = input("===>正在下载保存视频,请输入视频名称：")
        video = requests.get(url=mp4url, headers=self.headers)
        with open(desc+".mp4", 'wb') as file:
            file.write(video.content)
            file.close()
            print("===>视频下载完成！")
        data = dict()
        data['mp3'] = mp3
        data['mp4'] = mp4url
        data['cover'] = cover
        data['nickname'] = author
        data['desc'] = desc
        data['duration'] = item.get("duration")
        return data


# 定义函数，flow代表经过中间人的所有数据 https://www.h3blog.com/article/python-mitmproxy-douyin-download/
def response(flow):
    print(flow.request.url)
# 如果经过中间人的请求中有以url或者url1开头请求，我就解析它的响应
    url = 'https://aweme.snssdk.com/aweme/v1/feed/'
    url1 = 'https://api.amemv.com/aweme/v1/feed/'
    if flow.request.url.startswith(url) or flow.request.url.startswith(url1):
        resp = flow.response.text
        data = json.loads(resp)
# 解析url地址和视频名称
        url_list = data['aweme_list']
        for url in url_list:
            video_url = url['video']['play_addr']['url_list'][0]
            video_name = url['desc']
# 利用下载神器wget进行下载，并保存本地（这里大家自由发挥，也可以存数据库什么的）
            wget.download(url=video_url, out='{}'.format(video_name))
dy = DY()

if __name__ == '__main__':
    pass
    # dy = DY()
    # url = input("请输入你要去水印的抖音短视频链接：")#https://v.douyin.com/oXbjfe/
    # data = dy.parse(url)
    # import pprint
    # pprint.pprint(data)