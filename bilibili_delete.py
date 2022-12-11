import pprint
import requests
import json
import re
import os

# 最大删除条数https://www.52pojie.cn/thread-1720989-1-1.html
MAX_COUNT = 200
# 保存cookie的路径
COOKIE_FILE_PATH = r"./cookie.txt"

class BWebSite(object):

    def __init__(self):
        if not os.path.exists(COOKIE_FILE_PATH):
            print("未检测到cookie，请手动输入：")
            cookie = input()
            if re.search('DedeUserID=(.+?);', cookie) and re.search('bili_jct=(.+?);', cookie):
                with open(COOKIE_FILE_PATH, 'w', encoding='utf-8') as f:
                    f.write(cookie)
                print("*" * 50)
                print("输入成功".center(50))
                print("*" * 50)
            else:
                print('cookie输入错误')
                exit()
        else:
            with open(COOKIE_FILE_PATH, 'r', encoding='utf-8') as f:
                cookie = f.read()
                if not cookie:
                    print("cookie为空，请重新填入cookie")
                    os.remove(COOKIE_FILE_PATH)
                    exit()
        self.uid = re.search('DedeUserID=(.+?);', cookie)
        self.token = re.search('bili_jct=(.+?);', cookie)
        if not (self.uid and self.token):
            print("cookie错误，请重新填入")
            os.remove(COOKIE_FILE_PATH)
            exit()
        self.uid = self.uid.group(1)
        self.token = self.token.group(1)
        self.headers = {
            'authority': 'api.vc.bilibili.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://space.bilibili.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': f'{cookie}',
        }

    # 获取动态信息
    @property
    def dynamic(self):
        dynamic_id = 0
        params = (
            ('visitor_uid', f'{self.uid}'),
            ('host_uid', f'{self.uid}'),
            ('offset_dynamic_id', f'{dynamic_id}'),
            ('need_top', '1'),
            ('platform', 'web'),
        )
        list_cards = []
        response = requests.get('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history',
                                headers=self.headers,
                                params=params)
        data = json.loads(response.text)['data']
        while data.get('cards'):
            cards = data['cards']
            dynamic_id = data['next_offset']
            for card in cards:
                list_cards.append(card)
            if len(list_cards) >= MAX_COUNT:
                return list_cards
            params = (
                ('visitor_uid', f'{self.uid}'),
                ('host_uid', f'{self.uid}'),
                ('offset_dynamic_id', f'{dynamic_id}'),
                ('need_top', '1'),
                ('platform', 'web'),
            )
            response = requests.get('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history',
                                    headers=self.headers,
                                    params=params)
            data = json.loads(response.text)['data']
        return list_cards

    # 删除动态信息
    def delete_dynamic(self):
        list_dynamic_id = []
        for dynamic in self.dynamic:
            list_dynamic_id.append(dynamic['desc']['dynamic_id'])
        for dynamic_id in list_dynamic_id:
            data = {
                'dynamic_id': f'{dynamic_id}',
                'csrf_token': f'{self.token}',
                'csrf': f'{self.token}'
            }
            response = requests.post('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic',
                                     headers=self.headers,
                                     data=data)
            code = json.loads(response.text)['code']
            if code == 0:
                print(f"{dynamic_id}删除成功")

    # 获取所有回复
    @property
    def comments(self):
        params = (
            ('platform', 'web'),
            ('build', '0'),
            ('mobi_app', 'web'),
        )
        response = requests.get('https://api.bilibili.com/x/msgfeed/reply', headers=self.headers, params=params)
        ls = []
        data = json.loads(response.text)['data']
        while not data['cursor']['is_end']:
            ls.append(data)
            if len(ls) > MAX_COUNT:
                return ls
            cursor = data['cursor']
            comment_id = cursor['id']
            time = cursor['time']
            params = (
                ('id', f'{comment_id}'),
                ('reply_time', f'{time}'),
                ('platform', 'web'),
                ('build', '0'),
                ('mobi_app', 'web'),
            )
            response = requests.get('https://api.bilibili.com/x/msgfeed/reply', headers=self.headers, params=params)
            data = json.loads(response.text)['data']
        return ls

    # 删除回复
    def delete_comment(self):
        for comment in self.comments:
            for item in comment['items']:
                subject_id = item['item']['subject_id']
                target_id = item['item']['target_id']
                title = item['item']['title']
                data = {
                    'oid': f'{subject_id}',
                    'type': '1',
                    'jsonp': 'jsonp',
                    'rpid': f'{target_id}',
                    'csrf': f'{self.token}'
                }
                response = requests.post('https://api.bilibili.com/x/v2/reply/del', headers=self.headers, data=data)
                # data = json.loads(response.text)
                # print(data)
                code = json.loads(response.text)['code']
                if code == 0:
                    print(f"{title}-----------下面的回复已删除")

    # 获取所有收到赞的回复
    @property
    def likes(self):
        params = (
            ('platform', 'web'),
            ('build', '0'),
            ('mobi_app', 'web'),
        )
        response = requests.get('https://api.bilibili.com/x/msgfeed/like', headers=self.headers, params=params)
        ls = []
        data = json.loads(response.text)['data']
        total = json.loads(response.text)['data']['total']
        while not total['cursor']['is_end']:
            ls.append(data)
            if len(ls) > MAX_COUNT:
                return ls
            cursor = total['cursor']
            comment_id = cursor['id']
            time = cursor['time']
            params = (
                ('id', f'{comment_id}'),
                ('like_time', f'{time}'),
                ('platform', 'web'),
                ('build', '0'),
                ('mobi_app', 'web'),
            )
            response = requests.get('https://api.bilibili.com/x/msgfeed/like', headers=self.headers, params=params)
            data = json.loads(response.text)['data']
            total = json.loads(response.text)['data']['total']
        return ls

    def delete_like(self):
        for like in self.likes:
            for item in like['total']['items']:
                native_uri = item['item']['native_uri']
                item_id = item['item']['item_id']
                title = item['item']['title']
                rpid = item_id
                print(native_uri, title)
                oid = re.search("//video/(\d+)", native_uri)
                if not oid:
                    oid = re.search('//following/detail/(\d+)', native_uri)
                    if not oid:
                        oid = re.search('//album/(\d+)', native_uri)
                if not oid:
                    continue
                oid = oid.group(1)
                print(oid, rpid)
                data = {
                    'oid': f'{oid}',
                    'type': '1',
                    'jsonp': 'jsonp',
                    'rpid': f'{rpid}',
                    'csrf': f'{self.token}'
                }
                response = requests.post('https://api.bilibili.com/x/v2/reply/del', headers=self.headers, data=data)
                # data = json.loads(response.text)
                # print(data)
                code = json.loads(response.text)['code']
                if code == 0:
                    print(f"{title}-----------下面的回复已删除")

    # 获取所有关注
    @property
    def follows(self):
        vmid = f'{self.uid}'
        pn = 1
        list_follows = []
        h = self.headers
        h.update(
            {
                'referer': f'https://space.bilibili.com/{self.uid}/fans/follow?tagid=-10',
            }
        )
        while True:
            params = (
                ('vmid', f'{vmid}'),
                ('pn', f'{pn}'),
                ('ps', '20'),
                ('order', 'desc'),
                ('order_type', 'attention'),
                ('jsonp', 'jsonp'),
                ('callback', '__jp7'),
            )
            response = requests.get('https://api.bilibili.com/x/relation/followings', headers=h,
                                    params=params)
            data = json.loads(response.text[response.text.index('(') + 1:response.text.rindex(')')])['data']
            list_data = data['list']
            total = data['total']
            for item in list_data:
                list_follows.append(item)
            if total > MAX_COUNT and len(list_follows) == MAX_COUNT:
                break
            if len(list_follows) == total:
                break
            pn += 1
        return list_follows

    # 删除所有
    def delete_follows(self):
        follows = self.follows
        for follow in follows:
            mid = follow['mid']
            uname = follow['uname']
            data = {
                'fid': f'{mid}',
                'act': '2',
                're_src': '11',
                'spmid': '333.999.0.0',
                'extend_content': f'{{"entity":"user","entity_id":{mid}}}',
                'jsonp': 'jsonp',
                'csrf': f'{self.token}'
            }
            response = requests.post('https://api.bilibili.com/x/relation/modify', headers=self.headers, data=data)
            code = json.loads(response.text)['code']
            if code == 0:
                print(f'{uname}----------取消关注成功')

web = BWebSite()
# web.delete_comment()
# web.delete_like()
# web.delete_dynamic()
# pprint.pprint(web.follows)
# web.delete_follows()
