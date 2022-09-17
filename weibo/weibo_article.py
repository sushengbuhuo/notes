import re,requests,pandas,re,time
requests.packages.urllib3.disable_warnings()
cookie ='login_sid_t=f7538b0cb61e638646b7c0307d38d84e; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=3423612421583.007.1624065339537; SINAGLOBAL=3423612421583.007.1624065339537; YF-V-WEIBO-G0=b09171a17b2b5a470c42e2f713edace0; XSRF-TOKEN=69v_-Lzz-Lyfa0GpX2R6GNhd; __gads=ID=7ec05857ca68924e:T=1630124363:S=ALNI_MYKgiHHLvG3HSTGqrYKQMEsASi2UA; TC-V-WEIBO-G0=35846f552801987f8c1e8f7cec0e2230; ULOGIN_IMG=16349542994012; Hm_lpvt_1f12b0865d866ae1b93514870d93ce89=1651591964; Hm_lvt_1f12b0865d866ae1b93514870d93ce89=1651591964; ULV=1655217686213:1:1:1:3423612421583.007.1624065339537:; UPSTREAM-V-WEIBO-COM=35846f552801987f8c1e8f7cec0e2230; SSOLoginState=1659144445; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW1cajqHaL9UWbevdkzPrX95JpX5KMhUgL.FozNeKM4e05ceh22dJLoIEBLxKnL12zL12qLxKML1KBL1-qLxKBLBonL12BLxKqL1heL1K2t; ALF=1693739181; SCF=AupqOl8UKXkR5VBOFLBDq0Sj4ZXJnwLWyZLrddP462ABrTFlbTK11cEejjyE1_3ESAEFaAL1ahPG7g72FXkjifs.; SUB=_2A25OF0V9DeRhGeRJ6lUY8y7Kyz2IHXVtZTG1rDV8PUNbmtANLXigkW9NUn_GnjogdefwWWNqJ8u05gMQtfXxZnFk; wvr=6; UOR=,,login.sina.com.cn; wb_timefeed_2717930601=1; wb_view_log_2717930601=1494*9341.3499999046325684; WBPSESS=HpgDfnaKW52ew_rL_kRj37oqk2QHTOYpcaprwYC93qjdvxLuoOmn7COW12nvOH3eiv1jaMOKEmzUwj7sWKTfbuNkTOB0ISEihKkNWNDx0-ruSla4DX9-TOS6ov2-WG_e; webim_unReadCount=%7B%22time%22%3A1662260227101%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A1144%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A1146%2C%22msgbox%22%3A0%7D; PC_TOKEN=d01ac33c7a; WBStorage=4d96c54e|undefined'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        "Cookie":cookie
    }
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
df = pandas.read_csv('音乐先声/6236057337.csv',encoding='utf_8_sig')
df = df[df['头条文章链接'].notnull()]
urls=df.头条文章链接.tolist()
# urls=[urls[0]]
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