# -*- coding: utf-8 -*-
import json
import requests
import time
import random
 
 
class bili_exp:
    """
    登录bilibili网页，浏览器按F12-网络，刷新浏览器在开发者工具里找cookie复制https://www.52pojie.cn/thread-1564164-1-1.html
    """
 
    def __init__(self, c, coin_operated=None):
        self.cookie = c if type(c) == dict else self.extract_cookies(c)
        self.coin_operated = coin_operated
        self.s = requests.Session()
        self.headers = {"Content-Type": "application/x-www-form-urlencoded",
                        "Connection": "keep-alive",
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4728.0 Safari/537.36 Edg/98.0.1093.6'}
        self.csrf = self.cookie['bili_jct']
 
    @staticmethod
    def extract_cookies(cookies):
        cookies = dict([i.split("=", 1) for i in cookies.split("; ")])
        return cookies
 
    def getCoin(self):
        """
        获取硬币数量
        """
        url = "http://account.bilibili.com/site/getCoin"
        res = self.s.get(url, cookies=self.cookie, headers=self.headers).json()
        money = res['data']['money']
        return int(money)
 
    def getInfo(self):
        url = "http://api.bilibili.com/x/space/myinfo"
        data = self.s.get(url, cookies=self.cookie, headers=self.headers).json()['data']
        global username
        username = data['name']
        global uid
        uid = data['mid']
        level = data['level']
        current_exp = data['level_exp']['current_exp']
        next_exp = data['level_exp']['next_exp']
        require_exp = int(next_exp) - int(current_exp)
        if self.coin_operated:
            days = int(int(require_exp) / 65)
        else:
            days = int(int(require_exp) / 15)
        coin = self.getCoin()
        msg = f"昵称 {username} ，当前等级：{level}，当前经验值：{current_exp}，还需{require_exp}经验值升级，需要{days}天，当前硬币数：{coin}"
        return current_exp, msg
 
    def getvideo(self):
        uids = ['18982710', '10671515', '2638959']
        # 观看、分享和投币指定up的视频  https://space.bilibili.com/18982710
        url = f'https://api.bilibili.com/x/space/arc/search?mid={random.choice(uids)}'
        res = self.s.get(url, headers=self.headers).json()['data']['list']['vlist']
        return res
 
    def viewvideo(self, bvid):
        playedTime = random.randint(10, 100)
        url = "https://api.bilibili.com/x/click-interface/web/heartbeat"
        data = {
            'bvid': bvid,
            'played_time': playedTime,
            'csrf': self.csrf
        }
        j = self.s.post(url, data=data).json()
        code = j['code']
        if code == 0:
            print('看视频完成!')
        else:
            print('看视频失败!')
 
    def sharevideo(self, bvid):
        url = "https://api.bilibili.com/x/web-interface/share/add"
        data = {
            'bvid': bvid,
            'csrf': self.csrf
        }
        res = self.s.post(url, data=data, cookies=self.cookie, headers=self.headers).json()
        code = res['code']
        if code == 0:
            print('分享成功!')
        else:
            print('分享失败!')
 
    def toubi(self, bvid, aid):  # 投币
        coinNum = self.getCoin()
        if coinNum == 0:
            print('太穷了，硬币不够!')
            return -99
        url = "https://api.bilibili.com/x/web-interface/coin/add"
        data = {
            'aid': aid,
            'multiply': 1,
            'select_like': 1,
            'cross_domain': 'true',
            'csrf': self.csrf
        }
        self.headers['referer'] = f'https://www.bilibili.com/video/{bvid}'
        res = self.s.post(url, data=data, cookies=self.cookie, headers=self.headers).json()
        code = res['code']
        if code == 0:
            print(bvid + ' 投币成功!')
            return 1
        else:
            print(bvid + ' 投币失败!')
            return 0
 
    def task(self):
        coin_num = self.getCoin()
        k = 0
        for i in range(10):
            j = 0
            vlist = self.getvideo()
            random_list = random.randint(0, len(vlist) - 1)
            bvid = vlist[random_list]['bvid']
            title = vlist[random_list]['title']
            up = vlist[random_list]['author']
            aid = vlist[random_list]['aid']
            print('-' * 30 + f'\n正在观看视频 {i + 1}. {bvid} - {title} - {up}')
            self.viewvideo(bvid)
            time.sleep(1)
            self.sharevideo(bvid)
            time.sleep(1)
            if self.coin_operated and coin_num:
                while k < min(coin_num, 5) and j <= 2:
                    coin_code = self.toubi(bvid, aid)
                    time.sleep(1)
                    if coin_code == 1:
                        k += 1
                        coin_num -= 1
                        j -= 1
                        break
                    elif not coin_code:
                        j += 1
        #推送微信消息
    def robot(self,text):
        title = "b站升级消息"
        token="8f8994af17544d77adf86d47700fb60e"
        url = f"http://pushplus.hxtrip.com/send?token={token}&title={title}&content={text}&template=html"
        try:
            if token:
                r = requests.get(url)
        except:
            pass
    def start(self):
        exp1, msg = self.getInfo()
        print(msg)
        print(f'{username}：')
        self.task()
        exp2, a = self.getInfo()
        text_msg = msg + f' 任务完成，获得经验值{int(exp2) - int(exp1)} '
        self.robot(text_msg)
        print('-' * 30 + f'\n任务完成，获得经验值{int(exp2) - int(exp1)}\n' + '-' * 30 + '\n')
 
 
def main():
    cookie = "xxx"  # 浏览器开发者工具复制cookie,支持多账号，cookie之间用&连接
    for c in cookie.split('&'):
        b = bili_exp(c)  # 不投币取消本行注释，并注释下一行
        # b = bili_exp(c, 1)  # 投币需注释上一行，并取消本行注释
        b.start()
 

def main_handler(*args):  # 腾讯云函数
    main()
 
 
def handler(*args):  # 阿里云函数
    main()
 
 
if __name__ == '__main__':
    main()