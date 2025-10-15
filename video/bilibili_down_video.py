import requests
import time
import json,html
import random,re,os,csv
from bs4 import BeautifulSoup
import subprocess
requests.packages.urllib3.disable_warnings()
sname=input('请输入txt文件名：');sname='video'
with open(f'{sname}.txt', encoding='utf-8') as f:
    contents = f.read()
urls=contents.split('\n')
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ').replace('"', '“')
with open(f'视频数据.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('日期'+','+'标题' + ','+'链接'+ ','+'封面'+ ','+'播放数'+','+'点赞数'+','+'转发数'+','+'评论数'+ ','+'投币数'+ ','+'收藏数'+ ','+'时长'+'\n')
for url in urls:
    # try:
    #     result = subprocess.run(['lux', url], capture_output=True, text=True, check=True)
    #     print("脚本执行成功，输出如下:",url)
    #     print(result.stdout)
    # except subprocess.CalledProcessError as e:
    #     print(f"脚本执行失败，错误信息: {e.stderr}")
    try:
        bv_id = re.search(r"(BV[\w]+)/.*", url).group(1)
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
        response = requests.get(api_url, headers=headers)
        data = response.json()
        time.sleep(2)
        if data.get("code") == 0:
            info = data["data"]
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info['ctime']))
            title = info["title"]  # 标题
            play_count = info["stat"]["view"]  # 播放量
            like_count = info["stat"]["like"]  # 点赞数
            share_count = info["stat"]["share"]  # 转发数
            comment_count = info["stat"]["reply"]  # 评论数
            coin = info["stat"]["coin"]  # 投币
            favorite = info["stat"]["favorite"]  # 收藏
            duration = info["duration"]  # 时长
            print(bv_id,date,title)

            with open(f'视频数据.csv', 'a+', encoding='utf-8-sig') as f2:
                f2.write(date+','+trimName(title) + ','+'https://www.bilibili.com/video/'+bv_id+ ','+info['pic']+ ','+str(play_count)+','+str(like_count)+','+str(share_count)+','+str(comment_count)+ ','+str(coin)+ ','+str(favorite)+ ','+str(duration)+'\n')
    except Exception as e:
        print(f"错误信息: {e}")
