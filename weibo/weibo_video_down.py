import requests
import time
import json,html
import random,re,os,csv,sys
requests.packages.urllib3.disable_warnings()
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename

if not os.path.exists('video'):
    os.mkdir('video')
uid=input('请输入微博uid：')
name=input('请输入微博视频分类名称：')
cookie=input('请输入微博cookie：')
headers = {
'referer': 'https://weibo.com',
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
}

url=f'https://weibo.com/ajax/profile/getVideoTab?uid={uid}'
result = requests.get(url, headers=headers,verify=False,timeout=10).json()
# print(result)
if len(result['data']['playlists']) == 0:
	sys.exit('没有视频 ')
cid=0
for x in result['data']['playlists']:
	if name == x.get('name',''):
		cid = x.get('id',0)
		break
print(cid)
# url2=f'https://weibo.com/ajax/profile/getCollectionList?cid={cid}&cursor=&tab_code=0&has_header=true'
# result2 = requests.get(url2, headers=headers,verify=False,timeout=10).json()
# print(url2)
# first_cursor=0
# if len(result2['data']['header']['page_segments']) == 0:
# 	sys.exit('没有视频 ')
# first_cursor=result2['data']['header']['page_segments'][0]['first_cursor']
# print(first_cursor)
# url3=f'https://weibo.com/ajax/profile/getCollectionList?cid={cid}&cursor={first_cursor}&tab_code=0'
def down(cid,cursor):
	url = f'https://weibo.com/ajax/profile/getCollectionList?cid={cid}&cursor={cursor}&tab_code=0'
	result = requests.get(url, headers=headers,verify=False,timeout=10).json()
	if result:
		pass
	for x in result['data']['list']:
		time.sleep(1)
		video_data = requests.get(x.get('page_info').get('media_info').get('playback_list')[0]['play_info']['url'],headers=headers,verify=False,timeout=10)
		print('开始下载视频:',x.get('page_info').get('media_info').get('titles')[0]['title'])
		with open('video/'+replace_invalid_chars(x.get('page_info').get('media_info').get('titles')[0]['title'])+'.mp4','wb') as f:
			f.write(video_data.content)
	if result['data']['next_cursor'] != -1:
		down(cid,result['data']['next_cursor'])
down(cid,0)