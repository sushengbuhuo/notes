import requests
import time
import json,html
import random,re,os,csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
requests.packages.urllib3.disable_warnings()
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
        'referer': 'https://mp.weixin.qq.com',
        # "Cookie": re.sub('(\s+)','=',re.sub('\n',';',cookies)),
    }
def replace_invalid_chars(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
    for char in invalid_chars:
        filename = filename.replace(char, ' ')
    return filename
def trimName(name):
    return name.replace(',', '，').replace('\u200b', ' ').replace('\u355b', ' ').replace('\u0488', ' ').replace('\u0488', ' ').replace('\n', ' ').replace('\r', ' ').replace('\r\n', ' ').replace('"', '“').replace('\t', ' ')
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def get_history():
    history = []
    with open('wechat_url.txt', 'a+') as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            history.append(line.strip())
    return history

def save_history(url):
    with open('wechat_url.txt', 'a+') as f:
        f.write(url.strip() + '\n')
urls_history = get_history()
contents = ""
nums = 0
encoding = 'utf-8-sig'
sname='公众号'
fname=f'{sname}数据'
urls=[]
# with open(f'{sname}.md', encoding='utf-8') as f:
#      contents = f.read()
# urls = re.findall('\]\((.*?)\)',contents)
# contents = ''
# with open(f'{sname}.txt', encoding='utf-8') as f:
#     contents = f.read()
# urls=contents.split('\n')
f = open(f'{sname}.csv', encoding='UTF8')
csv_reader = csv.reader(f)
print(len(urls))
with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章简介'+ ','+'文章作者'+','+'文章封面'+','+'是否原创'+ ','+'文章位置'+ ','+'是否付费'+','+'文章发布国家'+ ','+'文章发布省份'+ ','+'阅读数'+','+'在看数'+','+'点赞数'+','+'分享数'+ ','+'留言数'+ ','+'赞赏数'+','+'视频数'+ ','+'音频数'+'\n')
with open(f'{sname}留言数据.csv', 'a+', encoding='utf-8-sig', newline='') as ff:
    ff.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'评论昵称'+ ','+'评论内容'+','+'评论点赞数'+','+'留言回复'+','+'留言时间'+','+'国家'+','+'省份'+'\n')
def down(url,position,copyright,digest,is_pay):
    if url in urls_history:
       print('已经下载过：',url)
       return True
    response = requests.get(html.unescape(url), headers=headers)#, params={'key': '', 'uin': 'xx'}
    global nums
    encoding = 'utf-8-sig'
    is_down_view = 1
    is_down = 1
    is_down_video = 0
    is_down_audio = 0
    is_down_img = 0
    is_down_cover=0
    is_down_comment = 0
    pass_ticket = ""
    url_comment = 'https://mp.weixin.qq.com/mp/appmsg_comment'
    appmsg_token = "-JKIOE"
    key=""
    uin = "=="
    biz="=="
    content = response.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com').replace('因网络连接问题，剩余内容暂无法加载。', '')#+'<p style="display:none">下载作者：公众号苏生不惑 微信：sushengbuhuo</p>'
    try:
        # soup = BeautifulSoup(content, 'html.parser')
        # div_to_delete = soup.find('div', {'id': 'js_pc_qr_code'})
        # if div_to_delete:
        #     div_to_delete.extract()
        # content = soup.prettify()
        title = re.search(r'var msg_title = \'(.*)\'', content) or re.search(r'window.title = "(.*)"', content)
        ct = re.search(r'var ct = "(.*)";', content) or re.search(r"d\.ct = xml \? getXmlValue\('ori_create_time\.DATA'\) \: '(.*)'",content)
        author = re.search(r'<meta name="author" content="(.*)"\s?/>', content)
        cover = re.search(r'<meta property="og:image" content="(.*)"\s?/>', content).group(1)
        if not title:
           title = re.search(r'window\.msg_title = \'(.*?)\'', content)
        if not ct:
           ct = re.search(r'window\.ct = \'(.*?)\'', content)
        # print(cover,title,ct)
        title = title.group(1)
        ct = ct.group(1)
        author = author.group(1)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(ct)))# %H:%M:%S
        # if int(ct) > 1660321824:
        #     return False
        print('文章数量：',nums)
        print('文章链接：',url,date)
        nums = nums+1
        # copyright="否"
        # is_pay = '否'
        province_name = country_name = comments_html=''
        read_num,like_num,old_like_num,share_num,comments_num,reward_num,videos,audios='0','0','0','0','0','0','0','0'
        if is_down_view == 1:
            read_num,like_num,old_like_num,reward_num,share_num = view(url,appmsg_token,uin,key,pass_ticket)
            if read_num == "error":
            	print('获取阅读数失败',url)
            	return "error"
        if is_down == 1:
            try:
               country_name=re.search("countryName: '(.*?)'",content).group(1)
               province_name=re.search("provinceName: '(.*?)'",content).group(1)
            except Exception as e:
               pass
               # print('获取地区失败',e,url)
            # if '<div class="pay__qrcode-title">微信扫一扫付费阅读本文</div>' in content:
            #     is_pay = '是'
            #转载原创文章误判 读取txt才用
            # if 'xx' not in content:
        	#    print('过滤文章',url)
            #    return True
            #下载视频
            if is_down_video:
                try:
                    videos = video(content,headers,date,url,replace_invalid_chars(title))
                except Exception as e:
                    print('下载视频失败',e,url)
            #下载音频
            if is_down_audio:
                try:
                    audios = audio(content,headers,date,replace_invalid_chars(title))
                except Exception as e:
                    print('下载音频失败',e,url)
            # 下载封面
            if is_down_cover:
                if not os.path.exists('cover'):
                    os.mkdir('cover')
                try:
                    cover_data = requests.get(cover,headers=headers)
                    with open('cover/'+date+'_'+replace_invalid_chars(title)+'.jpg','wb') as f:
                        f.write(cover_data.content)
                except Exception as e:
                    print('下载封面失败',e,url)
            #下载图片
            if is_down_img:
                try:
                    image(response,headers,date,replace_invalid_chars(title))
                except Exception as e:
                    print('下载图片失败',e,url)
            if is_down_comment == 1:
                comments_num,comments_html = comments(content,date,headers,url_comment,biz,uin,key,pass_ticket,url)
                if comments_num == "error":
                    print('获取评论数失败',url)
                    return "error"
            # try:
            #      with open(date+'-'+replace_invalid_chars(title)+'.txt', 'a+', encoding='utf-8') as f:
            #         soup = BeautifulSoup(content, 'html.parser')
            #         contentSoup = soup.find("div", {"id": "js_content"})
            #         result_text = [line for line in contentSoup.get_text().splitlines() if line.strip()]
            #         # result_text = re.sub(r'\n+', '\n', soup.get_text())
            #         f.write('\n'.join(result_text)+ '\n\n'+ '\n\n')
            # except Exception as err:
            #     print('下载txt出错了',err,url)
            # try:
            #     with open(date+'-'+replace_invalid_chars(title)+'.html', 'w', encoding='utf-8') as f:
            #         f.write(content+comments_html)
            # except Exception as err:
            #     with open(date+'-'+str(random.randint(100,1000))+'.html', 'w', encoding='utf-8') as f:
            #         f.write(content+comments_html)
        with open(f'{fname}.md', 'a+', encoding='utf-8') as f2:
            f2.write('[{}]'.format(date+'_'+html.unescape(title)) + '({})'.format(url)+ '\n\n'+'文章简介:'+html.unescape(digest)+ '\n\n'+ '\n\n')
        with open(f'{fname}.txt', 'a+', encoding='utf-8') as f2:
            f2.write(url+ '\n')
        with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
            f.write(date+','+trimName(html.unescape(title)) + ','+url+ ','+trimName(html.unescape(digest))+ ','+trimName(html.unescape(author))+','+cover+','+copyright+ ','+position+ ','+is_pay+ ','+country_name+','+province_name+','+read_num+','+like_num+','+old_like_num+','+share_num+','+comments_num+ ','+reward_num+','+videos+','+audios+'\n')
        save_history(url)
        return True
    except Exception as e:
        print(e,url)#;raise Exception("抓取失败了："+url)
        with open(f'{sname}下载失败文章列表.csv', 'a+', encoding=encoding) as f6:
            f6.write(''+','+'' + ','+url+ ','+digest+ ','+''+','+''+',,'+copyright+ ','+position+ ','+is_pay+ ','+''+','+''+',0,0,0,0,0,0,0,0'+'\n')
        # with open(f'{sname}下载失败文章列表.txt', 'a+', encoding='utf-8') as f5:
            # f5.write(url+'\n')
def view(link,appmsg_token,uin,key,pass_ticket):
    # 获得mid,_biz,idx,sn 有些文章没有chksm参数http://mp.weixin.qq.com/s?__biz=MzA3NTcyNzY3OA==&mid=400102856&idx=1&sn=c0dab637c639b52d1d308d609bb270e1#rd
    # mid = link.split("&")[1].split("=")[1]
    # idx = link.split("&")[2].split("=")[1]
    # sn = link.split("&")[3].split("=")[1]
    # _biz = link.split("&")[0].split("_biz=")[1]
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    if not '__biz' in query_params:
        return 'error','0','0','0','0'
    __biz=query_params['__biz'][0]
    # 早期文章http://mp.weixin.qq.com/mp/appmsg/show?__biz=MjM5Nzg5OTk5NA==&appmsgid=10014557&itemidx=4&sign=4c61d5477f07877436cd04b18ec2c884#wechat_redirect
    if 'mid' in query_params:
        mid=query_params['mid'][0]
    if 'appmsgid' in query_params:
        mid=query_params['appmsgid'][0]
    if 'sn' in query_params:
        sn=query_params['sn'][0]
    if 'sign' in query_params:
        sn=query_params['sign'][0]
    if 'idx' in query_params:
        idx=query_params['idx'][0]
    if 'itemidx' in query_params:
        idx=query_params['itemidx'][0]
    if not mid or not sn or not __biz or not idx:
        return 'error','0','0','0','0'
    url = "http://mp.weixin.qq.com/mp/getappmsgext"#获取详情页
    
    cookies = """rewardsn   

    """
    headers = {
        "Cookie": re.sub('(\s+)','=',re.sub('\n',';',cookies)),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309001c) XWEB/6500"
    }
    data = {
        "is_only_read": "1",
        "is_need_reward": "1",
        "is_temp_url": "0",
        "appmsg_type": "9",
        'reward_uin_count': '0',
        # 'comment_id':'3190316509655433217'
        # 'vid':'wxv_3145693246921261058',
        # 'item_show_type':'5',
        # 'finder_export_id':'export/UzFfAgtgekIEAQAAAAAAYSg1SChmpgAAAAstQy6ubaLX4KHWvLEZgBPEiINUJm9aZK2GzNPgMIttAAqM1EV1ILMbcYvWHeA2',
    }
    params = {
        "__biz": __biz,
        "mid": mid,
        "sn": sn,
        "idx": idx,
        "key": key,
        "pass_ticket": pass_ticket,
        "appmsg_token": appmsg_token,
        "uin": uin,
        "wxtoken": "777",
        "f":"json",
        # "devicetype":"Windows10x64",
        # "clientversion":"63090719",
    }
    content = requests.post(url, headers=headers, data=data, params=params).json()
    # print(params,content,data)
    if not 'appmsgstat' in content:
    	return 'error','0','0','0','0'
    try:
        readNum = content["appmsgstat"]["read_num"]
    except:
        readNum = 0
    try:
        likeNum = content["appmsgstat"]["like_num"]
    except:
        likeNum = 0
    try:
        old_like_num = content["appmsgstat"]["old_like_num"]  
    except:
        old_like_num = 0
    reward_num = 0
    if 'reward_total_count' in content:
        reward_num = content['reward_total_count']
    share_num=content.get('appmsgstat').get('share_num',0)
    # 视频号文章 https://mp.weixin.qq.com/s/8yTuzaYWkiwJcHgLkBlaMA 
    # if 'finder_fav_num' in content["appmsgstat"]:
    #     likeNum = content["appmsgstat"]['finder_fav_num']
    # if 'finder_like_num' in content["appmsgstat"]:
    #     old_like_num = content["appmsgstat"]['finder_like_num']
    time.sleep(random.randint(1, 2))
    print("文章阅读数:"+str(readNum))
    print("文章在看数:"+str(likeNum))
    print("文章点赞数:"+str(old_like_num))
    print("文章赞赏数:"+str(reward_num))
    print("文章分享数:"+str(share_num))#,str(content['comment_count'])
    return str(readNum), str(likeNum),str(old_like_num),str(reward_num),str(share_num)
def video(content, headers,date,article_url,title):
    # vid = re.search(r'wxv_.{19}',res.text).group(0)
    # time.sleep(1) https://mp.weixin.qq.com/s/goqAKIypCsI4vVLjdhmXSg https://mp.weixin.qq.com/s/gAdGPFj0pomdKcE5s9-Gkw
    # print('视频id',vid) unescape(encodedString.replace(/\\x/g, "%")); 视频号 https://mp.weixin.qq.com/s/pl8y30DALob_bKQmbdXcnQ
    videos_snap = re.findall(r'var\s+video_snap_json\s+\=\s+"\{\\x22list\\x22:(.*?)\}"\s+\|\|\s+"";',content)
    videos = re.findall(r"source_link\: xml \? getXmlValue\(\'video_page_info\.source_link\.DATA\'\) : \'http://v\.qq\.com/x/page/(.*?)\.html\'\,",content)
    if not videos:
        videos = re.findall(r"source_link\: \'http://v\.qq\.com/x/page/(.*?)\.html\' \|\| \'\'\,",content)
    num = 0
    if videos_snap:
        num = len(json.loads(videos_snap[0].replace('\\x22', '"')))
    if not os.path.exists('video'):
        os.mkdir('video')
    for i in videos:
        num+=1
        print(f'腾讯视频地址：http://v.qq.com/x/page/{i}.html')
        with open('视频链接合集.txt','a+') as f6:
            f6.write(f'http://v.qq.com/x/page/{i}.html'+'\n')
        with open('视频链接合集.csv','a+') as f:
            f.write(date+','+title+','+f'http://v.qq.com/x/page/{i}.html'+','+article_url+'\n')
    vinfo = re.findall(r'window\.__mpVideoTransInfo\s+\=\s+([\s\S]*?)\];',content,flags=re.S)#匹配任意数量（包括零个）的任意字符，直到遇到下一个匹配项。这样的表达式通常用于匹配多行文本，包括换行符在内的所有内容。
    if not vinfo:
        vinfo = re.findall(r'mp_video_trans_info:\s+([\s\S]*?)\],',content,flags=re.S)
    if not vinfo:
        matches = re.search(r'var\s*videoPageInfos\s*=\s*(\[.*?\]);', content, re.DOTALL)
        if not matches:
            return str(num)
        json_array = matches.group(1)
        vinfo = re.findall(r'mp_video_trans_info:\s+([\s\S]*?)\],',json_array,flags=re.S) 
    if not vinfo:
        return str(num)
    for v in vinfo:
        v_url = re.search(r"url:\s+'(.*?)',",v)
        if not v_url:
            v_url = re.search(r"url:\s+\('(.*?)'\)",v)
        # print(v,v_url)
        if v_url:
            video_url = html.unescape(v_url.group(1).replace(r'\x26','&'));print('视频地址',video_url)
            # vids = list(set(vids)) #去重
            num+=1
            print('正在下载视频：'+replace_invalid_chars(title)+'.mp4')
            video_data = requests.get(video_url,headers=headers)
            with open('视频链接合集.csv','a+') as f4:
                f4.write(date+','+trimName(title)+','+video_url+','+article_url+'\n')
            with open('video/'+date+'_'+replace_invalid_chars(title)+'_'+str(num)+'.mp4','wb') as f:
                f.write(video_data.content)
    return str(num)
def audio2(content,headers,date,title):
    # aid = re.search(r'"voice_id":"(.*?)"',res.text).group(1)
    aids = re.findall(r'"voice_id":"(.*?)"',content)
    if not aids:
        aids = re.findall(r'voiceid\s*:\s*"(.*?)"',content)
    time.sleep(1)
    num = 0
    if not os.path.exists('audio'):
        os.mkdir('audio')
    for id in aids:
        num +=1
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
        audio_data = requests.get(url,headers=headers)
        print('正在下载音频：'+title+'.mp3')
        with open('audio/'+date+'___'+replace_invalid_chars(title)+'___'+str(num)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
    return str(num)
def audio(content,headers,date,title):
    matches = re.search(r'voiceList=(\{.*\})', content)
    if not matches:
        return '0'
    json_array = json.loads(matches.group(1))
    if not json_array['voice_in_appmsg']:
        return '0'
    # time.sleep(1)
    num = 0
    if not os.path.exists('audio'):
        os.mkdir('audio')
    for item in json_array['voice_in_appmsg']:
        num +=1
        aid=item['voice_id']
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={aid}'
        audio_data = requests.get(url,headers=headers)
        print('正在下载音频：'+title+'.mp3')
        with open('audio/'+date+'___'+replace_invalid_chars(title)+'___'+str(num)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
    return str(num)
def image(response,headers,date,title):
    imgs=re.findall('data-src="(.*?)"',response.text)
    imgs2= re.findall("cdn_url: '(.*?)',",response.text)
    imgs.extend(imgs2)
    time.sleep(1)
    num = 0
    if not os.path.exists('images'):
        os.mkdir('images')
    for i in imgs:
        if not re.match(r'^https?://.*',i):
            continue
        num+=1
        img_data = requests.get(i,headers=headers)
        print('正在下载图片：'+i)
        with open('images/'+date+'_'+replace_invalid_chars(title)+'_'+str(num)+'.jpg','wb') as f6:
            f6.write(img_data.content)
    return str(num)
def comments(content,date,headers,url_comment,biz,uin,key,pass_ticket,url):
    time.sleep(random.randint(1, 1))
    str_comment = re.search(r'var comment_id = "(.*)" \|\| "(.*)" \* 1;', content) or re.search(r"d\.comment_id = xml \? getXmlValue\('comment_id\.DATA'\) : '(.*)';", content)
    str_msg = re.search(r"var appmsgid = \"\" \|\| '' \|\| '(.*)'", content) or re.search(r"window.appmsgid = '(.*?)' \|\| '' \|\| '';", content)   or re.search(r"window.appmsgid = '' \|\| '(.*?)' \|\| '';", content)   or re.search(r"window.appmsgid = '' \|\| '' \|\| '(.*?)';", content)  or re.search(r"var appmsgid = \"(.*)\" \|\| '' \|\| '';",content)  or re.search(r"var appmsgid = \"\" \|\| '(.*)' \|\| '';",content)
    str_token = re.search(r'window\.appmsg_token = "(.*)";', content) or re.search(r'var appmsg_token = "(.*)";', content)
    str_title = re.search(r'var msg_title = \'(.*)\'', content) or re.search(r"window\.msg_title = '(.*)' \|\| '';", content)
    # print(str_comment,str_msg,str_token)
    comments_html = """
    <link rel="stylesheet" href="https://lovecn.github.io/wxMessage.css"><div class="discuss_container" id="js_cmt_main" style="display: block;">
<div class="mod_title_context">
<strong class="mod_title">精选留言</strong>
</div>
<div class="discuss_list_wrp">
<ul class="discuss_list" id="js_cmt_list">
"""
    if str_comment and str_msg and str_token:
        comment_id = str_comment.group(1)  # 评论id(固定)
        app_msg_id = str_msg.group(1)  # 票据id(非固定)
        appmsg_token = str_token.group(1)  # 票据token(非固定)
        title_article = str_title.group(1)
        rand_title = str(random.randint(1,10))
        data_comments = []
        comments_excel = []
        #https://github.com/happyjared/python-learning/blob/master/wechat/wx_mps.py
        # p/104318974 
        #抓包工具Charles安装 https://xie.infoq.cn/article/4cfb8c32a7bb9a4121390c2e6
        # comment_url = url_comment+'?action=getcomment&scene=0&__biz={0}&appmsgid={1}&idx=1&comment_id={2}&offset=0&limit=100&pass_ticket={3}&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token={4}&x5=1&f=json&uin={5}&key={6}'.format(biz, app_msg_id, comment_id,pass_ticket, app_msg_token,uin ,key)
        comment_url = url_comment+f'?action=getcomment&scene=0&appmsgid={app_msg_id}&idx=1&comment_id={comment_id}&offset=0&limit=100&send_time=&sessionid=1644213099&enterid=1644285387&uin={uin}&key={key}&pass_ticket={pass_ticket}&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6305002e&__biz={biz}&appmsg_token={appmsg_token}&x5=0&f=json'
        resp = requests.get(comment_url, headers=headers,verify=False).json()
        # ret, status = resp['base_resp']['ret'], resp['base_resp']['errmsg'];
        ret = resp['base_resp']['ret']
        # print(resp)
        if ret != 0 and ret != -2:
            print("评论接口",comment_url)
            return "error","status"
        if ret == 0:
            elected_comment = resp['elected_comment']
            comment_num = resp['elected_comment_total_cnt']
            print('评论数:',len(elected_comment),resp['elected_comment_total_cnt'])
            # with open(date+'_'+trimName(title_article)+'.csv', 'a+', encoding='utf-8') as f:
            #     f.write('评论时间'+','+'评论昵称' + ','+'评论内容'+ ','+'评论点赞数'+ '\n')
            for comment in elected_comment:
                comment_num+=comment.get('reply_new')['reply_total_cnt']
                nick_name = comment.get('nick_name')  # 昵称
                logo_url = comment.get('logo_url')  # 头像
                # comment_time = datetime.fromtimestamp(comment.get('create_time'))  # 评论时间
                comment_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.get('create_time')))
                content = comment.get('content')  # 评论内容
                content_id = comment.get('content_id')  # id
                like_num = comment.get('like_num')  # 点赞数
                reply_list = comment.get('reply_new')['reply_list']  # 回复数据
                ip_info = comment.get('ip_wording')
                province_name = country_name = ''
                if ip_info:
                	country_name = ip_info['country_name']
                	province_name = ip_info['province_name']
                reply_content = reply_list[0]['content'] if len(reply_list) > 0 else ''
                data_comments.append([comment_time,nick_name,content,like_num,reply_content])
                comments_excel.append([date,title_article,url,nick_name,content,like_num,reply_content,comment_time,country_name,province_name])
                # print(comment_time,nick_name,content,like_num)
                comments_html = comments_html + f'<li class="js_comment_item discuss_item"><div class="discuss_item_hd"><div class="user_info"><div class="nickname_wrp"><img class="avatar" src="{logo_url}"><strong class="nickname">{nick_name}        来自{country_name}---{province_name}   {comment_time}</strong></div></div></div><div class="discuss_message"><span class="discuss_status"></span><div class="discuss_message_content js_comment_content">{content}</div></div>'
                for reply in reply_list:
                    reply_nick_name = reply.get('nick_name')
                    reply_nick_content = reply.get('content')
                    reply_logo_url = reply.get('logo_url')
                    comments_html = comments_html + f'<div class="reply_result js_reply_item "><div class="discuss_item_hd"><div class="user_info author_info"><div class="nickname_wrp"><div class="nickname">{reply_nick_name}</div></div></div></div><div class="discuss_message"><div class="discuss_message_content js_reply_content">{reply_nick_content}</div></div></div>'
                comments_html = comments_html + '</li>'
                # try:
                #     with open(date+'_'+trimName(title_article)+'.csv', 'a+', encoding='utf-8') as f:
                #         f.write(comment_time+','+nick_name + ','+trimName(content)+ ','+str(like_num)+ '\n')
                # except Exception as err:
                #     print(err)
                #     with open(date+'_'+rand_title+'.csv', 'a+', encoding='utf-8') as f:
                #         f.write(comment_time+','+nick_name + ','+trimName(content)+ ','+str(like_num)+ '\n')
            # with open(date+'_'+trimName(title_article)+'.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
            #      writer = csv.writer(csvfile)
            #      writer.writerow(['评论时间','评论昵称','评论内容','评论点赞数','回复内容'])
            #      writer.writerows(data_comments)
            # dataframe = pandas.DataFrame(data_comments,columns=['评论时间','评论昵称','评论内容','评论点赞数','回复内容','评论发布国家','评论发布省份'])
            # dataframe.to_csv(date+'_'+trimName(title_article)+'.csv',encoding='utf_8_sig',index=False)
            comments_html = comments_html + '</ul></div></div>'
            with open(f'{sname}留言数据.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(comments_excel)
            return str(comment_num),comments_html
        return '0',''
    return '0',''
for line in csv_reader:
    if line[2] == "文章链接":
        continue
    res = down(line[2],line[8],line[7],line[3],line[9])
    time.sleep(random.randint(1, 1))
    if not res:
       continue
    if res == "error":
       break
for item in urls:
    res = down(item,'1','','','')
    time.sleep(random.randint(1, 1))
    if not res:
       continue
    if res == "error":
       break