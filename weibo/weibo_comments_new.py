import requests,re,csv,time,random,urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime
def trimName(name):
    return name.replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')

def comments(mid,count,headers,max_id):
	url=f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count={count}&uid=2087169013&fetch_level=0&locale=zh-CN&max_id={max_id}'
	print(url)
	res=requests.get(url, headers=headers, verify=False,timeout=5).json()
	if not res["data"]:
		print(res)
		return False
	for v in res["data"]:
		parsed_datetime = datetime.strptime(v['created_at'], "%a %b %d %H:%M:%S %z %Y")#Mon Nov 06 14:06:06 +0800 2023
		formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
		try:
			# soup = BeautifulSoup(v['source'], 'html.parser')
			# source = soup.text#删除HTML标签
			source = v.get('source','')
			total_number = v.get('total_number',0)
			print(v['text_raw'])
			with open(f'{mid}.csv', 'a+', encoding='utf-8-sig') as f:
				f.write(trimName(v['user']['screen_name'])+','+trimName(v['user']['idstr']) + ','+formatted_datetime+ ','+trimName(v['text_raw'])+ ','+source+ ','+str(total_number)+ ','+str(v['like_counts'])+'\n')
			if total_number > 0:
				commentsChild(mid,v['id'],20,headers,0)
		except Exception as e:
			print(e,url,res);raise Exception(e)
	time.sleep(2)
	comments(mid,count,headers,res['max_id'])		
	return True
def commentsChild(mid,midChild,count,headers,max_id):
	url=f'https://weibo.com/ajax/statuses/buildComments?flow=1&is_reload=1&id={midChild}&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id={max_id}&count={count}&uid=2087169013&locale=zh-CN'
	print('子评论',url)
	res=requests.get(url, headers=headers, verify=False,timeout=5).json()
	if not res["data"]:
		print(res)
		return False
	for v in res["data"]:
		parsed_datetime = datetime.strptime(v['created_at'], "%a %b %d %H:%M:%S %z %Y")#Mon Nov 06 14:06:06 +0800 2023
		formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
		try:
			# soup = BeautifulSoup(v['source'], 'html.parser')
			# source = soup.text#删除HTML标签
			source = v.get('source','')
			total_number = v.get('total_number',0)
			print(v['text_raw'])
			with open(f'{mid}.csv', 'a+', encoding='utf-8-sig') as f:
				f.write(trimName(v['user']['screen_name'])+','+trimName(v['user']['idstr']) + ','+formatted_datetime+ ','+trimName(v['text_raw'])+ ','+source+ ','+str(total_number)+ ','+str(v['like_counts'])+'\n')
		except Exception as e:
			print(e,url,res);raise Exception(e)
	if res['max_id'] == 0:
		print(res['trendsText'])
		return False
	time.sleep(3)
	commentsChild(mid,midChild,count,headers,res['max_id'])		
	return True
count = 20
mid=input('请输入微博mid：')
if not mid:
	sys.exit('mid为空')
cookie=input('请输入微博cookie：')
cookie=''
if not cookie:
	sys.exit('cookie为空')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 FirePHP/0.7.4',
        'Cookie': cookie
               # 'Referer': 'https://m.weibo.cn/detail/4497103885505673',
               # 'Sec-Fetch-Mode': 'navigate'
    }
with open(f'{mid}.csv', 'a+', encoding='utf-8-sig') as f:
    f.write('微博昵称'+','+'微博uid' + ','+'评论时间'+','+'评论内容'+','+'评论地区'+','+'回复数'+','+'点赞数'+ '\n')
comments(mid,count,headers,0)
print('抓取结束')