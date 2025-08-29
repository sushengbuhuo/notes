import requests
import time
import json,html
import random,re,os,csv
requests.packages.urllib3.disable_warnings()
# 东方财富 https://emcreative.eastmoney.com/app_fortune/person/index.html?uid=3825336190592976&anchor=0&userv=1&subAnchor=0&latestChannelId=&version=20240225202&basefilter=0&douguSwitch=1 https://emcreative.eastmoney.com/app_fortune/article/index.html?postId=1393015277
def remove_html_tags(text):
    # 匹配所有HTML标签的正则表达式
    clean = re.compile('<.*?>')
    # 替换匹配到的标签为空字符串
    return re.sub(clean, '', text)
def remove_html_tags2(text):
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(text, "html.parser")
    # 获取纯文本
    return soup.get_text()
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
msg_url = "https://emcreative.eastmoney.com/FortuneApi/GuBaApi/common"
article_url='https://i.eastmoney.com/api/guba/postCenterList'
post_url = "https://i.eastmoney.com/api/guba/postCenterList"
Cookie = ""
headers = {
    "Cookie": Cookie,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://i.eastmoney.com/2238094774109802',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 FirePHP/0.7.4',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
def post(page,callback_param):
	p=page+1
	print(f'第{page}页')
	params = {
    'uid': '2238094774109802',
    'pagesize': '10',
    'type': '1',
    'filterType': '2',
    'onlyYt': '0',
    'pagenum': str(page),
    'callbackParam': callback_param,
    # '_': str(int(time.time())),
	}
	time.sleep(2)
	res=requests.get(post_url, headers=headers, params=params).json()
	data=res.get('result','')#;print(res)
	callback_param=res.get('callback_param','')
	if not data:
		return True
	for i in data:
		print(i['post_title'],i['post_publish_time'],i['post_id'])
		date=i['post_publish_time'][0:10]
		title=remove_html_tags(i['post_content'])[:64]
		url='https://guba.eastmoney.com/news,fshfeagm,'+str(i['post_id'])+'.html'
		post_content = i['post_content']
		if i['post_pic_url']:
			for img in i['post_pic_url']:
				post_content+=f'<br><img src="{img}"><br>'
		if i['source_post_content']:
			post_content+='\n<br><br><p style="color: red;">源贴：</p>\n<br>'+i['source_post_title']+'\n<br><br>'+i['source_post_content']
		content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1><h3>%s</h3>%s</body></html>' % (
			title, url,post_content)
		with open('html/'+date+'_'+replace_invalid_chars(title)+'.html', 'w', encoding='utf-8') as f:
			f.write(content)
		with open(f'帖子目录.md', 'a+', encoding='utf-8') as f2:
			f2.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n\n')
		with open(f'eastmoney.txt', 'a+', encoding='utf-8') as f3:
			f3.write('https://guba.eastmoney.com/news,fshfeagm,'+str(i['post_id'])+'.html\n')
	post(p,callback_param)
def article(page,callback_param):
	p=page+1
	print(f'第{page}页')
	params = {
    'uid': '3825336190592976',
    'onlyYt': '0',
    'ctoken': '',
    'utoken': '',
    'deviceid': '172.30.66.125',
    'version': '9001',
    'product': 'Guba',
    'plat': 'Wap',
    'gtoken': '',
    'type': '1',
    'filterType': '0',
    'noinlist': '0',
    'p': str(page),
    'ps': '10',
    'callback_param': callback_param,
	}
	time.sleep(2)
	# print(data)
	res=requests.get(article_url, headers=headers, params=params).json()
	data=res.get('re','')
	callback_param=res.get('callback_param','')
	if not data:
		return True
	for i in data:
		print(i['post_title'],i['post_publish_time'],i['post_id'])
		with open(f'eastmoney.txt', 'a+', encoding='utf-8') as f3:
			f3.write('https://caifuhao.eastmoney.com/news/'+str(i['post_id'])+'\n')
	article(p,callback_param)
def down3(page):
	data1={'parm':f'ctoken=mdGfR6OXdEc4cii06HYA7-IMNL88s8KxN_Pg9iesJQqjcIyuHXu_nJwJymyL3m-0zXTx7sHwdIDsC9bNh71YM3VJ-NjilJHwuLKxXr2UI2KuZwOpPjMHscy20HTNvXSE_yA9RmguCNM-ZIqMnIJxsYnJUduXWZPkks_aSIeAs9Q&utoken=FobyicMgeV4XKdbUhrvvY0QBhrziMEAsJdkk7KmvNW1_zk6Y5Ux1mL0auEKqjwFCCSbWaLa8laGXziKTbxU-oWCXXLQmoJOjMF-iwlt7gI0FvnGue-KoLM0Nv5kNbGEmzg3r75A6-Aq4axT6obA-jBZuOAEymqI8DKZJZDhaa0nrpyNswEU-gUvQZul1JhUT1mAXKUaol6FH7WnX2AnLHvrgDS7RV3C1P4qd0AtdDFJcxssfzB3M8A134FQOjX-x3NhriP3zfR8Q_Izo9H8kbJVLF3dv61xu&deviceid=172.30.66.125&version=9001&product=Guba&plat=Wap&gtoken=&uid=2717094178652400&type=1&ps=10&p={page}','sumit':'form','type':'Post','url':'userpostlist/api/article/UserDynamicListV2'}
	p=page+1
	time.sleep(2)
	# print(data)
	res=requests.post(msg_url, headers=headers, data=json.dumps(data1)).json()
	data=res.get('re','')
	if not data:
		return True
	for i in data:
		print(i['post_title'],i['post_publish_time'],i['post_id'])
		pid=i['post_id']
		data2={'parm':f'ctoken=mdGfR6OXdEc4cii06HYA7-IMNL88s8KxN_Pg9iesJQqjcIyuHXu_nJwJymyL3m-0zXTx7sHwdIDsC9bNh71YM3VJ-NjilJHwuLKxXr2UI2KuZwOpPjMHscy20HTNvXSE_yA9RmguCNM-ZIqMnIJxsYnJUduXWZPkks_aSIeAs9Q&utoken=FobyicMgeV4XKdbUhrvvY0QBhrziMEAsJdkk7KmvNW1_zk6Y5Ux1mL0auEKqjwFCCSbWaLa8laGXziKTbxU-oWCXXLQmoJOjMF-iwlt7gI0FvnGue-KoLM0Nv5kNbGEmzg3r75A6-Aq4axT6obA-jBZuOAEymqI8DKZJZDhaa0nrpyNswEU-gUvQZul1JhUT1mAXKUaol6FH7WnX2AnLHvrgDS7RV3C1P4qd0AtdDFJcxssfzB3M8A134FQOjX-x3NhriP3zfR8Q_Izo9H8kbJVLF3dv61xu&deviceid=$IP$&version=9008000&product=StockWay&plat=Wap&location=&postid={pid}&IsMatch=false&type=0&cutword=true&paytext=true','sumit':'form','type':'post','url':'content/api/Post/ArticleContent'}
		res2=requests.post('https://emcreative.eastmoney.com/FortuneApi/GuBaApi/common', headers=headers, data=json.dumps(data2)).json()
		content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1><h3>%s</h3>%s</body></html>' % (
            res2['post']['post_title'], '发布日期：'+res2['post']['post_publish_time']+'   原文链接：https://emcreative.eastmoney.com/app_fortune/article/index.html?postId='+str(i['post_id']),res2['post']['post_content'].replace('\\', ''))
		# print(res2['post']['post_abstract'])
		title=trimName(res2['post']['post_title'])
		if not title:
			title = str(pid)
		try:
			with open('html/'+res2['post']['post_publish_time'][0:10]+'-'+title+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
		except Exception as err:
			raise Exception(err)
			with open('html/'+str(random.randint(100,10000))+'.html', 'w', encoding='utf-8') as f:
				f.write(content)
	down2(p)
post(1,'')
# url='https://www.cdstm.cn/theme/kkxw/tyt/kxkkm_1/'
# res=requests.get(url).text
# audio=re.search(r'var audioList =\s+(.*?);',res).group(1)

# json_dict = json.loads(audio.replace("src",'"src"').replace("name",'"name"'))
# print(audio,json_dict)
# for i in json_dict:
# 	if not i:
# 		continue
# 	# hex_string = i.get('name').replace("\\x", "")
# 	# # 将十六进制编码的字符串转换为字节序列
# 	# byte_sequence = bytes.fromhex(hex_string)
# 	# # 将字节序列解码为字符串
# 	# result_string = byte_sequence.decode('utf-8')
# 	name=re.search(r'(\d+)',i.get('name')).group(1)
# 	print(i.get('src'),name,type(i.get('name')))
# 	audio_data = requests.get(i.get('src'))
# 	with open('audio/'+trimName(f'第{name}集')+'.mp3','wb') as f5:
# 		f5.write(audio_data.content)

