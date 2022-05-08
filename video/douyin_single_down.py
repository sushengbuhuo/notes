import requests,re,json,os,sys
url = input('公众号苏生不惑提示你，请输入抖音视频链接:')
headers = {
	'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
} #https://v.douyin.com/d6s55wa/  https://www.douyin.com/video/7001337943700819235 主页https://v.douyin.com/eLhwxF2/
if url == '':
	print('链接为空')
	exit(1)
# def getId(url):
# 	m1= re.match(r'^https?://v.douyin.com/(.*)$', url)
# 	m2 = re.match(r'^https?://www.douyin.com/video/(\d+)\??.*$',url)
# 	item_id = ''
# 	if m1:
# 		try:
# 			rep = requests.get(url=url, headers=headers, timeout=5).url
# 			item_id = re.findall('video[/](.*?)[/]', rep)[0]
# 		except Exception as e:
# 			pass
# 	if m2:
# 		item_id = m2.group(1)
# 	return item_id
# item_id = getId(url)

res = requests.get(url=url, headers=headers, timeout=5)
item_id = re.findall('video/(\d+)?',str(res.url))[0]
if item_id == '':
	print('链接错误')
	exit(1)
douyin_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}&dytk='.format(item_id)
response = requests.get(url=douyin_url, headers=headers, timeout=5).text
response_json = json.loads(response)
print('视频id:'+item_id)
video_data = {}
video_url = str(response_json['item_list'][0]['video']['play_addr']['url_list'][0]).replace('playwm','play')   #去水印后链接
music_url = str(response_json['item_list'][0]['music']['play_url']['url_list'][0])
video_title = re.sub(r"[\/\\\:\*\?\"\<\>\|]", "", response_json['item_list'][0]['desc'])
music_title = str(response_json['item_list'][0]['music']['author'])
response = requests.get(url=video_url, headers=headers, timeout=5).content
with open(f'{video_title}.mp4', 'wb') as f:
	f.write(response)
	f.close()
response = requests.get(url=music_url, headers=headers, timeout=5).content
with open(f'{video_title}.mp3', 'wb') as f:
	f.write(response)
	f.close()	
#vid = response_json['item_list'][0]['video']['vid']
# play_url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id={}&line=0&ratio=720p&media_type=4&vr_type=0&improve_bitrate=0&is_play_url=1&is_support_h265=0&source=PackSourceEnum_PUBLISH'.format(vid)
# response = requests.get(url=play_url, headers=headers, timeout=5).content
# with open(f'{video_title}.mp4', 'wb') as f:
# 	f.write(response)
# 	f.close()
print('下载完成')