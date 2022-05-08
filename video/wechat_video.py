import os
import re
from time import sleep
import requests
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup
#硕鼠解析可以直接返回得到文章内的视频下载链接，根据获得的链接进行视频下载即可。
def download_url(url):
    try:
        path = os.getcwd()#获取当前的文件位置
        filepath = path
        if os.path.exists(filepath) == False:#判断是否存在filepath，不存在则创建文件夹
            os.mkdir(filepath)
        URL = 'https://www.flvcd.com/parse.php?format=&kw=' + str(url).replace('/', '%2F').replace(':', '%3A').replace(
            '?', '%3F').replace('=', '%3D').replace('&', '%26').replace(';', '%3B').replace('#', '%23')#构造硕鼠的解析链接
        # print(URL)
        headers = {'UserAgent': 'str(UserAgent).random'}
        response = requests.get(URL, headers=headers)
        response.encoding = 'gbk'
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup = str(soup)
        regex_title = re.compile(
            r'document.title = "(.*?)" ')
        title = re.findall(regex_title, soup)[0]#获取title
        # print(title)
        regex_href = re.compile(r'href="(.*?)"', re.S)
        href = re.findall(regex_href, soup)[9]#获取视频下载地址
        # print(href)
        video_response = requests.get(href, headers=headers)
        print('正在下载{}，请稍后。。。。。。'.format(title))
        with open(filepath + f'\\{title}.mp4', mode='wb') as f:
            f.write(video_response.content)
            sleep(10)
        print('下载完成！！！')
    except:
        print(f'下载失败，请确认该文章内含有视频，失败链接是：{url}')

if __name__ == '__main__':
    url = 'http://mp.weixin.qq.com/s?__biz=MjM5MDMyMzMxMg==&mid=2247687337&idx=5&sn' \
          '=efd74900ff01a778bb0a879a2c6dda30&chksm' \
          '=a64adbb6913d52a0908e5ae580ae7f3aa7bbb4b32a2271d7a9e9b7875af84362a2c247479125&scene=21#wechat_redirect '

    download_url(url)
