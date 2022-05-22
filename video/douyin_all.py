import os
 
import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
 
#https://www.52pojie.cn/thread-1634311-1-1.html
class Douyin:
    def __init__(self, url):
        self.share_url = url
        self.headers = {
            'User-Agent': "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3"
        }
        self.sec_uid = None
        self.nick_name = None
 
    def get_user_info(self):
        resp = requests.get(self.share_url, headers=self.headers)
        self.sec_uid = re.search(r'sec_uid=[\S]{0,76}&', resp.url).group().strip('&').strip('sec_uid=')
        user_info = f'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={self.sec_uid}'
        resp = requests.get(user_info, headers=self.headers)
        user_data = {
            'signature': resp.json()['user_info']['signature'],
            'nickname': resp.json()['user_info']['nickname'],
            'aweme_count': resp.json()['user_info']['aweme_count'],
            'following_count': resp.json()['user_info']['following_count'],
            'total_favorited': resp.json()['user_info']['total_favorited'],
            'avatar': resp.json()['user_info']['avatar_larger']['url_list'][0]
        }
        self.nick_name = resp.json()['user_info']['nickname']
        return user_data
 
    def get_all_video(self):
        max_cursor = 0
        video_has_more = True
        all_video_list = []
        if self.sec_uid is None:
            self.get_user_info()
        while video_has_more is True:
            json_url = f'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={self.sec_uid}&' \
                       f'count=21&max_cursor={max_cursor}'
            resp = requests.get(json_url, headers=self.headers)
            video_has_more = resp.json()['has_more']
            max_cursor = resp.json()['max_cursor']
            video_list = resp.json()['aweme_list']
            for i in video_list:
                all_video_list.append({'desc': i['desc'], 'vid': i['video']['vid'], 'aweme_id': i['aweme_id']})
        return all_video_list
 
    def down_video(self, down_info):
        if os.path.exists(self.nick_name) is False:
            try:
                os.makedirs(self.nick_name)
            except FileExistsError:
                pass
        if down_info['desc'] == '':
            down_info['desc'] = down_info['aweme_id']
        download_url = f'https://aweme.snssdk.com/aweme/v1/play/?video_id={down_info["vid"]}&ratio=1080p'
        response = requests.get(download_url, headers=self.headers)
        with open(f'{self.nick_name}/{down_info["desc"]}.mp4', 'wb') as file:
            file.write(response.content)
        print(down_info['aweme_id'] + ' 下载完毕')
 
 
if __name__ == '__main__':
    share_url = re.search(r'[a-zA-z]+://[^\s]*', input('输入分享链接:')).group()
    douyin = Douyin(share_url)
    info = douyin.get_user_info()
    print(f'作者:{info["nickname"]}\n视频数:{info["aweme_count"]}')
    down_list = douyin.get_all_video()
    print(f'视频列表获取完毕开始下载 总视频数')
    pool = ThreadPool(10)
    results = pool.map(douyin.down_video, down_list)
    pool.close()
    pool.join()