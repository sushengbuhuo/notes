# -*- coding:utf-8 -*-

import re
import requests
import os
import urllib.request
import ssl

from urllib.parse import urlsplit
from os.path import basename

# 全局禁   用证书验证
ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    'Accept-Encoding': 'gzip, deflate'
}

# 下载出错的列表
failed_image_list = []


def mkdir(path):
    if not os.path.exists(path):
        print('新建文件夹：', path)
        os.makedirs(path)
        return True
    else:
        print(u"图片存放于：", os.getcwd() + os.sep + path)
        return False


def download_pic2(img_lists, dir_name):
    print("一共有{num}张照片".format(num=len(img_lists)))

    # 标记下载进度
    index = 1

    for image_url in img_lists:
        file_name = dir_name + os.sep + basename(urlsplit(image_url)[2])

        # 已经下载的文件跳过
        if os.path.exists(file_name):
            print("文件{file_name}已存在。".format(file_name=file_name))
            index += 1
            continue

        # 重试次数
        retry_time = 3
        auto_download(image_url, file_name, retry_time)

        print("下载{pic_name}完成！({index}/{sum})".format(pic_name=file_name, index=index, sum=len(img_lists)))
        index += 1

    # 打印下载出错的文件
    if len(failed_image_list):
        print("以下文件下载失败：")
        for failed_image_url in failed_image_list:
            print(failed_image_url)


def auto_download(image_url, file_name, retry_time):
    # 递归下载，直到文件下载成功
    try:
        # 判断剩余下载次数是否小于等于0，如果是，就跳过下载
        if retry_time <= 0:
            print("下载失败，请检查{image_url}链接是否正确（必要时可以手动下载）")
            failed_image_list.append(image_url)
            return

        # 下载文件
        urllib.request.urlretrieve(image_url, file_name)

    except urllib.request.ContentTooShortError:
        print("文件下载不完整，尝试重新下载，剩余尝试次数{retry_time}".format(retry_time=retry_time))
        retry_time -= 1
        auto_download(image_url, file_name, retry_time)

    except urllib.request.URLError as e:
        print("网络连接出错，尝试重新下载，剩余尝试次数{retry_time}".format(retry_time=retry_time))
        retry_time -= 1
        auto_download(image_url, file_name, retry_time)


def download_pic(img_lists, dir_name):
    print("一共有{num}张照片".format(num=len(img_lists)))
    for image_url in img_lists:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image = response.content
        else:
            continue

        file_name = dir_name + os.sep + basename(urlsplit(image_url)[2])

        try:
            with open(file_name, "wb") as picture:
                picture.write(image)
        except IOError:
            print("IO Error\n")
            continue
        finally:
            picture.close()

        print("下载{pic_name}完成！".format(pic_name=file_name))


def get_image_url(qid, headers, path):
    # 利用正则表达式把源代码中的图片地址过滤出来
    # reg = r'data-actualsrc="(.*?)">'
    tmp_url = "https://www.zhihu.com/node/QuestionAnswerListV2"
    offset = 0
    image_urls = []

    session = requests.Session()

    # 答案数
    answer_num = 0

    while True:
        postdata = {'method': 'next',
                    'params': '{"url_token":' + str(qid) + ',"pagesize": "10","offset":' + str(offset) + "}"}
        page = session.post(tmp_url, headers=headers, data=postdata)
        ret = eval(page.text)
        answers = ret['msg']

        offset += 10

        if not answers:
            print("图片URL获取完毕, 页数: ", (offset - 10) / 10)
            return image_urls

        answer_num += len(answers)

        # reg = r'https://pic\d.zhimg.com/[a-fA-F0-9]{5,32}_\w+.jpg'
        imgreg = re.compile('data-original="(.*?)"', re.S)

        for answer in answers:
            tmp_list = []
            url_items = re.findall(imgreg, answer)

            for item in url_items:  # 这里去掉得到的图片URL中的转义字符'\\'
                image_url = item.replace("\\", "")
                tmp_list.append(image_url)

            # 清理掉头像和去重 获取data-original的内容
            tmp_list = list(set(tmp_list))  # 去重
            for item in tmp_list:
                if item.endswith('r.jpg'):
                    print(item)
                    write_image_url_to_file(path, item)
                    image_urls.append(item)

        print('offset: %d, num : %d' % (offset, len(image_urls)))

    # 打印答案数
    print(u"答案数：%d" % (len(answers)))


def write_image_url_to_file(file_name, image_url):
    file_full_name = file_name + '.txt'

    f = open(file_full_name, 'a')
    f.write(image_url + '\n')
    f.close()


def read_image_url_from_file(file_name):
    file_full_name = file_name + '.txt'

    # 文件下载链接列表
    image_url_list = []

    # 判断文件是否存在
    if not os.path.exists(file_full_name):
        return image_url_list

    with open(file_full_name, 'r') as f:
        for line in f:
            line = line.replace("\n", "")
            image_url_list.append(line)

    print("从文件中读取下载链接完毕，总共有{num}个文件".format(num=len(image_url_list)))
    return image_url_list


if __name__ == '__main__':
    title = '刘亦菲有什么出圈神图'
    question_id = 374798860
    zhihu_url = "https://www.zhihu.com/question/{qid}".format(qid=question_id)
    path = str(question_id) + '_' + title
    mkdir(path)  # 创建本地文件夹

    # 优先从文件中读取下载列表
    img_list = read_image_url_from_file(path)
    if not len(img_list):
        # 获取图片的地址列表
        img_list = get_image_url(question_id, headers, path)

    # 下载文件
    download_pic2(img_list, path)
