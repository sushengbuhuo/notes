import PySimpleGUI as sg
import arrow
import threading
import time,sys
import threading
import time
import httpx
import asyncio
import pandas as pd
df_table = pd.read_csv('公众号历史文章.csv',encoding='utf-8')
print(df_table.文章日期,df_table[df_table['文章日期'] == '2022-07-01'][['文章标题']],df_table['文章位置'].unique(),df_table[df_table['文章位置'] == 1][['留言数','文章标题']].sort_values(by='留言数',ascending=False))
print(df_table['文章位置'].unique().tolist(),df_table.groupby(by=['是否原创']).agg({"文章标题":count}))

url = 'https://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

#同步异步请求https://learnku.com/articles/54989
async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        print(resp.status_code)

if __name__ == '__main__':
    asyncio.run(main())
async def make_request(client):
    resp = await client.get(url, headers=headers)
    print(resp.status_code)

async def main2():
    async with httpx.AsyncClient() as client:
        start = time.time()
        tasks = [asyncio.create_task(make_request(client)) for _ in range(20)]
        await asyncio.gather(*tasks)
        end = time.time()
    print(f'发送100次请求，耗时：{end - start}')

asyncio.run(main2())
# https://learnku.com/articles/56743 多线程  python3 中主进程会等待子进程结束后再结束
a = 0
exact = []
not_exact = []
while a < 10:
    # 0 - 10 是否存在被整除的数
    if a % 2 == 0:
        exact.append(a)
    # 不能被整除的数
    else:
        not_exact.append(a)
    a = a + 1
else:
    print("这个循环我结束了！")
print("能被被整除的数：", exact)
print("不能被被整除的数：", not_exact)
localtime = time.asctime(time.localtime(time.time()))#将时间元组转换为字符串 https://learnku.com/articles/55951
print("本地时间为 :", localtime,time.asctime((2017,6,11,16,7,40,59,59,59)),time.ctime())#将时间戳转换为以本地时间为单位的字符串
print( time.gmtime())#将时间戳转换为时间元祖
print(time.localtime())#与 gmtime 功能类似，但是返回的时间变成了当地时间
print(time.mktime((2017,4,18,10,45,50,3,108,0)))#将时间元祖转化为时间戳，返回时间戳

print(time.strptime("2017-01-01 01:01:02", "%Y-%m-%d %H:%M:%S")) #根据格式规范将字符串解析为时间元组
# 格式化成2020-12-04 15:44:05形式
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),time.strftime("%Y-%m-%d %H:%M:%S", (2017, 1, 1, 1, 1, 1, 1, 13, 0)))
# 格式化成Fri Dec 04 15:44:05 2020形式
print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))
from datetime import date,datetime
print(date.today(),date.fromtimestamp(1560415206),datetime(2017,6,6).today(),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.fromtimestamp(1516083000).strftime("%Y-%m-%d %H:%M:%S"),datetime(2018,1,1).date())
import calendar
cal = calendar.month(2020, 1)
print("输出2020年1月份的日历:")
print(cal)

def run():
    """跑步"""
    for i in range(3):
        print("我要减肥!")
        time.sleep(1)
if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()#调用了 start 方法才会开启
    len = len(threading.enumerate())
    print('当前运行的线程数为：%d' % len)
sys.exit(-1)
# layout = [
#     [sg.Text('一句话概括Python')],
#     [sg.Input(key='-INPUT111-')],
#     [sg.Input(key='-INPUT222-')],
#     [sg.Button('确认'), sg.Button('取消')],
#     [sg.Text('输出：'), sg.Text(key='-OUTPUT-'), sg.Text(key='-OUTPUT2-')]
# ]
# window = sg.Window('PySimpleGUI Demo', layout)
# while True:
#     event, values = window.read()
#     print(event)
#     print(values)
#     if event in (None, '取消'):
#         break
#     else:
#         window['-OUTPUT-'].update(values['-INPUT111-'])
#         window['-OUTPUT2-'].update(values['-INPUT222-'])
# window.close()
# import qrcode
# import cv2
# img = qrcode.make('https://www.zhihu.com/')
# img.save('./zhihu.jpg')
# #pip install opencv-python

# d = cv2.QRCodeDetector()
# val, _, _ = d.detectAndDecode(cv2.imread("zhihu.jpg"))
# print("the secret is: ", val)
import datetime
now = datetime.datetime.now()

print(now,f'{now:%Y年%m月%d号%H点%M分%S秒}')
import math
pi = math.pi
print(f'{pi*100:.10e}')
number_10 = 1024
print(f'{number_10:b}')  # 2进制
print(f'{number_10:o}')  # 8进制
print(f'{number_10:x}')  # 16进制小写
print(f'{number_10:X}')  # 16进制大写
print(f'{number_10:c}')  # ASCII编码
print(f'{pi:.3f}')
print(f'{pi:.8f}')
a = [1, 2, 3, 4]
b = a
a = a + [5, 6, 7, 8]#a = a + [5,6,7,8] 会生成一个新列表, 并让 a 引用这个新列表, 同时保持 b 不变
# a += [5, 6, 7, 8] # a += [5,6,7,8] 实际上是使用的是 “extend” 函数, 所以 a 和 b 仍然指向已被修改的同一列表
print(a)
print(b)
import pandas as pd
# def max_age(s):    //函数：求最大年龄
#     today = datetime. datetime.today().year     //年份
#     age = today-s.dt.year    //求年龄
#     return age.max()
# employee = pd.read_csv("Employees.csv")
# employee['BIRTHDAY']=pd.to_datetime(employee['BIRTHDAY'])
# dept_agg =   employee.groupby('DEPT').agg({'SALARY':['count','mean'],'BIRTHDAY':max_age}) //按 DEPT 分组，根据 SALARY 计数和求均值，BIRTHDAY 使用 max_age 计算最大年龄
# dept_agg.columns   = ['NUM','AVG_SALARY','MAX_AGE'] //修改列名
# print(dept_agg.reset_index()) 
# years_salary =   employee.groupby(np.floor((employee['BIRTHDAY'].dt.year-1900)/10)).SALARY.mean() //计算衍生数组并按此数组分组，再计算平均工资
# dept_agg =   employee.groupby('DEPT',as_index=False).agg({'EID':'count','SALARY':'mean'}) //分组并对 EID 计数，对 SALARY 求平均
# print(dept_agg.rename(columns={'EID':'NUM','SALARY':'AVG_SALARY'})) // 重命名列名 
# dept_agg = employee.groupby('DEPT').SALARY.agg(['count','mean']).reset_index() //对 SALARY 计数并求平均
 # employee['AVG_SALARY'] =   employee.groupby('DEPT').SALARY.transform('mean') //按照 DEPT 分组并对 SALARY 求平均
 
df=
df['日期'] = pd.to_datetime(df['日期'])

# 提取2021年的数据
df = df[df['日期'].dt.year == 2021]
print(df)
# df = df[(df['号码']=='')&(df['日期'].dt.year == 2022)]
print(arrow.now(),arrow.now().timestamp,arrow.now().format('YYYY-MM-DD HH:mm:ss'),arrow.get(1651800761).format('YYYY-MM-DD HH:mm:ss'),arrow.now().datetime )

import time
import threading
import requests,pyperclip

def download(url, index):
    response = requests.get(url)
    print(f'{index:0>2d}:{url} downlaoded.')

urls = [f'https://learnku.com/' for i in range(1)]

now = time.time()

threads = []
for i, url in enumerate(urls):
    thread = threading.Thread(target=download, args=(url, i), daemon=True)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

seconds = time.time() - now

print(f'All URLs downloaded in {seconds:.2f} seconds')
def retryDo(img_url):
	res = requests.get(img_url, stream=True)
	count = 1
	while res.status_code != 200 and count <= 5:
		res = requests.get(img_url, stream=True)
		print(f'Retry: {count} {img_url}')
		count += 1
from re import split
from pandas import DataFrame

"""
with open(csv_file, 'rt', encoding='utf-8') as f:
    data = f.read()
"""

data = """
column1,column2,column3,column4
11,12,13,{“name”:’name1’,”data”:’data1’}
21,22,23,{“name”:’name2’,”data”:’data2’}
31,32,33,{“name”:’name3’,”data”:’data3’}
41,42,43,{“name”:’name4’,”data”:’data4’}
"""

lines = list(map(lambda line: split(',\s*(?![^{}]*\})', line), data.strip().split('\n')))

df = DataFrame(lines)
print(df,lines)
import openpyxl
from xpinyin import Pinyin
p.get_pinyin("上海", tone_marks='marks')
# workbook = openpyxl.load_workbook('demo.xlsx')

# sheet = workbook['Sheet1']
# sheet["C9"] = "NBbfdgbfdbfdb"

# workbook.save('output.xlsx')
def setCopyText(text):#写入剪切板
    pyperclip.copy(text)
# df = pandas.read_csv('addresses.csv')
# result = df.values.tolist()
import pyautogui
import easyocr
#判断屏幕是否有1234
# file = 'screenshot.jpg'
# pyautogui.screenshot().save(file)

# reader = easyocr.Reader(['ch_sim','en'])
# result = reader.readtext(file, detail = 0)
# print(result)

# if any(map(lambda x:'1234' in x, result)):
#     print('Yes, "1234" found !')
# else:
#     print('No, "1234" not found !')
from win32gui import *  # 操作windows窗口 pip install Pillow win32gui
from PIL import ImageGrab  # 操作图像
import win32con  # 系统操作 https://www.cnblogs.com/lwsbc/p/16271504.html
def get_window_title(window, nouse):
    '''
    获取窗口标题函数
    :param window: 窗口对象
    :param nouse:
    :return:
    '''

    if IsWindow(window) and IsWindowEnabled(window) and IsWindowVisible(window):

        names.add(GetWindowText(window))

EnumWindows(get_window_title, 0)

list_ = [name for name in names if name]

for n in list_:

    print('活动窗口: ', n)
name = input('请输入需要截图的活动窗口名称: \n')

window = FindWindow(0, name)  # 根据窗口名称获取窗口对象

ShowWindow(window, win32con.SW_MAXIMIZE)  # 将该窗口最大化

x_start, y_start, x_end, y_end = GetWindowRect(window)

# 坐标信息
box = (x_start, y_start, x_end, y_end)
image = ImageGrab.grab(box)
image.show()  # 图片展示，如果截完图需要展示则放开此项
image.save('target.png')

from docx import Document  # 文档处理对象 pip install python-docx

from docx.shared import RGBColor, Pt, Cm  # 文本样式处理

import os  # 应用/文件处理

import glob  # 文件处理
source_file = 'source'  # 来源文件路径

target_file = 'target'  # 目标文件路径
for current_file in glob.glob(source_file + '/*.docx'):  # 遍历word文档文件

    word_obj = Document(current_file)  # 初始化word对象

    for para in word_obj.paragraphs:  # 遍历当前文档段落

        for run in para.runs:  # 遍历当前段落的文本块

            if 'Python' in run.text: # 判断当前文本块是否包含Python字符串

                run.font.underline = True  # 加上下划线

                run.font.color.rgb = RGBColor(255, 0, 0)  # 设置字体颜色为红色

    word_obj.save(target_file + '/' + os.path.basename(current_file))
#pip install PyPDF2  pyttsx3  -i https://pypi.tuna.tsinghua.edu.cn/simple/
def read_pdf_to_txt(pdf_file):
    '''
    读取PDF文件返回text文本
    :param pdf_file: PDF文件路径
    :return:
    '''
    reader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
    texts = ''
    for page_num in range(reader.numPages):
        text = reader.getPage(page_num).extractText()
        text = text.strip().replace('\n', ' ')
        texts = texts + text
    return texts


def to_video(text):
    '''
    文本转换为音频函数
    :param text: 文本字符串
    :return:
    '''
    sp = pyttsx3.init()
    sp.save_to_file(text, './vi.mp3')
    sp.runAndWait()
    sp.stop()

# 初始化语言转换引擎
tsx = pyttsx3.init()

# 获取所有的声音模式
voice_model = tsx.getProperty('voices')

# 遍历所有的声音模式
for voice in voice_model:
    print ('编号 = {} \n名称 = {} \n'.format(voice.id, voice.name))
tsx.setProperty('voice', voice_model[0].id)
tsx.say('大家好')
tsx.runAndWait()
#pip install exifread  地理位置转换网址：http://www.giscalculator.com/enter_regeocode_input/
def read_image():
    '''
    经纬度信息读取函数
    :return:
    '''
    image = open('c.jpg', 'rb')  # 打开照片文件
    messages = exifread.process_file(image)  # 获取照片信息
    '''遍历提取照片信息'''
    for message in messages:
        print('照片信息：', message)
        if message == "GPS GPSLongitude":
            print("经度 =", messages[message], messages['GPS GPSLatitudeRef'])
        elif message == "GPS GPSLatitude":
            print("纬度 =", messages[message], messages['GPS GPSLongitudeRef'])
import os  # python标准库，不需要安装，用于系统文件操作相关
import cv2  # python非标准库，pip install opencv-python 多媒体处理
from PIL import Image  # python非标准库，pip install pillow，图像处理
import moviepy.editor as mov  # python非标准库，pip install moviepy，多媒体编辑
def image_to_video(image_path, media_path):
    '''
    图片合成视频函数
    :param image_path: 图片路径
    :param media_path: 合成视频保存路径
    :return:
    '''
    # 获取图片路径下面的所有图片名称
    image_names = os.listdir(image_path)
    # 对提取到的图片名称进行排序
    image_names.sort(key=lambda n: int(n[:-4]))
    # 设置写入格式
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    # 设置每秒帧数
    fps = 2  # 由于图片数目较少，这里设置的帧数比较低
    # 读取第一个图片获取大小尺寸，因为需要转换成视频的图片大小尺寸是一样的
    image = Image.open(image_path + image_names[0])
    # 初始化媒体写入对象
    media_writer = cv2.VideoWriter(media_path, fourcc, fps, image.size)
    # 遍历图片，将每张图片加入视频当中
    for image_name in image_names:
        im = cv2.imread(os.path.join(image_path, image_name))
        media_writer.write(im)
        print(image_name, '合并完成！')
    # 释放媒体写入对象
    media_writer.release()
    print('写入完成！')
def set_music():
    '''
    合成视频设置背景音乐函数
    :return:
    '''
    print('开始添加背景音乐！')
    # 初始化视频文件对象
    clip = mov.VideoFileClip('media.mp4')
    # 从某个视频中提取一段背景音乐
    audio = mov.AudioFileClip('source.mp4').subclip(0, 83)
    # 将背景音乐写入.mp3文件
    audio.write_audiofile('background.mp3')
    # 向合成好的无声视频中加背景音乐
    clip = clip.set_audio(audio)
    # 保存视频
    clip.write_videofile('media.mp4')
    print('！')

# image_to_video('./images/', './media.mp4')
# set_music()
from collections import deque  # 将队列对象导入到代码块中
queue_ = deque([1,2,3])  # 初始化队列对象
queue_.append(20)  # 向队列中添加元素20
queue_.popleft()  # 从队列的头部取出数据元素
# pip install emoji
res = emoji.emojize(' Python！ :thumbs_up:')
res = emoji.emojize('我喜欢！ :red_heart:')
# emoji字符串列表地址：https://www.webfx.com/tools/emoji-cheat-sheet/
# pip install jmespath
json_data1 = {"name": "Python", "age": "10年"}

res = jmespath.search("name", json_data1)
json_data2 = {"names": {"name": "Python  ", "age": "5年"}}

res = jmespath.search("names.name", json_data2)
json_data3 = ['Python  ', 'Sir.wang']

res = jp.search("[0]", json_data3)
json_data4 = {
    "key1": {"key1_1": "value1_1"},
    "key2": {"key2_1": ["a", "b", "c"]}
}

res = jp.search('key2.key2_1[0]', json_data4)
res = jp.search('*.key2_1',json_data6)
from win10toast import ToastNotifier  # 导入系统通知对象pip install win10toast
import time  # 系统时间模块
import datetime
from threading import Timer  # 定时器
notify = ToastNotifier()  # 初始化系统通知对象
notify_head = '主人，来通知啦！'
notify_min = 1.0
notify_text = '已经过了' + str(int(notify_min)) + '分钟了，该喝水了！'

notify_sen = notify_min * 1
def show_toast():
    print('当前时间:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    notify.show_toast(f"{notify_head}", f"{notify_text}", duration=5, threaded=True, icon_path='水杯.ico')
    while notify.notification_active():
        time.sleep(0.005)
    timer = Timer(notify_sen, show_toast)
    timer.start()
from tabulate import tabulate
list_ = [['张三', '90班', '98'], ['张三', '90班', '98'], ['张三', '90班', '98'], ['张三', '90班', '98'], ['张三', '90班', '98']]

print(tabulate(list_))
print(tabulate(dict_,headers='keys'))

diretory = input('请输入需要整理的文件目录: \n')  # 去重的文件夹路径
logger = logging.getLogger('系统文件去重')
logging.basicConfig(format='%(asctime)s %(levelname)-8s: %(message)s')
logger.setLevel(logging.DEBUG)
import os  # 应用文件操作
import hashlib  # 文件对比操作
import logging  # 日志函数操作
import sys  # 系统应用操作
if os.path.isdir(diretory):
    logger.info('当前目录[' + diretory + ']校验成功！')
    md5s = []
    for file_path, dir_names, file_names in os.walk(r'' + diretory):
        for file_name in file_names:
            try:
                file_name_path = os.path.join(file_path, file_name)
                logger.info('当前比对路径: '+ file_name_path)
                md5 = hashlib.md5()
                file = open(file_name_path, "rb")
                md5.update(file.read())
                file.close()
                md5_value = md5.hexdigest()
                if md5_value in md5s:
                    os.remove(file_name_path)
                    logger.info('[' + file_name_path + ']出现重复已经移除！')
                else:
                    md5s.append(md5_value)
            except:
                logger.error('[' + file_name_path + ']对比发生异常，执行下一个！')

else:
    logger.error('输入的文件夹或者目录不存在！')
# PDF读取第三方库
import pdfplumber

# DataFrame 数据结果处理
import pandas as pd
# 初始化DataFrame数据对象、用于DataFrame数据保存
data_frame = pd.DataFrame()
# pdf 文件路径
pdf_file = 'data.pdf'

# 读取pdf数据
pdf_data = pdfplumber.open(pdf_file)

# 遍历PDF数据
for page in pdf_data.pages:
    # 每一页的Tbale表格数据
    table = page.extract_table()
    # 将每一页的数据写入一个DataFrame对象
    data_frame_page = pd.DataFrame(table[1:], columns=table[0])
    # 合并每一页的表格数据
    data_frame = pd.concat([data_frame_page, data_frame], ignore_index=True)

# 简单的数据清洗、删除其中列值全部为Nan的数据列
data_frame.dropna(axis=1, how='all', inplace=True)
# excel 文件路径
excel_path = 'data.pdf'

# 自定义列名
data_frame.columns = ['姓名', '年龄', '身份证号', '绩效']

# DataFrame数据保存到Excel数据表中
data_frame.to_excel(excel_writer=excel_path, index=False, encoding='utf-8')
 
# word文档处理库
from docxtpl import DocxTemplate
# 读取数据，并返回DataFrame数据形式
data_frame = pd.read_excel('pyrhon.xlsx')

# 按照章、节、序号进行排序
data_frame.sort_values(["章","节","序号"],inplace = True)
# 匹配word模板
tpl_word = DocxTemplate("python_model.docx")

# 按照模板进行转换、转换后进行排序
tpl_word.render({'ps':data_frame[["章","节","序号","题目"]].values.tolist()})

# 将结果保存到word文档
tpl_word.save("python_qes.docx")
# pip install coverage
# coverage命令执行代码统计

# coverage run hello_world.py
# 控制台输出报告

# coverage report
# 生成html报告

# coverage html
# # word文档处理器
from win32com.client import Dispatch

# 文件目录遍历器
from os import walk
def wordToPdf(word_file):
    '''
    将word文件转换成pdf文件
    :param word_file: word文件
    :return:
    '''
    # 获取word格式处理对象
    word = Dispatch('Word.Application')
    # 以Doc对象打开文件
    doc_ = word.Documents.Open(word_file)
    # 另存为pdf文件
    doc_.SaveAs(word_file.replace(".docx", ".pdf"), FileFormat=17)
    # 关闭doc对象
    doc_.Close()
    # 退出word对象
    word.Quit()
def run(doc_path):
    '''
    主要逻辑处理、支持批量多文件处理
    :param word_file: word文件
    :return:
    '''
    # 遍历文件夹下面的所有文件
    for root, dirs, filenames in walk(doc_path):
        # 遍历当前文件名称、并校验是否是word文档
        for file in filenames:
            if file.endswith(".doc") or file.endswith(".docx"):
                # 如果当前文件是word文档则调用word转换函数
                wordToPdf(str(root + "\\" + file))
# pip install auto-py-to-exe
# 打开PDF文件、得到PDF数据文件对象
pdf_obj = pdfplumber.open('data.pdf')

# 这里我们以获取第一页的PDF数据为例
page_1 = pdf_obj.pages[0]

# 从得到的第一页数据中提取表格数据
data_table = page_1.extract_table()

# 将提取到的数据表格转换为DataFrame数据对象
data_frame = pd.DataFrame(data_table)

# 打印查看DataFrame数据
print(data_frame)
writer = pd.ExcelWriter('data.xlsx') # 设置文档路径

data_frame.to_excel(writer, index=None, startrow=1, encoding='utf-8',sheet_name='数据统计')  # 设置Excel对象

ws = writer.sheets['数据统计']  # 写入工作表名称

ws.write_string(0, 0, '标题')  # 添加标题

writer.save()  # 保存
pip install pdf2docx  # 安装 pdf2docx

# 导入文件转换对象Converter
from pdf2docx import Converter
# 初始化PDF转换对象
converter = Converter(pdf_file_path)
# 连续页面进行转换
converter.convert(docx_file_path, start=0, end=None)

# 指定页面进行转换
# converter.convert(docx_file_path, pages=[0,2,4,6,8,10])

# 关闭转换对象
converter.close()
pip install dtale
>>> data_frame = pd.read_excel('data.xlsx')
>>> dtale.show(data_frame)
 print(datetime.now().timestamp())  # 获取时间戳

  print(datetime.fromtimestamp(1627791637.223392))  # 将时间戳转换为日期时间格式
print(datetime.now().strftime("%Y%m%d"))
date_time = datetime.strptime('2021-8-1  08:23:56', '%Y-%m-%d  %H:%M:%S')  # 格式化日期时间
 date_time = datetime.timedelta(hours=5,minutes=2,seconds=20)  # 定义时间差值print(date_time_now - date_time)  # 5小时2分钟20秒以前
 
