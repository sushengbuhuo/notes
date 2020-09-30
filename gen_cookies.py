
# get_cookies.py

import json

# 从浏览器中复制出来的 Cookie 字符串
cookie_str = "把cookie字符串都复制到这里来"

cookie = {}
# 遍历 cookie 信息
for cookies in cookie_str.split("; "):
    cookie_item = cookies.split("=")
    cookie[cookie_item[0]] = cookie_item[1]
# 将cookies写入到本地文件
with open('cookie.txt', "w") as file:
    #  写入文件
    file.write(json.dumps(cookie))