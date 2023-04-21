import re,requests,re,time,sys,csv,os
requests.packages.urllib3.disable_warnings()
# url='https://weibo.com/ttarticle/p/show?id=2309404650864861381210'
cookie = input('公众号苏生不惑提示你，请输入微博cookie:')
filename = input('公众号苏生不惑提示你，请输入csv文件名:')
if not cookie or not filename:
	print('输入有误')
	sys.exit(1)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        "Cookie":cookie
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
filename=filename.replace('.csv','')
f = open(f'{filename}.csv', encoding='UTF8')
csv_reader = csv.reader(f)
# df = pd.read_csv('5044429589.csv',encoding='utf_8_sig')
# df = df[df['头条文章地址'].notnull()]
# urls=df.头条文章地址.tolist()
# urls=[urls[0]]
# print("数量",len(urls))
if not os.path.exists('weibo_articles'):
    os.mkdir('weibo_articles')
for line in csv_reader:
	if line[3] == "头条文章地址" or not line[3]:
		continue
	try:
		res=requests.get(line[3],headers=headers, verify=False)
		title = re.search(r'<title>(.*?)</title>',res.text).group(1)
		weibo_time = re.search(r'<span class="time".*>(.*?)</span>',res.text).group(1)
		# print(title,weibo_time)
		if not weibo_time.startswith('20'):
			weibo_time=time.strftime('%Y')+'-'+weibo_time.strip().split(' ')[0]
		with open('articles/'+weibo_time+'_'+trimName(title)+'.html', 'w+', encoding='utf-8') as f:
			f.write(res.text.replace('"//','https://'))
			print('下载文章中',line[3])
	except Exception as e:
		print('错误信息',e,line[3])
