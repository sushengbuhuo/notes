from DrissionPage import Chromium
from DrissionPage import ChromiumOptions
from DrissionPage import SessionPage
path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # 请改为你电脑内Chrome可执行文件路径
# ChromiumOptions().set_browser_path(path).save() dp -p "D:\Chrome\chrome.exe"
co=ChromiumOptions().set_browser_path(path)
tab = Chromium(co).latest_tab
# tab.get('https://DrissionPage.cn')
# tab.get('https://gitee.com/login')
# 定位到账号文本框，获取文本框元素
# ele = tab.ele('#user_login')
# 输入对文本框输入账号
# ele.input('账号')
# 定位到密码文本框并输入密码
# tab.ele('#user_password').input('密码')
# 点击登录按钮
# tab.ele('@value=登 录').click()
# 创建页面对象 收发数据包的页面类SessionPage
page = SessionPage()
# tab.get('https://xueqiu.com/u/1505944393')
# 爬取3页
for i in range(1, 1):
    # 访问某一页的网页
    page.get(f'https://gitee.com/explore/all?page={i}')
    # 获取所有开源库<a>元素列表
    links = page.eles('.title project-namespace-path')
    # 遍历所有<a>元素
    for link in links:
        # 打印链接信息
        print(link.text, link.link)
# tab.get('https://gitee.com/explore/all')
# # 切换到收发数据包模式 从当前控制浏览器的模式切换到收发数据包模式
# tab.change_mode()
# # 获取所有行元素
# items = tab.ele('.ui relaxed divided items explore-repo__list').eles('.item')
# # 遍历获取到的元素
# for item in items:
#     # 打印元素文本
#     print(item('t:h3').text)
#     print(item('.project-desc mb-1').text)
#     print()
tab.get('https://www.baidu.com')  
# 获取文本框元素对象
ele = tab.ele('#kw')
# 向文本框元素对象输入文本
ele.input('DrissionPage')  
# 点击按钮，上两行的代码可以缩写成这样
# tab('#su').click() 
tab.ele('#su').click() 
# 获取所有<h3>元素
links = tab.eles('tag:h3')  
# 遍历并打印结果
for link in links:  
    print(link.text)
