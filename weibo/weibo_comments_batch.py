import requests,re,csv,time,random,urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime
def trimName(name):
    return name.replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
def count_csv_rows(filename):
    with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        row_count = sum(1 for row in csv_reader)
    return row_count
def comments(m,mid,count,headers,max_id):
	if max_id == 0:
		with open(f'comments/{m}.csv', 'a+', encoding='utf-8-sig') as f:
			f.write('微博昵称'+','+'微博uid' + ','+'评论时间'+','+'评论内容'+','+'评论地区'+','+'回复数'+','+'点赞数'+ '\n')
	url=f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count={count}&uid=2087169013&fetch_level=0&locale=zh-CN&max_id={max_id}'
	num=count_csv_rows(f'comments/{m}.csv')
	if num > 5000:
		return False
	# print(url)
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
			# print(v['text_raw'])
			with open(f'comments/{m}.csv', 'a+', encoding='utf-8-sig') as f:
				f.write(trimName(v['user']['screen_name'])+','+trimName(v['user']['idstr']) + ','+formatted_datetime+ ','+trimName(v['text_raw'])+ ','+source+ ','+str(total_number)+ ','+str(v['like_counts'])+'\n')
			if total_number > 0:
				commentsChild(m,mid,v['id'],20,headers,0)
		except Exception as e:
			print(e,url,res)#;raise Exception(e)
	if res['max_id'] == 0:
		print(res['trendsText'])
		return False
	time.sleep(1)
	comments(m,mid,count,headers,res['max_id'])		
	return True
def commentsChild(m,mid,midChild,count,headers,max_id):
	url=f'https://weibo.com/ajax/statuses/buildComments?flow=1&is_reload=1&id={midChild}&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id={max_id}&count={count}&uid=2087169013&locale=zh-CN'
	# print('子评论',url)
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
			# print(v['text_raw'])
			with open(f'comments/{m}.csv', 'a+', encoding='utf-8-sig') as f:
				f.write(trimName(v['user']['screen_name'])+','+trimName(v['user']['idstr']) + ','+formatted_datetime+ ','+trimName(v['text_raw'])+ ','+source+ ','+str(total_number)+ ','+str(v['like_counts'])+'\n')
		except Exception as e:
			print(e,url,res)#;raise Exception(e)
	if res['max_id'] == 0:
		print(res['trendsText'])
		return False
	time.sleep(2)
	commentsChild(m,mid,midChild,count,headers,res['max_id'])		
	return True
count = 20
# mid=input('请输入微博mid：')
# if not mid:
# 	sys.exit('mid为空')
cookie=input('请输入微博cookie：')
if not cookie:
	sys.exit('cookie为空')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 FirePHP/0.7.4',
        'Cookie': cookie
               # 'Referer': 'https://m.weibo.cn/detail/4497103885505673',
               # 'Sec-Fetch-Mode': 'navigate'
    }
if not os.path.exists('comments'):
    os.mkdir('comments')
# comments(mid,count,headers,0)
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def base62_encode(num, alphabet=ALPHABET):
    num = int(num)
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def base62_decode(string, alphabet=ALPHABET):
    string = str(string)
    num = 0
    idx = 0
    for char in string:
        power = (len(string) - (idx + 1))
        num += alphabet.index(char) * (len(alphabet) ** power)
        idx += 1

    return num
def reverse_cut_to_length(content, code_func, cut_num=4, fill_num=7):
    content = str(content)
    cut_list = [content[i - cut_num if i >= cut_num else 0:i] for i in range(len(content), 0, (-1 * cut_num))]
    cut_list.reverse()
    result = []
    for i, item in enumerate(cut_list):
        s = str(code_func(item))
        if i > 0 and len(s) < fill_num:
            s = (fill_num - len(s)) * '0' + s
        result.append(s)
    return ''.join(result)
# reverse_cut_to_length('5002742349956958', base62_encode, 7, 4)
# print(reverse_cut_to_length('O19l8FMg6', base62_decode, 4, 7))
f = open(f'1744395855.csv', encoding='utf-8-sig')
csv_reader = csv.reader(f)
num=0
for line in csv_reader:
    if line[0] == "微博链接":
        continue
    num+=1
    print(f'第{num}条微博链接:',line[0])
    m=re.search(r'https://www\.weibo\.com/\d+/(.*)',line[0]).group(1)
    mid=reverse_cut_to_length(m, base62_decode, 4, 7)
    comments(m,mid,count,headers,0)
    time.sleep(random.randint(1, 2))
    # break
print('抓取结束')