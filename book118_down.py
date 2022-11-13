# !/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import json
import os
import shutil
import sys
import time
import requests
import img2pdf
from PIL import Image

from alive_progress import alive_bar
from requests.exceptions import SSLError
 
png_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Referer': 'https://max.book118.com/',
}
 
 
def down_pngs(pageIndex):
    print(pngs[pageIndex])
    down_url = 'https://view-cache.book118.com' + pngs[pageIndex]
    print(down_url)
    res = requests.get(url=down_url)
    try:
        png = res.content
        with open(os.path.join(temp_dir, str(pageIndex) + '.jpeg'), 'wb') as f:
            f.write(png)
    except:
        return
 
#https://www.52pojie.cn/thread-1705825-1-1.html
while True:
    url = input('请输入原创力文库链接:')
    url = url.split('?')[0]
    # print('下载地址：', url)
    temp_dir = url.split('/')[-1]
 
    # 删除老的临时文件夹并新建临时文件夹
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)
 
    print('开始下载 ', end='')
 
    try:
        response = requests.get(url=url)
    except(SSLError):
        print("\n\033[31m不要使用代理软件-------\033[0m")
        sys.exit(0)
 
    page = response.text
 
    print('成功. \n开始解析 ', end='')
 
    title = re.search('title: (.*),', page).group(1).replace("'", "")
    view_token = re.search('view_token: (.*)\'', page).group(1).replace("'", "")
    filetype = re.search('format: (.*)\'', page).group(1).replace("'", "")
    senddate = re.search('senddate: (.*),', page).group(1).replace("'", "")
    aid = re.search(' aid: (.*), //解密后的id', page).group(1)
    actual_page = int(re.search('actual_page: (.*),', page).group(1))  # 真实页数
    preview_page = int(re.search('preview_page: (.*),', page).group(1))  # 可预览页数
 
    if actual_page > preview_page:
        print("\n\033[31m该文档为限制文档，无法下载全部内容\033[0m\n")
 
    output = title  # 输出文件（夹）
    print('解析成功. ')
    print('文档标题: ', title)
    # 接口每次会返回6个下载page地址
    list_pn = list(range(1, preview_page + 1, 6))
 
    # print(pngs)
    if filetype == 'pdf':
        pngs = {}
        print('解析到pdf文档, 准备开始解析下载..', end='')
        print('解析成功.\n正在获取pngs下载地址...')
        print('受接口限制，2s访问一次，请耐心等待所有接口信息返回')
 
        with alive_bar(len(list_pn), title='ing...') as bar:
            for pn in list_pn:
                bar()
                down_page_url = 'https://openapi.book118.com/getPreview.html?project_id=1&aid={}&view_token={}&page={}&_={}'.format(
                    aid, view_token, pn, str(int(time.time())))
                jsonpReturn = requests.get(url=down_page_url)
                page = re.search('jsonpReturn\((.*)\)', jsonpReturn.text).group(1)
                data_temp = json.loads(page)['data']
                # print(data_temp)
                pngs.update({x: data_temp[x] for x in data_temp})  # 这里有个bug，若返回值的url为空时，这里不会报错，但会造成下载png时异常，暂时没有考虑处理
                if pn != list_pn[-1]:
                    time.sleep(2)
 
        print('\n开始下载 jpg(s)...')
        pagenums = list(range(1, len(pngs) + 1))
 
        with alive_bar(len(pagenums), title='ing...') as bar:
            for i in range(len(pagenums)):
                bar()
                down_url = "https:" + pngs[str(i + 1)]
                request = requests.get(url=down_url, headers=png_headers)
                try:
                    page = request.content
                    with open(os.path.join(temp_dir, str(pagenums[i]) + '.jpeg'), 'wb') as f:
                        f.write(page)
                except:
                    continue
 
        print('\n开始合并图片成PDF...', end='')
 
        file_imgs = [os.path.join(temp_dir, str(i) + '.jpeg') for i in pagenums]
        # 不用以下代码会使img2pdf报错
        for img_path in file_imgs:
            with open(img_path, 'rb') as data:
                img = Image.open(data)
                # 将PNG中RGBA属性变为RGB，即可删掉alpha透明度通道
                img.convert('RGB').save(img_path)
 
        with open(output + '.pdf', 'wb') as f:
            f.write(img2pdf.convert(file_imgs))
 
        shutil.rmtree(temp_dir)
 
        print('下载成功.')
        print('保存到 ' + output + '.pdf')
    elif filetype in ['docx', 'doc']:
        pngs = {}
        print('解析到{}文档, 准备开始解析下载..'.format(filetype), end='')
        print('解析成功.\n正在获取pngs下载地址...')
        print('受接口限制，2s访问一次')
        with alive_bar(len(list_pn), title='ing...') as bar:
            for pn in list_pn:
 
                down_page_url = 'https://openapi.book118.com/getPreview.html?&project_id=1&aid={}&t={}&view_token={}&page={}&_={}'.format(
                    aid, senddate, view_token, pn, str(int(time.time())))
                jsonpReturn = requests.get(url=down_page_url)
 
                page = re.search('jsonpReturn\((.*)\)', jsonpReturn.text).group(1)
                data_temp = json.loads(page)['data']
                # print(data_temp)
                bar()
                pngs.update({x: data_temp[x] for x in data_temp})
                if pn != list_pn[-1]:
                    time.sleep(2)
 
        print('\n开始下载 jpg(s)...')
        pagenums = list(range(1, len(pngs) + 1))
 
        with alive_bar(len(pagenums), title='ing...') as bar:
            for i in range(len(pagenums)):
                down_url = "https:" + pngs[str(i + 1)]
                request = requests.get(url=down_url, headers=png_headers)
                bar()
                try:
                    page = request.content
                    with open(os.path.join(temp_dir, str(pagenums[i]) + '.jpeg'), 'wb') as f:
                        f.write(page)
                except:
                    continue
 
        print('\n开始合并图片成PDF...', end='')
 
        file_imgs = [os.path.join(temp_dir, str(i) + '.jpeg') for i in pagenums]
        for img_path in file_imgs:
            with open(img_path, 'rb') as data:
                img = Image.open(data)
                # 将PNG中RGBA属性变为RGB，即可删掉alpha透明度通道
                img.convert('RGB').save(img_path)
 
        with open(output + '.pdf', 'wb') as f:
            f.write(img2pdf.convert(file_imgs))
 
        shutil.rmtree(temp_dir)
 
        print('下载成功.')
        print('保存到 ' + output + '.pdf')
 
    else:
        print('不支持的参数.文件类型:', filetype)
 
    temp_ = os.path.realpath(sys.argv[0])
    os.startfile(os.path.dirname(temp_))
    print("执行完成\n")