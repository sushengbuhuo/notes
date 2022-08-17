import requests
from bs4 import BeautifulSoup
import re
import time
 
myHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
}
myCookies = {
    "Cookie": 'xxxxx'
 
}
url = "https://tieba.baidu.com/sign/add"#https://www.52pojie.cn/thread-1670811-1-1.html
 
def getTblikes():
    i = 0
    url = "https://tieba.baidu.com/f/like/mylike"
    contain1 = BeautifulSoup(requests.get(url=url, cookies=myCookies, headers=myHeader).text, "html.parser")
 
    if contain1.find("div", attrs={"class": "pagination"}):
        pageNum = len(contain1.find("div", attrs={"class": "pagination"}).findAll("a"))
    else:
        pageNum = 2
    a = 1
    while a < pageNum:
        urlLike = f"https://tieba.baidu.com/f/like/mylike?&pn={a}"
        contain = BeautifulSoup(requests.get(url=urlLike, cookies=myCookies, headers=myHeader).text, "html.parser")
        first = contain.find_all("tr")
        for result in first[1:]:
            second = result.find_next("td")
            name = second.find_next("a")['title']
            singUp(name)
            time.sleep(5)
            i += 1
        a += 1
    print(f"签到完毕！总共签到完成{i}个贴吧")
 
def getTbs(name):
    urls = f"https://tieba.baidu.com/f?kw={name}"
    contain = BeautifulSoup(requests.get(urls, headers=myHeader, cookies=myCookies).text, "html.parser")
    first = contain.find_all("script")
    try:
        second = re.findall('\'tbs\': "(.*?)" ', str(first[1]))[0]
        return second
    finally:
        return re.findall('\'tbs\': "(.*?)" ', str(first[1]))
 
def singUp(tb):
    myDate = {
        "ie": "utf-8",
        "kw": tb,
        "tbs": getTbs(tb)
    }
    resp = requests.post(url, data=myDate, headers=myHeader, cookies=myCookies)
    result = re.findall('"error":"(.*?)"', str(resp.text))[0]
    if result.encode().decode("unicode_escape") == "":
        print(f"在{tb}签到成功了！！")
    else:
        print(f"在{tb}签到失败了，返回信息: " + result.encode().decode("unicode_escape"))
 
getTblikes()