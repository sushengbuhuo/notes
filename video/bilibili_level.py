# -*- coding: utf8 -*-

import requests
import json
import time

# 填写cookie即可运行 https://www.52pojie.cn/thread-1556299-1-1.html
'''
1、浏览器登入哔哩网站
2、访问 http://api.bilibili.com/x/space/myinfo
3、F12看到cookie的值粘贴即可
'''
cookies = "xxxx"

def extract_cookies(cookies):
    global csrf
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    csrf = cookies['bili_jct']
    return cookies

# 银币数

def getCoin():
    cookie = extract_cookies(cookies)
    url = "http://account.bilibili.com/site/getCoin"
    r = requests.get(url, cookies=cookie).text
    j = json.loads(r)
    money = j['data']['money']
    return money

# 个人信息

def getInfo():
    global uid
    url = "http://api.bilibili.com/x/space/myinfo"
    cookie = extract_cookies(cookies)
    r = requests.get(url, cookies=cookie).text
    j = json.loads(r)
    uid = j['data']['mid']
    name = j['data']['name']
    level = j['data']['level']
    current_exp = j['data']['level_exp']['current_exp']
    next_exp = j['data']['level_exp']['next_exp']
    sub_exp = int(next_exp)-int(current_exp)
    days = int(int(sub_exp)/65)
    coin = getCoin()
    msg = "当前等级为"+str(level) + " ,经验值为" + \
        str(current_exp)+",距升级还需要经验值 "+str(sub_exp) + \
        "  时间 "+str(days)+" 天"+"，硬币数为"+str(coin)
    robot(msg)
    print(msg)

# 推荐动态

def getActiveInfo():
    url = "http://api.bilibili.com/x/web-interface/archive/related?aid=" + \
        str(7)
    cookie = extract_cookies(cookies)
    r = requests.get(url, cookies=cookie).text
    j = json.loads(r)
    return j

# 投币 分享5次

def Task():
    j = getActiveInfo()
    data = j['data']
    coin_count = 0
    for i in range(0, len(data)):
        bvid = data[i]['bvid']
        aid = data[i]['aid']
        print(str(bvid)+' -- '+str(aid))
        if coin_count < 5:
            coin_code = tocoin(bvid)
            if coin_code == -99:
                return
        try:
            toshare(aid)
        except Exception as e:
            pass
        time.sleep(3)
        if coin_code == 1:
            coin_count = coin_count+1
        if coin_count == 5:
            break
        print('##########')

# 投币函数
def tocoin(bvid):
    coinNum = getCoin()
    if coinNum == 0:
        print('硬币不足')
        return -99
    url = "http://api.bilibili.com/x/web-interface/coin/add"
    data = {
        'bvid': bvid,
        'multiply': 1,
        'select_like': 1,
        'csrf': csrf
    }
    cookie = extract_cookies(cookies)
    r = requests.post(url, data=data, cookies=cookie).text
    j = json.loads(r)
    code = j['code']
    print("code="+str(code))
    if code == 0:
        print(str(bvid)+' 投币成功 !')
        return 1
    else:
        print(str(bvid)+' 投币失败!')
        return 0

# 分享视频

def toshare(rid):
    url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/share"
    data = {
        'uid': 0,
        'type': 8,
        'share_uid': 0,
        'content': 'testing!',
        'rid': rid,
        'csrf': csrf
    }
    cookie = extract_cookies(cookies)
    r = requests.post(url, data=data, cookies=cookie).text
    j = json.loads(r)
    code = j['code']
    dynamic_id = j['data']['dynamic_id']
    if code == 0:
        print('分享视频成功')
    else:
        print('分享视频失败')
    time.sleep(2)
    todelshare(dynamic_id)

# 删除动态

def todelshare(dynamic_id):
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic"
    data = {
        'dynamic_id': dynamic_id,
        'csrf': csrf
    }
    cookie = extract_cookies(cookies)
    r = requests.post(url, data=data, cookies=cookie).text
    j = json.loads(r)
    code = j['code']
    if code == 0:
        print('删除动态成功')
    else:
        print('删除动态失败')
#推送微信消息
def robot(text):
    title = "b站升级消息"
    token="8f8994af17544d77adf86d47700fb60e"
    url = f"http://pushplus.hxtrip.com/send?token={token}&title={title}&content={text}&template=html"
    try:
        if token:
            r = requests.get(url)
    except:
        pass
def run():
    getInfo()
    Task()

def main_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))
    run()
    return("运行结束")

if __name__ == '__main__':
    run()
