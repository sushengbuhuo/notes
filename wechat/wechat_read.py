import time
import requests
import json


# 目标url
url = "http://mp.weixin.qq.com/mp/getappmsgext"
# 添加Cookie避免登陆操作，这里的"User-Agent"最好为手机浏览器的标识 https://www.its203.com/article/wnma3mz/78570580
headers = {
    "Cookie": 'pgv_pvid=3462479730;sd_userid=26861634200545809;sd_cookie_crttime=1634200545809;tvfe_boss_uuid=2462cb91e2efc262;ua_id=BbSW7iXpRV9kLjy3AAAAAJnbZGccv_XAw3N3660mGLU=;wxuin=1541436403;lang=zh_CN;devicetype=Windows10x64;version=63040026;pass_ticket=49VtuZM5BD+2FwRgVp/qQe+RJZ7htI6chbyYY0kyLTD2sRTalhGiv3ZoCuHvUkax;rewardsn=;  wxtokenkey=777;appmsg_token=1142_4UBRaKzI8heNhPvIticaNMVVQyuahECjvOuiy2UszU7MbG4Z-JMRCeGOA9sAiLgZNbK__0dLflo8-pJl;wap_sid2=CPPngd8FEooBeV9IQkRwd18zbU5US0pycjc3UHRyYnpPbTJBdEgwZ19FZHBsZm1QTWpPekgxay1rYW1YSUN6d195REdka2lWbHJ5WlRnMlpyQTZNcGVMLUN0a3BWM0RTX2tYRnBZcnhfZ0hYbjFFeTdGRXh1TWsyRGVpNkRxUVdDUlJzUnlmdm8yV3BsUVNBQUF+MLq5t40GOA1AAQ==;',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.27.400 QQBrowser/9.0.2524.400"
}


data = {
    "is_only_read": "1",
    "is_temp_url": "0",                
    "appmsg_type": "9", # 新参数，不加入无法获取like_num
}
"""
添加请求参数
__biz对应公众号的信息，唯一
mid、sn、idx分别对应每篇文章的url的信息，需要从url中进行提取
key、appmsg_token从fiddler上复制即可
pass_ticket对应的文章的信息，貌似影响不大，也可以直接从fiddler复制
"""
your__biz='MzIxNDA0MTExMg=='
article_mid='2652131858'
article_sn='d244ed277a11f4fabf145d0ba329e3c6'
article_idx='1'
yourkey='33b3ce9713fe05567363897a789cddaceefce2c7946fc50feac1d932b9ceb12c4a292e012b23edbf323730932a7d2660f88d37caa0a10726f9fb8bc7348dc5aed75e50df9d4fa89264be85c1fb8b707194172cfcc50ae07617c72c838efe46d814d3e61ba70bba3cd24ab1aa2eeec8f91d5c3cf028dfb7fe6d4e29c094ffab79'
pass_ticket='49VtuZM5BD+2FwRgVp/qQe+RJZ7htI6chbyYY0kyLTD2sRTalhGiv3ZoCuHvUkax'
yourappmsg_token='1142_tfTRZ30asDOsvLhsQVb6S_4RkADrESRZqQz1tzW-QZdjRDET_8a0eQEJDIQ9uNy87PUOSQnO2vbWArMm'
params = {
    "__biz": your__biz,
    "mid": article_mid,
    "sn": article_sn,
    "idx": article_idx,
    "key": yourkey,
    "pass_ticket": pass_ticket,
    "appmsg_token": yourappmsg_token,
}
# 使用post方法进行提交 Python 也可以分析公众号https://cloud.tencent.com/developer/article/1698155
# content = requests.post(url, headers=headers, data=data, params=params).json()

# 由于上面这种方法可能会获取数据失败，可以采取字符串拼接这种方法
origin_url = "https://mp.weixin.qq.com/mp/getappmsgext?"
appmsgext_url = origin_url + "__biz={}&mid={}&sn={}&idx={}&appmsg_token={}&x5=1".format(your__biz, article_mid, article_sn, article_idx, yourappmsg_token)
content = requests.post(appmsgext_url, headers=headers, data=data).json()

# 提取其中的阅读数和点赞数
print(content["appmsgstat"]["read_num"], content["appmsgstat"]["like_num"], content["appmsgstat"]["old_like_num"])
