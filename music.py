import requests
from bs4 import BeautifulSoup
import json,sys
import easygui as g

#https://zhuanlan.zhihu.com/p/193144459
while True:
    search = g.enterbox('请输入你想搜索的歌曲：',title='酷狗音乐下载器')
    if search ==None:
        sys.exit()
    if search!='':
        break
while True:
    number = g.enterbox('请输入你想下载多少首搜索出的歌曲，请输入对应数字（最多30）:', title='酷狗音乐下载器')
    if number ==None:
        sys.exit()
    if number != '':
        break
if int(number)>30:
    number='30'

search_headers={
    'referer':'https: // www.kugou.com/song /',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
search_results = 'http://songsearch.kugou.com/song_search_v2?callback=jQuery19109017207142454389_1595994946923&keyword='+search + \
    '&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1595994946925%27'

res=requests.get(search_results,headers=search_headers)
song_json =json.loads(res.text[res.text.index('(') + 1:-2])
song_list=song_json['data']['lists']
a=0
final_number=int(number)
for i in song_list:
    if a==int(number):
        break
    song_hash = i['FileHash']
    song_id = i['AlbumID']
    song_name = i['FileName'].replace('<em>','').replace('</em>','')
    song_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19109017207142454389_1595994946923&hash='+song_hash+'&album_id='+song_id+'&dfid=1aF52t2JD7yx11ML0H2JZ9UE&mid=2391153464a766aea6860623fc508772&platid=4&_=1595994946925'
    song_res = requests.get(song_url, headers=search_headers)
    song_js = json.loads(song_res.text[song_res.text.index('(') + 1:-2])
    url = song_js['data']['play_url']
    if url!='':
        res_finnal = requests.get(url, headers=search_headers)
        with open(song_name+'.mp3', 'wb') as f:
            f.write(res_finnal.content)
        print('【'+song_name+'.mp3】下载完成')
    else:
        print('【'+song_name+'.mp3】无版权，无法下载！')
        final_number-=1
    a += 1
print('-----------------------------------')
print('【'+str(final_number)+'首音乐已下载完毕！】')