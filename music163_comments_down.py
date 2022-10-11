from selenium import webdriver
from selenium.webdriver import ChromeOptions  # 反检测
from time import sleep
import time
import re
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options  # 无头浏览器所用模块
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt  # 绘制图像的模块
import jieba  # jieba分词https://www.52pojie.cn/thread-1694760-1-1.html
import re
import stylecloud
import collections
from PIL import Image
def comments():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=chrome_options)# webdriver.Chrome(service=Service("chromedriver.exe"),options=option)
    driver.get('https://music.163.com/#/song?id=25641703')
    # 执行自动化
    # selenium无法直接获取到嵌套页面里面的数据,主要是看iframe
    driver.switch_to.frame(0)  # switch_to.frame()  切换到嵌套网页
    driver.implicitly_wait(10)  # 让浏览器加载的时候, 等待渲染页面
    # 下拉页面, 直接下拉到页面的底部
    js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight'
    driver.execute_script(js)
    # .解析数据
    for i in tqdm(range(1, 10)):  # 爬取的时候可以搞一个tqdm模块，要不然这100多页太慢了
        btn = driver.find_element(By.CSS_SELECTOR, 'div.u-page .znxt')  # 定位翻页定位不到就完蛋
        btn.click()
        time.sleep(1)
        divs = driver.find_elements(By.CSS_SELECTOR, '.itm')  # 所有div  css语法: 定位到 html 数据/xpath/正则
        for div in divs:
            cnt = div.find_element(By.CSS_SELECTOR, '.cnt.f-brk').text
            id = cnt.split("：")[0]  # 以：作为分割
            cnt = cnt.split("：")[1]
            print(id, ":", cnt)
            with open('music163.txt', mode="a", encoding='utf-8') as f:
                f.write(cnt)
                f.write('\n')
    # print(resp.text)
    sleep(100)
    driver.quit()
# 改生成图片的地址,改txt文件路径，该打开的图片名称
comments()
def draw():
    path_txt = 'music163.txt'
    f = open(path_txt, 'r', encoding='utf-8').read()
    # 文本预处理 ：只提取出中文
    new_data = re.findall('[\u4e00-\u9fa5]+', f, re.S)
    new_data = "/".join(new_data)
    # 文本分词
    seg_list_exact = jieba.cut(new_data, cut_all=True)
    result_list = stop_words= []
    # with open('停用词库.txt', encoding='utf-8') as f:  # 可根据需要打开停用词库，然后加上不想显示的词语
    #     con = f.readlines()
    #     stop_words = set()
    #     for i in con:
    #         i = i.replace("\n", "")  # 去掉读取每一行数据的\n
    #         stop_words.add(i)
    for word in seg_list_exact:
        if word not in stop_words and len(word) > 1:
            result_list.append(word)
    # print(result_list)
    word_counts = collections.Counter(result_list)
    # 词频统计：获取前100最高频的词
    word_counts_top = word_counts.most_common(100)
    print(word_counts_top)
    # 绘制词云图
    stylecloud.gen_stylecloud(text=' '.join(result_list[:1000]),  # 提取500个词进行绘图
                              collocations=False,  # 是否包括两个单词的搭配（二字组）
                              font_path=r'C:\Windows\Fonts\msyh.ttc',  # 设置字体，参考位置为  C:\Windows\Fonts\ ，根据里面的字体编号来设置
                              size=2000,  # stylecloud 的大小
                              palette='cartocolors.qualitative.Bold_7',  # 调色板，调色网址： https://jiffyclub.github.io/palettable/
                              background_color='black',  # 背景颜色
                              icon_name='fas fa-plane',
                              # 形状的图标名称 蒙版网址：https://fontawesome.com/icons?d=gallery&p=2&c=chat,shopping,travel&m=free
                              gradient='horizontal',  # 梯度方向
                              max_words=2000,  # stylecloud 可包含的最大单词数
                              max_font_size=200,  # stylecloud 中的最大字号
                              stopwords=True,  # 布尔值，用于筛除常见禁用词
                              output_name='我有我天地.png')  # 输出图片
    # 打开图片展示
    img = Image.open('我有我天地.png')
    img.show()
# draw()