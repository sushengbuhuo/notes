# !/usr/bin/env python
# -*- coding:utf-8 -*-
# [url=home.php?mod=space&uid=238618]@Time[/url]  : 2021/8/6 17:49
# @Author: 冬酒暖阳
# [url=home.php?mod=space&uid=267492]@file[/url]  : weiboCountSpider.py
#https://www.52pojie.cn/thread-1682643-2-1.html pip install win10toast apscheduler playsound
import requests
import sys
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import json
from jsonpath import jsonpath
from win10toast import ToastNotifier
 
 
def get_weibo_count(always_send_notice=False):
    url = 'https://m.weibo.cn/api/container/getIndex'
 
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62 '
    }
    params = {
        'type': 'uid',
        'value': uid,
        'containerid': f'107603{uid}'
    }
    try:
        res = requests.get(
            url,
            headers=header,
            params=params
        )
        json_data = res.json()
        statuses_count = json_data['data']['cardlistInfo']['total']
        screen_name = jsonpath(json_data, f'$.data.cards[?(@.mblog.user.id=={uid})].mblog.user.screen_name')[0]
        print(screen_name, statuses_count)
 
        statuses_content_list = jsonpath(json_data, f'$.data.cards[?(@.mblog.user.id=={uid})].mblog.text')
    except:
        return
 
    data = {
        'uid': uid,
        'screen_name': screen_name,
        'statuses_count': statuses_count
    }
 
    json_dumps = json.dumps(
        data,
        ensure_ascii=False,
        indent=4
    )
    try:
        with open('weibo_count_data.json', 'r', encoding='UTF-8') as fp:
            try:
                file_content = fp.read()
            except:
                file_content = ''
    except:
        file_content = ''
    print(json_dumps)
    print(file_content)
    print(file_content != json_dumps)
    if always_send_notice or file_content != json_dumps:
        # print('发送微信通知')
        # 发送通知
        notice_text = f'微博信息变动\n用户名：{screen_name}\n当前微博数量：{statuses_count}'
        try:
            toaster.show_toast(
                notice_text,
                duration=0
            )
        except:
            pass
    try:
        with open('weibo_count_data.json', 'w', encoding='UTF-8') as fp:
            # 将新数据写入文件
            fp.write(json_dumps)
 
        with open('weibo_content_list.json', 'w', encoding='UTF-8') as fp:
            fp.write(
                json.dumps(
                    statuses_content_list,
                    ensure_ascii=False,
                    indent=4
                )
            )
    except:
        pass
 
 
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('缺失 uid 参数')
        exit(1)
    # 判断是否存在 weibo_count_data.json 数据文件，若不存在，自动创建
    if not os.path.exists('weibo_count_data.json'):
        with open('weibo_count_data.json', 'w', encoding='UTF-8'):
            pass
    # 获取传入的 uid 参数
    uid = sys.argv[1]
 
    toaster = ToastNotifier()
 
    get_weibo_count(always_send_notice=False)
 
    # 以下是定时任务不需要则可以将一下内容注释
    scheduler = BlockingScheduler()
    scheduler.add_job(get_weibo_count, 'cron', minute='*/5')
    try:
        print('启动定时任务')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.remove_all_jobs()
        scheduler.shutdown()
        print('启动失败，请重试')