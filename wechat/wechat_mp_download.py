import json
import requests
import time
import random
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        "Cookie": '',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
begin = "0"
params = {
    "action": "list_ex",
    "begin": begin,
    "count": "5",
    "fakeid": 'MjM5NjM4MDAxMg==',#其他公众号id
    "type": "9",
    "token": '',#自己token
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1"
}
app_msg_list = []
with open("wechat_articles_list.csv", "w",encoding='utf-8-sig') as file:
    file.write("文章封面,标题,链接,时间\n")
i = 0
while True:
    begin = i * 5
    params["begin"] = str(begin)
    # 随机暂停几秒，避免过快的请求导致过快的被查到
    time.sleep(random.randint(1,2))
    resp = requests.get(url, headers=headers, params = params, verify=False)
    # 微信流量控制, 退出
    if resp.json()['base_resp']['ret'] == 200013:
        print("frequencey control, stop at {}".format(str(begin)))
        time.sleep(3)
        continue
    
    # 如果返回的内容中为空则结束
    if len(resp.json()['app_msg_list']) == 0:
        print("all ariticle parsed")
        break
        
    msg = resp.json()
    if "app_msg_list" in msg:
        for item in msg["app_msg_list"]:
            print(item)
            info = '"{}","{}","{}","{}"'.format(str(item["cover"]), item['title'], item['link'], time.strftime('%Y-%m-%d', time.localtime(item['create_time'])))
            with open("wechat_articles_list.csv", "a",encoding='utf-8-sig') as f:
                f.write(info+'\n')
        print(f"第{i}页爬取成功\n")
        print("\n".join(info.split(",")))
    # 翻页
    i += 1    