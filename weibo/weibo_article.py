import re,requests,pandas,re,time
requests.packages.urllib3.disable_warnings()
cookie =''
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        "Cookie":cookie
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
df = pandas.read_csv('音乐先声/6236057337.csv',encoding='utf_8_sig')
df = df[df['头条文章链接'].notnull()]
urls=df.头条文章链接.tolist()
# urls=[urls[0]] https://github.com/dataabc/weibo-crawler
for url in urls:
	try:
		res=requests.get(url,headers=headers, verify=False)#;print(re.search(r'<title>(.*?)</title>',res.text).group(0))
		title = re.search(r'<title>(.*?)</title>',res.text).group(1)
		weibo_time = re.search(r'<span class="time".*?>(.*?)</span>',res.text).group(1)
		if not weibo_time.startswith('20'):
			weibo_time=time.strftime('%Y')+'-'+weibo_time.strip().split(' ')[0]
		with open('articles/'+weibo_time+'_'+trimName(title)+'.html', 'w+', encoding='utf-8') as f:
			f.write(res.text.replace('"//','https://'))
			print('下载微博文章',url)
	except Exception as e:
		print('错误信息',e,url)