from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
 
 
def info():    #获取信息https://www.52pojie.cn/thread-1722095-1-1.html
    wares = wd.find_elements(By.CLASS_NAME,'sku-name')
    print(wares)
    print(len(wares))
 
    for ware in wares:
        print(ware.text)
 
    prices = wd.find_elements(By.CSS_SELECTOR,'.price.overflow')
    print(prices)
    print(len(prices))
 
    for price in prices:
        print(price.text)
 
def roll():   #滚动
    for i in range(10):
        wd.execute_script(f'document.documentElement.scrollTop={(i+1)*1000}')
        time.sleep(2)
 
 
chromedriver = 'chromedriver.exe'  # 浏览器内核文件位置
chome_options = webdriver.ChromeOptions()
wd = webdriver.Chrome(chromedriver, chrome_options=chome_options)
wd.delete_all_cookies()  # 删除cookies
wd.maximize_window()  # 将浏览器最大化
wd.implicitly_wait(120)  # 最大等待120秒以防网速问题导致页面无法加载
time.sleep(2)  #个人习惯停2秒
 
 
"""保存成功后就可以注释掉这块代码了"""
"""
log_url = 'https://www.cneptp.com'
wd.get(log_url)
time.sleep(80)     # 进行登陆
dictCookies = wd.get_cookies()    # 获取list的cookies
jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
 
with open('cookies.txt', 'w') as f:
    f.write(jsonCookies)
print('cookies保存成功！')
"""
"""保存成功后就可以注释掉这块代码了"""
 
 
"""从本地读取cookies并刷新页面,成为已登录状态"""
 
wd.get('https://www.cneptp.com')   #还是一样，访问官网
time.sleep(5)   #停5秒，代码里最好多加点停，这样才像个人，谁手速能那么快，多加停可以防反爬
 
with open('cookies.txt', 'r', encoding='utf8') as f:      #打开刚才保存的cookies文件
    listCookies = json.loads(f.read())     #读取保存的cookies内容
# 往浏览器里添加cookies
for cookie in listCookies:       #循环
    cookie_dict = {
        'domain': '.cneptp.com',
        'name': cookie.get('name'),
        'value': cookie.get('value'),
        "expires": '',
        'path': '/',
        'httpOnly': False,
        'HostOnly': False,
        'Secure': False
    }
    wd.add_cookie(cookie_dict)     #添加进去
wd.refresh()  # 刷新网页,cookies才成功
 
# print("登录成功！")
time.sleep(3)
 
url = "https://www.cneptp.com/AvgPriceSearchPage?type=1&cat=8&st=0&pageN=1"   #要爬取的原材料价格页面
wd.get(url)  #打开页面
 
#突破蒙版引导
wd.find_element(By.CLASS_NAME,'mc__wrapper_5').click() #找到蒙版引导需要点击的位置
time.sleep(5)
 
#查找一共有多少页
nums = wd.find_elements(By.CSS_SELECTOR,'.el-pager')[0].text
# print('查找num')
# print(nums)
num = int(nums[4:])
# print(num)
 
#构建循环来依次爬取
for i in range(1,num+1):
    while i == 1:
        roll()
        info()
    time.sleep(15)  #停15秒
 
    wd.find_elements(By.CSS_SELECTOR,'.el-icon.el-icon-arrow-right').click()  #点击下一页
    roll()
    info()
    time.sleep(15)