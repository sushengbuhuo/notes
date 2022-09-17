import requests,pdfkit,json,time,datetime,os,re,html,pandas,csv,os
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
def down(url,channel_id):
    response = requests.get(url, headers=headers)
    res = response.json();print(url)
    has_more = res['data']['has_more']
    for i in res['data']['list']:
    	if 'bvid' in i:
            danmaku = '0'
            if 'danmaku' in i:
                danmaku = str(i['danmaku'])
            with open('视频列表.csv', 'a+', encoding='utf-8-sig') as f:
                f.write(i['name']+','+i['cover']+','+str(i['view_count'])+','+str(i['like_count'])+','+i['duration']+','+i['author_name']+','+'https://www.bilibili.com/'+i['bvid']+','+danmaku+'\n')
            with open('视频列表.txt', 'a+', encoding='utf-8') as f:
                f.write(i['bvid']+'\n')
    if has_more:
    	down(f'https://api.bilibili.com/x/web-interface/web/channel/featured/list?channel_id={channel_id}&filter_type=0&offset={res["data"]["offset"]}&page_size=30',channel_id)
    else:
    	return False
channel_id=input('输入频道id:')
url = f'https://api.bilibili.com/x/web-interface/web/channel/featured/list?channel_id={channel_id}&filter_type=0&offset=&page_size=30'
with open('视频列表.csv', 'a+', encoding='utf-8-sig') as f:
     f.write('标题'+','+'封面'+','+'播放量'+','+'点赞量'+','+'时长'+','+'up主'+','+'视频链接'+','+'弹幕数'+'\n')
down(url,channel_id)
# https://www.bilibili.com/v/channel/35826?tab=featured

file = open('视频列表.txt').read()
ids = file.split('\n')
ids=ids[:1]
print(len(ids))
for i in ids:
    print(i)
    os.system(f"lux -f 16-12 {i}")