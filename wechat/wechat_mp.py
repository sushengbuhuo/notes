import json
import requests
import time
import random
import os
import yaml
import sys
#抓取公众号后台文章https://xuzhougeng.top/archives/wechatarticleparseri python wechat_parser.py wechat.yaml
if len(sys.argv) < 2:
    print("too few arguments")
    sys.exit(1)

yaml_file = sys.argv[1]
if not os.path.exists(yaml_file):
    print("yaml_file is not exists")
    sys.exit(1)
    

with open(yaml_file, "r") as file:
    file_data = file.read()
config = yaml.safe_load(file_data)

headers = {
    "Cookie": config['cookie'],
    "User-Agent": config['user_agent'] 
}

# 请求参数
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
begin = "0"
params = {
    "action": "list_ex",
    "begin": begin,
    "count": "5",
    "fakeid": config['fakeid'],
    "type": "9",
    "token": config['token'],
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1"
}

# 存放结果
if os.path.exists("mp_data.json"):
    with open("mp_data.json", "r") as file:
        app_msg_list = json.load(file)
else:
    app_msg_list = []
# 在不知道公众号有多少文章的情况下，使用while语句
# 也方便重新运行时设置页数
i = len(app_msg_list) // 5
while True:
    begin = i * 5
    params["begin"] = str(begin)
    # 随机暂停几秒，避免过快的请求导致过快的被查到
    time.sleep(random.randint(1,10))
    resp = requests.get(url, headers=headers, params = params, verify=False)
    # 微信流量控制, 退出
    if resp.json()['base_resp']['ret'] == 200013:
        print("frequencey control, stop at {}".format(str(begin)))
        break
    
    # 如果返回的内容中为空则结束
    if len(resp.json()['app_msg_list']) == 0:
        print("all ariticle parsed")
        break
        
    app_msg_list.append(resp.json())
    # 翻页
    i += 1

# 保存结果为JSON
json_name = "mp_data.json"
with open(json_name, "w") as file:
    file.write(json.dumps(app_msg_list, indent=2, ensure_ascii=False))
#pc微信公众号数据分析 https://mp.weixin.qq.com/s?__biz=MzU4OTYzNjE2OQ==&mid=2247484999&idx=1&sn=714f7112d0dd15ca446e4bb06cb5f864&chksm=fdcb3161cabcb877ced00eb1cd8d634b8d11aff28c62c26777a0076f3cc82191e8d374738095&scene=21#wechat_redirect
def parse(__biz, uin, key, pass_ticket, appmsg_token="", offset="0"):
    """
    文章信息获取
    """
    url = 'https://mp.weixin.qq.com/mp/profile_ext'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400",
    }
    params = {
        "action": "getmsg",
        "__biz": __biz,
        "f": "json",
        "offset": str(offset),
        "count": "10",
        "is_ok": "1",
        "scene": "124",
        "uin": uin,
        "key": key,
        "pass_ticket": pass_ticket,
        "wxtoken": "",
        "appmsg_token": appmsg_token,
        "x5": "0",
    }

    res = requests.get(url, headers=headers, params=params, timeout=3)
    data = json.loads(res.text)
    # 获取信息列表
    msg_list = eval(data.get("general_msg_list")).get("list", [])
    for i in msg_list:
        # 去除文字链接
        try:
            # 文章标题
            title = i["app_msg_ext_info"]["title"].replace(',', '，')
            # 文章摘要
            digest = i["app_msg_ext_info"]["digest"].replace(',', '，')
            # 文章链接
            url = i["app_msg_ext_info"]["content_url"].replace("\\", "").replace("http", "https")
            # 文章发布时间
            date = i["comm_msg_info"]["datetime"]
            print(title, digest, url, date)
            with open('article.csv', 'a') as f:
                f.write(title + ',' + digest + ',' + url + ',' + str(date) + '\n')
        except:
            pass
    # 判断是否可继续翻页 1-可以翻页  0-到底了
    if 1 == data.get("can_msg_continue", 0):
        time.sleep(3)
        parse(__biz, uin, key, pass_ticket, appmsg_token, data["next_offset"])
    else:
        print("爬取完毕")


if __name__ == '__main__':
    # 请求参数
    __biz = '你的参数'
    uin = '你的参数'
    key = '你的参数'
    pass_ticket = '你的参数'
    # 解析函数
    parse(__biz, uin, key, pass_ticket, appmsg_token="", offset="0")