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
with open(f'{name}.txt', encoding='utf-8') as f:
    contents = f.read()
urls=contents.split('\n')
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ').replace('"', '“')
def data(url):
	try:
		response = requests.get(url, headers=headers)
		res = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?)</script></body></html>',response.text,flags=re.S)
		print(res[0])
		data=json.loads(res[0].replace('undefined','""'))
		note_id = re.search(r'https?://www\.xiaohongshu\.com/explore/(.*)',url).group(1)
		ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['note']['noteDetailMap'][note_id]['note']['time'] / 1000))
		utime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['note']['noteDetailMap'][note_id]['note']['lastUpdateTime'] / 1000))
		ip=data['note']['noteDetailMap'][note_id]['note'].get('ipLocation','')
		if '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['likedCount'] or '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['collectedCount'] or '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['commentCount'] or '+' in data['note']['noteDetailMap'][note_id]['note']['interactInfo']['shareCount']:
			with open(f'{name}失败列表.txt', 'a+', encoding='utf-8') as f2:
				f2.write(url+ '\n')
			return True
		note_type='图文'
		if data['note']['noteDetailMap'][note_id]['note']['type'] == 'video':
			note_type = '视频'
		images = ''
		if len(data['note']['noteDetailMap'][note_id]['note']['imageList']) > 0:
			for img in data['note']['noteDetailMap'][note_id]['note']['imageList']:
				images+=trimName(img['urlDefault'].replace('\u002F','/'))+"，"
		tags = ''
		if len(data['note']['noteDetailMap'][note_id]['note']['tagList']) > 0:
			for tag in data['note']['noteDetailMap'][note_id]['note']['tagList']:
				tags+=trimName(tag['name'])+"#"
		with open(f'{name}数据.csv', 'a+', encoding='utf-8-sig', newline='') as ff:
			ff.write(ctime+','+utime+','+trimName(data['note']['noteDetailMap'][note_id]['note']['title']) + ','+ip+  ','+url+ ','+trimName(data['note']['noteDetailMap'][note_id]['note']['desc'])+ ','+images+','+note_type+','+tags+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['likedCount']+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['collectedCount']+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['commentCount']+','+data['note']['noteDetailMap'][note_id]['note']['interactInfo']['shareCount']+'\n')
		# print(data)
		return True
	except Exception as e:
		print(e,url);raise Exception("抓取失败了："+url)

with open(f'{name}数据.csv', 'a+', encoding='utf-8-sig', newline='') as ff:
    ff.write('发布时间'+','+'更新时间'+','+'标题'+','+'ip' + ','+'链接'+ ','+'内容'+ ','+'图片链接'+','+'类型'+','+'标签'+','+'点赞数'+','+'收藏数'+','+'评论数'+','+'分享数'+'\n')
for url in urls:
    res = data(url)
    time.sleep(randint(1, 4))
    if not res:
       continue
    if res == "error":
       break
# response = requests.get('https://www.xiaohongshu.com/explore/6026775c0000000021035e1e', headers=headers)
# res = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?)</script></body></html>',response.text,flags=re.S)
# print(res[0])
# data=json.loads(res[0].replace('undefined','""'))
# print(data)