# -*- coding:utf-8 -*-
import os
import requests
import prettytable as pt
input_name = input("请输入你要下载的歌曲或歌手：")
url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn=1&rn=30&httpsStatus=1&reqId=64b76101-9883-11ec-9b9e-2f1fed2b10cf".format(input_name)
headers = {
    'User-Agent': 'UA',
    'Cookie': 'cookie',
    'Host': 'www.kuwo.cn',
    'Referer': 'referer'
}#https://www.52pojie.cn/thread-1629787-1-1.html
music_list = requests.get(url=url, headers=headers).json()["data"]["list"]
music_tb = pt.PrettyTable()
music_tb.field_names = ["序号", "歌曲", "歌手"]
num = 0
music_rid_list = []
for music in music_list:
    music_rid = music["rid"]
    music_name = music["name"]
    music_artist = music["artist"]
    music_rid_list.append([music_rid, music_name, music_artist])
    music_tb.add_row([num, music_name, music_artist])
    num += 1
print(music_tb)
while True:
    music_tb_index = eval(input("请输入你想下载的歌曲序号(输入-1退出程序)：\t"))
    if music_tb_index == -1:
        print("bye!")
        break
    rid = music_rid_list[music_tb_index][0]
    music_url = 'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={}&type=convert_url3&br=320kmp3'.format(rid)
    download_url = requests.get(music_url).json()["data"]["url"]
    music = requests.get(download_url).content
    if not os.path.exists(r"./music"):
        os.mkdir(r"./music")
    else:
        with open(f'./music/{music_rid_list[music_tb_index][1]}-{music_rid_list[music_tb_index][2]}.mp3', mode="wb") as f:
            f.write(music)
            print("{}-{},download successful!go go go!".format(music_rid_list[music_tb_index][1], music_rid_list[music_tb_index][2]))