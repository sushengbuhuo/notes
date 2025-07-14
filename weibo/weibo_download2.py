import requests,re,os,time,html,sys,csv
import random
import traceback,urllib3
from os.path import basename
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
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
cookie = input('请输入微博cookie:')
url=input('请输入微博链接:') #https://weibo.com/1744395855/OykWZj6Zt  https://weibo.com/1744395855/O0haQaIfE
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://weibo.com/1744395855/NkD5bjvPC',
        "Cookie":cookie,
    }
if not cookie or not url:
	print('输入为空')
	sys.exit(1)
if int(time.time()) > 1753979775:
	print('未知错误')
	sys.exit(1)
m=re.search(r'https://(www\.)?weibo\.com/\d+/(.*)',url).group(2)
mid=reverse_cut_to_length(m, base62_decode, 4, 7)
url=f'https://weibo.com/ajax/statuses/show?id={mid}&locale=zh-CN&isGetLongText=true'#https://www.weibo.com/ajax/statuses/extend?id=5049927780796644
res = requests.get(html.unescape(url),proxies={'http': None,'https': None},verify=False, headers=headers).json()

dt_obj = datetime.strptime(res['created_at'], '%a %b %d %H:%M:%S %z %Y')
if not os.path.exists(f'image'):
    os.mkdir(f'image')
if not os.path.exists(f'video'):
    os.mkdir(f'video')
if 'pic_infos' in res:
    for j,k in res['pic_infos'].items():
        print('图片:',k['largest']['url'])
        img_data = requests.get(k['largest']['url'].replace('/large/','/oslarge/'),headers=headers,timeout=5)
        with open('image/'+dt_obj.strftime('%Y-%m-%d')+mid+j+'.jpg','wb') as f2:
            f2.write(img_data.content)
if 'page_info' in res and 'media_info' in res.get('page_info') and 'playback_list' in res.get('page_info').get('media_info'):
    video_url = res.get('page_info').get('media_info').get('playback_list')[0]['play_info']['url']
    title=res.get('page_info').get('media_info').get('name')+res.get('page_info').get('object_id')
    print('视频:',video_url)
    video_data = requests.get(video_url,headers=headers,verify=False,timeout=10)
    with open(f'video/'+dt_obj.strftime('%Y-%m-%d')+replace_invalid_chars(title)+'.mp4','wb') as f5:
        f5.write(video_data.content)
