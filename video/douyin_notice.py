import base64
import datetime
import hashlib
import hmac
import json
import re
import time
import urllib
 
import requests
 
# 抖音用户 主页链接
douyin_home_page = 'https://v.douyin.com/****/'
 
headers_douyin = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.114 Mobile Safari/537.36 "
}
 
headers_DingDing = {
    'Content-Type': 'application/json;charset=utf-8'
}
 
 
def get_sec_uid():
    short_url = re.findall('[a-z]+://[\S]+', douyin_home_page, re.I | re.M)[0]
    start_page = requests.get(url=short_url, headers=headers_douyin, allow_redirects=False)
    location = start_page.headers['location']
    sec_uid = re.findall('(?<=sec_uid=)[a-z，A-Z，0-9, _, -]+', location, re.M | re.I)[0]
    return sec_uid
 
 
def get_user_info(sec_uid):
    userinfo = requests.get(url='https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={}'.format(sec_uid),
                            headers=headers_douyin).json()
    name = userinfo['user_info']['nickname']
    print(userinfo)
    print(name)
 
 
def get_video_list(shape_id):
    """
    根据sec_uid 获取出置顶外 第一个视频 count=1
    """
    sign_ = "HunHKQABfpAtN81GL5ujHx7pvd"
    url = f"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={shape_id}&count=1&max_cursor=0&aid=1128&_signature={sign_}"
    resp = requests.get(url)
    resp_result = resp.json()
    return resp_result['aweme_list']
 
 
def get_video_detail(aweme_id):
    """
    根据id 获取单个视频明细
    """
    url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + aweme_id
    r = requests.get(url=url, headers=headers_douyin).json()
    return r
 
 
def timeStamp(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y%m%d %H:%M:%S", timeArray)
    return otherStyleTime
 
 
def get_notice_text():
    vide_list = get_video_list(get_sec_uid())
    if len(vide_list) > 0:
        aweme_id = vide_list[0]['aweme_id']
        print(aweme_id)
        video_detail = get_video_detail(aweme_id)
        print(video_detail)
        # 发表时间
        create_time = video_detail['item_list'][0]['create_time']
        # 文本内容
        desc = video_detail['item_list'][0]['desc']
        # 视频url
        video_url = video_detail['item_list'][0]['video']['play_addr']['url_list'][0]
        cover = video_detail['item_list'][0]['video']['cover']['url_list'][0]
        created_at_time = datetime.datetime.strptime(timeStamp(create_time), '%Y%m%d %H:%M:%S')
        now_time = datetime.datetime.now() + datetime.timedelta(hours=8)
        if (now_time - created_at_time).total_seconds() <= 1800:
            noticeDouyinDing(timeStamp(create_time), desc, video_url, cover)
 
 
def noticeDouyinDing(create_time, text, url, cover):
    """
    通知钉钉https://www.52pojie.cn/thread-1619783-1-1.html
    """
    timestamp = str(round(time.time() * 1000))
    # 自己的密钥（群聊创建机器人 才有）
    secret = '*********'
    # 自己的token （群聊创建机器人 才有）
    access_token = '******************'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    api_url = "https://oapi.dingtalk.com/robot/send?access_token=" + access_token + "×tamp=" + timestamp + "&sign=" + sign
    data_dict = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": "抖音通知",
            "text": "![cover](" + cover + ") 发表时间: " + create_time + "\n\n>" + text,
            "btnOrientation": "0",
            "singleTitle": "点击进入",
            "singleURL": url
        }
    }
    r = requests.post(api_url, data=json.dumps(data_dict), headers=headers_DingDing).json()
    code = r["errcode"]
    if code == 0:
        print("通知成功")
    else:
        print("通知失败")
 
 
if __name__ == '__main__':
    get_notice_text()