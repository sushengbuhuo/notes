import requests,json,time,datetime,os,re,html,csv
from random import randint
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cookie =''
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309021a) XWEB/6919",
        'cookie':cookie,
    }
name=input('请输入文件名：')
with open(f'{name}', encoding='utf-8') as f:
    contents = f.read()
urls=contents.split('\n')
def get_history():
    history = []
    with open('xiaohongshu_history.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history
#https://github.com/ReaJason/xhs 
def save_history(url):
    with open('xiaohongshu_history.txt', 'a+') as f:
        f.write(url.strip() + '\n')
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ').replace('"', '“')
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def remove_query_params(url):
    url_parts = url.split('?')
    if len(url_parts) > 1:
        url_without_query = url_parts[0]
    else:
        url_without_query = url
    
    return url_without_query
if not os.path.exists('image'):
	os.mkdir('image')
if not os.path.exists('txt'):
	os.mkdir('txt')
if not os.path.exists('video'):
	os.mkdir('video')
def data(url):
	try:
		url=remove_query_params(url)
		response = requests.get(url, headers=headers)
		res = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?)</script></body></html>',response.text,flags=re.S)
		print('开始下载:',url)
		data=json.loads(res[0].replace('undefined','""'))
		note_id = re.search(r'https?://www\.xiaohongshu\.com/explore/(.*)',url).group(1)
		ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['note']['noteDetailMap'][note_id]['note']['time'] / 1000))
		utime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['note']['noteDetailMap'][note_id]['note']['lastUpdateTime'] / 1000))
		ip=data['note']['noteDetailMap'][note_id]['note'].get('ipLocation','')
		if '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['likedCount'] or '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['collectedCount'] or '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['commentCount'] or '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['shareCount']:
			with open(f'{name}下载失败列表.txt', 'a+', encoding='utf-8') as f2:
				f2.write(url+ '\n');print(data['note']['noteDetailMap'][note_id]['note'],url)
			return True
		note_type='图文'
		if data['note']['noteDetailMap'][note_id]['note']['type'] == 'video':
			note_type = '视频'
			print(data['note']['noteDetailMap'][note_id]['note'])
			for key, value in data['note']['noteDetailMap'][note_id]['note']['video']['media']['stream'].items():
				if len(value) > 0:
					video_data = requests.get(value[0]['masterUrl'],headers=headers)
					with open('video/'+ctime[0:10]+'_'+replace_invalid_chars(trimName(data['note']['noteDetailMap'][note_id]['note']['title']))+'.mp4','wb') as ff:
						ff.write(video_data.content)
					break
		images = ''
		if len(data['note']['noteDetailMap'][note_id]['note']['imageList']) > 0:
			num = 0
			for img in data['note']['noteDetailMap'][note_id]['note']['imageList']:
				# picUrl = f"https://sns-img-qc.xhscdn.com/{img['traceId']}"
				images+=trimName(img['urlDefault'].replace('\u002F','/'))+"，"
				num+=1
				img_data = requests.get(img['urlDefault'].replace('\u002F','/'),headers=headers)
				print('正在下载图片：'+img['urlDefault'].replace('\u002F','/'))
				with open('image/'+ctime[0:10]+'_'+replace_invalid_chars(trimName(data['note']['noteDetailMap'][note_id]['note']['title']))+'_'+str(num)+'.jpg','wb') as f6:
					f6.write(img_data.content)
		tags = ''
		if len(data['note']['noteDetailMap'][note_id]['note']['tagList']) > 0:
			for tag in data['note']['noteDetailMap'][note_id]['note']['tagList']:
				tags+=trimName(tag['name'])+"#"
		with open(f'{name}数据.csv', 'a+', encoding='utf-8-sig', newline='') as ff:
			ff.write(ctime+','+utime+','+trimName(data['note']['noteDetailMap'][note_id]['note']['title']) + ','+ip+  ','+url+ ','+trimName(data['note']['noteDetailMap'][note_id]['note']['desc'])+ ','+images+','+note_type+','+tags+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['likedCount']+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['collectedCount']+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['commentCount']+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['shareCount']+'\n')
		with open('txt/'+ctime[0:10]+'_'+replace_invalid_chars(trimName(data['note']['noteDetailMap'][note_id]['note']['title']))+'.txt', 'a+', encoding='utf-8') as f22:
			f22.write(data['note']['noteDetailMap'][note_id]['note']['desc'])
		save_history(url)
		# print(data)
		return True
	except Exception as e:
		print(e,url);raise Exception("抓取失败了："+url)
urls_history = get_history()
with open(f'{name}数据.csv', 'a+', encoding='utf-8-sig', newline='') as ff:
    ff.write('发布时间'+','+'更新时间'+','+'标题'+','+'ip' + ','+'链接'+ ','+'内容'+ ','+'图片链接'+','+'类型'+','+'标签'+','+'点赞数'+','+'收藏数'+','+'评论数'+','+'分享数'+'\n')
for url in urls:
    if url in urls_history:
        print('已经下载过:'+url)
        continue
    res = data(url)
    time.sleep(randint(2, 5))
    if not res:
       continue
    if res == "error":
       break
# response = requests.get('https://www.xiaohongshu.com/explore/6026775c0000000021035e1e', headers=headers)
# res = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?)</script></body></html>',response.text,flags=re.S)
# print(res[0])
# data=json.loads(res[0].replace('undefined','""'))
# print(data)