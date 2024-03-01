import requests,re,csv,time,random,urllib3,sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests,re,csv,time,random,pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image
from datetime import datetime
def trimName(name):
    return name.replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
def count_csv_rows(filename):
    with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        row_count = sum(1 for row in csv_reader)
    return row_count
def comments(mid,count,headers,max_id):
	if max_id == 0:
		with open(f'{mid}.csv', 'a+', encoding='utf-8-sig') as f:
			f.write('微博昵称'+','+'微博uid' + ','+'评论时间'+','+'评论内容'+','+'评论地区'+','+'回复数'+','+'点赞数'+ '\n')
	url=f'https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={mid}&is_show_bulletin=2&is_mix=0&count={count}&uid=2087169013&fetch_level=0&locale=zh-CN&max_id={max_id}'
	num=count_csv_rows(f'{mid}.csv')
	if num > 5000:
		return False
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
			print(e,url,res)#;raise Exception(e)
	if res['max_id'] == 0:
		print(res['trendsText'])
		return False
	time.sleep(2)
	comments(mid,count,headers,res['max_id'])		
	return True
def commentsChild(mid,midChild,count,headers,max_id):
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
def close_on_any_input():
    # 提示用户输入任何字符
    print("输入任何字符关闭程序...")
    # 等待用户输入
    input()
def remove_query_params(url):
    # 使用 split() 方法将 URL 按照问号分割成两部分
    url_parts = url.split('?')
    
    # 检查是否存在问号
    if len(url_parts) > 1:
        # 存在问号，只取问号前面的部分
        url_without_query = url_parts[0]
    else:
        # 不存在问号，保持原样
        url_without_query = url
    
    return url_without_query
while True:
	url = ''
	cookie = ''
	if len(sys.argv) > 1:
		url = sys.argv[1]
	if not url:
		print('本工具更新于2024年3月5日，获取最新版本请关注公众号苏生不惑')
		url=input('请输入微博链接：')
		if not url:
			sys.exit('微博链接为空')
		cookie=input('请输入微博cookie：')
		if not cookie:
			sys.exit('cookie为空')

	headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Cookie': cookie
               # 'Referer': 'https://m.weibo.cn/detail/4497103885505673',
               # 'Sec-Fetch-Mode': 'navigate'
    }
	# https://weibo.com/1744395855/NFM1mexIw  https://m.weibo.cn/detail/4999560443466204
	m=re.search(r'https://(www\.)?weibo\.com/\d+/(.*)',remove_query_params(url))
	if m:
		mid=reverse_cut_to_length(m.group(2), base62_decode, 4, 7)
		comments(mid,count,headers,0)

	m2=re.search(r'https://m\.weibo\.cn/(detail|status)/(\d+)',remove_query_params(url))
	if m2:
		comments(m2.group(2),count,headers,0)

	print('done!')
def ip_detail(mid):
    df = pd.read_csv(f"{mid}.csv",encoding='utf-8',on_bad_lines='skip')
    df2=df.评论地区.value_counts().sort_values(ascending=False).head(10)
    ip = df2.index.tolist()
    counts = df2.values.tolist()
    bar = (
        Bar()
            .add_xaxis(ip)
            .add_yaxis("", counts)
    )
    pie = (
        Pie()
        .add("", [list(z) for z in zip(ip, counts)],radius=["40%", "75%"], )
        .set_global_opts(title_opts=opts.TitleOpts(title="饼图",pos_left="center",pos_top="20"))
        .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"), )
    )
    pie.render(str(mid) +'.html')
    # df2.to_csv(str(mid) +".csv",encoding="utf_8_sig",index=False)
def wordcloud_img(mid):
    font = r'C:\Windows\Fonts\simhei.ttf'
    STOPWORDS = {"回复", '的','可以','吗','了','有','ca'}#https://github.com/baipengyan/Chinese-StopWords https://github.com/elephantnose/characters
    df = pd.read_csv(f"{mid}.csv",encoding='utf-8',on_bad_lines='skip', usecols=[3])#取第4列
    df_copy = df.copy()
    print(df)
    df_copy['comment'] = df_copy['评论内容'].apply(lambda x: str(x).split())  # 去掉空格
    print(df_copy)
    df_list = df_copy.values.tolist()
    comment = jieba.cut(str(df_list), cut_all=False)
    words = ' '.join(comment)
    # cloud_mask = np.array(Image.open("wangfei.jpg"))
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path=font,
                   stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    wc.generate(words)
    # image_colors = ImageColorGenerator(cloud_mask)#给词云上色
    # wc.recolor(color_func=image_colors)
    #看看词频高的有哪些,把无用信息去除 https://github.com/Brucepk/luoxiang/blob/master/bilibili_ciyun.py
    process_word = WordCloud.process_text(wc, words)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    print(sort[:50])
    wc.to_file(f"{mid}.jpg")
ip_detail('5000660202553386')
wordcloud_img('5000660202553386')