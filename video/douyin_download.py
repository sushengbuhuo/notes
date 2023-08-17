#!/usr/bin/env python
# encoding: utf-8

import os, sys, requests
import json, re, hashlib, time
import configparser
from retrying import retry
from contextlib import closing
 
class DouYin:
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }
        self.config = configparser.ConfigParser()
        self.shared_list = []
        self.history = []
        self.save_path = './download/'
        self.block_count = 50
        self.current_download_name = ''
        

    def read_config(self):
        urls  = input('请输入抖音主页链接：')#https://v.douyin.com/eLhwxF2/
        self.shared_list = urls.split(',')
    def remove(self):
        if os.path.exists(self.current_download_name):
            os.remove(self.current_download_name)
 
    def get_video_urls(self, sec_uid, max_cursor):
        user_url_prefix = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&max_cursor={1}&count=2000'
 
        i = 0
        result = []
        has_more = False
        while result == []:
            i = i + 1
            sys.stdout.write('---解析视频链接中，正在第 {} 次尝试...\r'.format(str(i)))
            sys.stdout.flush()

            user_url = user_url_prefix.format(sec_uid, max_cursor)
            response = self.get_request(user_url)
            html = json.loads(response.content.decode())
            if html['aweme_list'] != []:
                max_cursor = html['max_cursor']
                has_more = bool(html['has_more'])
                result = html['aweme_list']
 
        nickname = None
        video_list = []
        aweme_ids = []
        for item in result:
            if nickname is None:
                nickname = item['author']['nickname'] if re.sub(r'[\/:*?"<>|]', '', item['author']['nickname']) else None
 
            video_list.append({
                'desc': re.sub(r'[\/:*?"<>|]', '', item['desc']) if item['desc'] else '无标题' + str(int(time.time())),
                'url': item['video']['play_addr']['url_list'][0]
            })
            aweme_ids.append(item['aweme_id'])
        return nickname, video_list, max_cursor, has_more,aweme_ids
 

    #下载视频
    def video_downloader(self, video_url, video_name, types):
        if video_url == '':
            return
        size = 0
        video_url = video_url.replace('aweme.snssdk.com', 'api.amemv.com')
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                text = '----[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024)
                self.current_download_name = video_name
                with open(video_name, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
                        done = int(self.block_count * size / content_size)
                        sys.stdout.write('%s [下载进度]:%s%s %.2f%%\r' % (text, '█' * done, ' ' * (self.block_count - done), float(size / content_size * 100)))
                        sys.stdout.flush()
                os.rename(video_name, video_name+types)

 
    @retry(stop_max_attempt_number=3)
    def get_request(self, url, params=None):
        if params is None:
            params = {}
        response = requests.get(url, params=params, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response
 
    @retry(stop_max_attempt_number=3)
    def post_request(self, url, data=None):
        if data is None:
            data = {}
        response = requests.post(url, data=data, headers=self.headers, timeout=10)
        assert response.status_code == 200
        return response

    def get_sec_uid(self, url):
        rsp = self.get_request(url)
        sec_uid = re.search(r'sec_uid=.*?\&', rsp.url).group(0)
        return sec_uid[8:-1]

    def get_history(self):
        history = []
        with open('history.txt', 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            for line in lines:
                history.append(line.strip())

        return history

    def save_history(self, title):
        with open('history.txt', 'a+') as f:
            f.write(title.strip() + '\n')
    
    def run(self):
        self.read_config()
        self.history = self.get_history()
        print('---历史下载共 {0} 个视频'.format(len(self.history)))

        for url in self.shared_list:
            print('正在解析下载 ' + url)
            self.get_video_by_url(url)

    def get_video_by_url(self, url):
        max_cursor = 0
        has_more = True
        total_count = 0

        sec_uid = self.get_sec_uid(url)
        if not sec_uid:
            print('获取sec_uid失败')
            return
        print('---获取sec_uid成功: ' + sec_uid)
 
        while has_more:
            nickname, video_list, max_cursor, has_more,aweme_ids = self.get_video_urls(sec_uid, max_cursor)
            nickname_dir = os.path.join(self.save_path, nickname)
            # print(nickname_dir)
            if not os.path.exists(nickname_dir):
                os.makedirs(nickname_dir)

            page_count = len(video_list)
            total_count = total_count + page_count
            print('---视频下载中，共有{0}个作品，累计{1}个作品，翻页标识:{2} 是否还有更多内容:{3}\r'
                .format(page_count, total_count, max_cursor, has_more))

            for num in range(page_count):
                title = video_list[num]['desc']
                title = title.replace('@抖音小助手', '').strip()
                # print('---正在解析第{0}/{1}个视频 [{2}]，请稍后...'.format(num + 1, page_count, title))
                # print('mp3:'+f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aweme_ids[num]}')
                try:
                    music_res = json.loads(self.get_request(f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aweme_ids[num]}').text)
                    music_url = str(music_res['item_list'][0]['music']['play_url']['url_list'][0])
                    music_title = str(music_res['item_list'][0]['desc'])
                    
                except Exception as e:
                    music_url = ''
                    music_title = str(int(time.time()))
                # print(music_url,music_title)
                music_path = os.path.join(nickname_dir, music_title)
                video_path = os.path.join(nickname_dir, title)
                history_name = nickname + '\\' + title
                md5 = hashlib.md5(history_name.encode('utf-8')).hexdigest()
                if md5 in self.history:
                    print('---{0} -- 已下载...'.format(history_name))
                else:
                    self.video_downloader(video_list[num]['url'], video_path, '.mp4')
                    self.video_downloader(music_url, music_path, '.mp3')
                    self.history.append(md5)
                    self.save_history(md5)
                print('\n')
            print('---视频/音频下载完成...\r')

 
if __name__ == "__main__":
    app = DouYin()
    try:
        app.run()
    except KeyboardInterrupt:
        app.remove()
        input('\r\n按任意键退出')
        exit(0)
