
# gzh_download.py
# 引入模块
import requests
import json
import re
import random
import time
import pdfkit

# 打开 cookie.txt
with open("cookie.txt", "r") as file:
    cookie = file.read()
cookies = json.loads(cookie)
url = "https://mp.weixin.qq.com"
#请求公号平台
response = requests.get(url, cookies=cookies)
# 从url中获取token
token = re.findall(r'token=(\d+)', str(response.url))[0]
# 设置请求访问头信息
headers = {
    #          https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid=MzI1NjAxOTI0Ng==&type=9&query=&token=1098806330&lang=zh_CN&f=json&ajax=1
    "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=" + token + "&lang=zh_CN",
    "Host": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

# 循环遍历前10页的文章
for j in range(1, 10, 1):
    begin = (j-1)*5
    # 请求当前页获取文章列表
    #https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid=MjM5MjAzODU2MA==&type=9&query=&token=310737197&lang=zh_CN&f=json&ajax=1
    requestUrl = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin="+str(begin)+"&count=5&fakeid=MjM5MjAzODU2MA==&type=9&query=&token=" + token + "&lang=zh_CN&f=json&ajax=1"
    search_response = requests.get(requestUrl, cookies=cookies, headers=headers)
    # 获取到返回列表 Json 信息
    re_text = search_response.json()
    list = re_text.get("app_msg_list")
    #https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid=Mzg2NzIzOTQ4NQ==&type=9&query=&token=1098806330&lang=zh_CN&f=json&ajax=1
    # 遍历当前页的文章列表
    for i in list:
        # 将文章链接转换 pdf 下载到当前目录
        pdfkit.from_url(i["link"], i["title"] + ".pdf")
    # 过快请求可能会被微信问候，这里进行10秒等待
    time.sleep(10)
