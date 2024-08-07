import re,requests,time,json,csv,sys,random,os,calendar
from lxml import etree
from collections import OrderedDict
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
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
def url_to_mid(url: str):
    result = reverse_cut_to_length(url, base62_decode, 4, 7)
    return int(result)

def mid_to_url(mid_int: int):
    result = reverse_cut_to_length(mid_int, base62_encode, 7, 4)
    return result
def get_weibo(id,headers):
        url = "https://m.weibo.cn/detail/%s" % id
        html = requests.get(url, headers=headers, verify=False).text
        html = html[html.find('"status":') :]
        html = html[: html.rfind('"call"')]
        html = html[: html.rfind(",")]
        html = "{" + html + "}"
        js = json.loads(html, strict=False)
        weibo_info = js.get("status")
        weibo = dict()
        if weibo_info:
            weibo = parse_weibo(weibo_info)
        return weibo

def parse_weibo(weibo_info):
        weibo = dict()
        if weibo_info["user"]:
            weibo["user_id"] = weibo_info["user"]["id"]
            weibo["screen_name"] = weibo_info["user"]["screen_name"]
        else:
            weibo["user_id"] = ""
            weibo["screen_name"] = ""
        weibo["id"] = weibo_info["id"]
        weibo["bid"] = 'https://weibo.com/'+str(weibo["user_id"])+'/'+weibo_info["bid"]
        text_body = weibo_info["text"]
        selector = etree.HTML(text_body)
        remove_html_tag=1
        if remove_html_tag:
            weibo["text"] = selector.xpath("string(.)")
        else:
            weibo["text"] = text_body
        weibo["pics"] = get_pics(weibo_info)
        weibo["created_at"] = datetime.strptime(weibo_info["created_at"].replace("+0800 ", ""), "%c").strftime("%Y-%m-%d %H:%M:%S")
        weibo["source"] = weibo_info["source"]
        weibo["attitudes_count"] = weibo_info.get("attitudes_count", 0)
        weibo["comments_count"] = weibo_info.get("comments_count", 0)
        weibo["reposts_count"] = weibo_info.get("reposts_count", 0)
        weibo["reads_count"] = weibo_info.get("reads_count", 0)
        weibo["region_name"] = weibo_info.get("region_name", "")
        weibo["full_created_at"] = weibo_info["created_at"]
        return weibo

def get_pics(weibo_info):
        if weibo_info.get("pics"):
            pic_info = weibo_info["pics"]
            pic_list = [pic["large"]["url"] for pic in pic_info]
            pics = ",".join(pic_list)
        else:
            pics = ""
        return pics
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ').replace('"', '“')
def down():
    with open('微博数据.csv', 'a+', encoding='utf-8-sig', newline='') as f:
        f.write('微博链接'+','+'微博昵称' +','+'微博mid' + ','+'微博uid'+ ','+'微博日期'+ ','+'微博内容'+','+'微博转发数'+','+'微博评论数'+','+'微博点赞数'+'\n')
    filename = input("请输入微博链接文件名:")
    cookie = input("请输入微博cookie:")
    headers = {"User_Agent": user_agent,'cookie':cookie}
    contents = ''
    with open(filename, encoding='utf-8') as f:
        contents = f.read()
    if not contents:
        sys.exit('文件内容为空')
    urls = contents.split('\n')
    res=[]
    for i in urls:
        if i == '':
            continue
        try:
            mid=''
            if i.startswith('https://weibo.com'):
                mid = re.search(r'https?://weibo\.com/\d+/(.*)\?*', i).group(1)
                #转换 兼容
                if not mid.isdigit():
                    mid=url_to_mid(mid)
            else:
                mid = re.search(r'https?://m\.weibo\.cn/(status|\d+)/(\d+)\?*', i).group(2)
            if not mid:
                continue
            weibo=get_weibo(mid,headers)
            print('开始抓取微博内容：',i,mid)
            time.sleep(random.randint(1, 3))
            if not weibo:
                res.append([i,'x','x','x','x','x','x','x','x'])
            else:
                res.append([i,weibo['screen_name'],'\t'+str(weibo['id']),'\t'+str(weibo['user_id']),weibo['created_at'],weibo['text'],weibo['reposts_count'],weibo['comments_count'],weibo['attitudes_count']])
        except Exception as e:
            print("出错了",i,e)
            res.append([i,'x','x','x','x','x','x','x','x'])
    with open('微博数据.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(res)
with open('微博.csv', 'a+', encoding='utf-8-sig', newline='') as f:
    # f.write('链接'+','+'平台' +','+'日期' + ','+'标题'+ ','+'阅读数'+ ','+'转发数'+','+'评论数'+','+'点赞数'+'\n')
    f.write('微博链接'+','+'mid'+','+'微博类型' +','+'微博内容'+ ','+'图片链接'+ ','+'发布来源'+ ','+'发布地区'+ ','+'发布时间' + ','+'阅读数'+ ','+'转发数'+','+'评论数'+','+'点赞数'+'\n')
def get_cookie():
    cookie = ''
    if os.path.exists('cookie.txt'):
        with open('cookie.txt', encoding='utf-8') as f:
            cookie = f.read().replace('\n','')
    return cookie
cookie = get_cookie()
print('本工具更新于2024年8月1日,获取最新版本关注公众号苏生不惑')
if not cookie:
    cookie=input('请输入微博cookie:')
headers = {"User_Agent": user_agent,'cookie':cookie}
url='https://www.weibo.com/ajax/profile/detail'
res=requests.get(url, headers=headers, verify=False,timeout=5).json()
if not res['data']['created_at']:
    sys.exit(1)
myuid=re.search(r'.*\?uid=(\d+)',res['data']['verified_url']).group(1)
month = 6
uid=input('请输入微博uid:')
if uid != "" and uid != myuid:
    month = 1
if not uid:
    uid=myuid

# print(uid,month)
def timeAgo(day):
    current_date = datetime.now()
    months_ago = current_date - timedelta(days=day)
    months_ago_first_day = months_ago.replace(day=1)
    return months_ago_first_day.strftime("%Y-%m-%d %H:%M:%S")
def data(uid,page,since_id,month):
    url =f'https://www.weibo.com/ajax/statuses/mymblog?uid={uid}&page={page}&feature=0&since_id={since_id}'
    # print(f'开始第{page}页',url)
    res=requests.get(url, headers=headers, verify=False,timeout=5).json()
    if not res["data"]['list']:
        return False
    try:
        t = int(time.mktime(datetime.strptime(res["data"]['list'][0]['created_at'], "%a %b %d %H:%M:%S %z %Y").timetuple()))
        months_ago_first_day = timeAgo(month*30)
        date_object = datetime.strptime(months_ago_first_day, "%Y-%m-%d %H:%M:%S")
        # date_object = datetime.fromtimestamp(int(date_object.timestamp()))
        # print(months_ago_first_day,time.strftime('%Y-%m-%d', time.localtime(int(date_object.timestamp()))))
        if t < int(date_object.timestamp()):
            return False
        for v in res["data"]['list']:
            if 'deleted' in v and v['deleted'] == 1:
                continue
            parsed_datetime = datetime.strptime(v['created_at'], "%a %b %d %H:%M:%S %z %Y")
            formatted_datetime = parsed_datetime.strftime("%m月%d日")
            timestamp = int(time.mktime(parsed_datetime.timetuple()))
            if timestamp < int(date_object.timestamp()):
                continue
            print(parsed_datetime.strftime("%Y-%m-%d %H:%M:%S"),v['mid'],v['text_raw'])
            soup = BeautifulSoup(v['source'], 'html.parser')
            pics=''
            if v['pic_num'] > 0:
                for j,k in v['pic_infos'].items():
                    pics+=k['largest']['url'].replace('/large/','/oslarge/')+';'
            weibo_type='原创'
            if 'retweeted_status' in v:
                weibo_type='转发'
            if v['user']['idstr'] != uid:
                weibo_type='快转'
            with open('微博.csv', 'a+', encoding='utf-8-sig', newline='') as f:
                # f.write('https://m.weibo.cn/detail/'+v['mid']+','+'微博'+','+formatted_datetime +','+trimName(v['text_raw']) +','+str(v['reads_count']) + ','+str(v['reposts_count'])+ ','+str(v['comments_count'])+ ','+str(v['attitudes_count'])+'\n')
                f.write(f'https://www.weibo.com/{uid}/'+v['mblogid']+','+v['mid']+','+weibo_type+','+trimName(v['text_raw']) +','+pics+','+soup.get_text()+','+v.get('region_name','')+','+parsed_datetime.strftime("%Y-%m-%d %H:%M") +','+str(v.get('reads_count',0)) + ','+str(v['reposts_count'])+ ','+str(v['comments_count'])+ ','+str(v['attitudes_count'])+'\n')
        if res["data"]['since_id'] == 0:
            return False
        time.sleep(random.randint(2, 6))
        page+=1
        data(uid,page,res["data"]['since_id'],month)
    except Exception as e:
        print('error',e)
data(uid,1,'',month)