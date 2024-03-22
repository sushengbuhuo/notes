import requests
import time
import json,html
import random,re,os,csv
requests.packages.urllib3.disable_warnings()
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
msg_url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
Cookie = ""
headers = {
    "Cookie": Cookie,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44",
}
# https://github.com/YPstar-yes/Crawl-WeChat-articles/blob/master/weixin.py
token = ""#动态 people/bai-ri-meng-yu-shi-76 
fakeid = "=="#公众号id ==
msg_type = '101_1'
count=5
nums =1
is_down = 0
is_down_view = 0
is_down_video = 0
is_down_audio = 0
is_down_img = 0
is_down_cover=0
is_down_comment = 0
is_down_copyright = 0
pass_ticket = "EKEY0ZN+/PIsHv2mSivGJ9AHKnN2SFbyC5q40PeeZWAgtl8HXGw=="
url_comment = 'https://mp.weixin.qq.com/mp/appmsg_comment'
appmsg_token = "-"
key=""
uin = ""
biz=fakeid
def down(offset, fakeid, uin, key,pass_ticket,appmsg_token):
    params = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "sub": "list",
        "free_publish_type": "1",
        "sub_action": "list_ex",
        "begin": offset,
        "count": count,
        "query": "",
        "fakeid": fakeid,
        "type": msg_type,
    }
    global nums
    fname = ''
    encoding = 'utf-8-sig'
    result = requests.get(msg_url, headers=headers, params=params, verify=False).json()
    # print(result)
    time.sleep(random.randint(4, 5))
    if  result['base_resp']['err_msg'] != 'ok':
        print("出错了",result,params)
        return True
    if len(result['publish_page']) == 0:
        print("done")
        return True
    articles = json.loads(result['publish_page'])
    if len(articles['publish_list']) == 0:
        print("done")
        return True
    print('文章位置',offset)
    if offset == 0:
        with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
            f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章简介'+ ','+'文章作者'+','+'文章封面'+','+'原文链接'+','+'是否原创'+ ','+'文章位置'+ ','+'是否付费'+','+'文章发布国家'+ ','+'文章发布省份'+ ','+'文章类型'+ ','+'是否删除'+ ','+'粉丝数'+ ','+'阅读数'+','+'在看数'+','+'点赞数'+ ','+'留言数'+ ','+'赞赏数'+','+'视频数'+ ','+'音频数'+'\n')
        # with open('文章留言数据.csv', 'a+', encoding='utf-8-sig', newline='') as ff:
            # ff.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'评论昵称'+ ','+'评论内容'+','+'评论点赞数'+','+'留言回复'+','+'留言时间'+','+'国家'+','+'省份'+'\n')
    for publish_list in articles['publish_list']:
        try:
            if not publish_list['publish_info']:
                continue
            publish_info = json.loads(publish_list['publish_info'])
            article_type = '发布'
            fans = 0
            msg_fail_reason = ''
            fail = 0
            delete_status = '否'
            print('文章信息',publish_info.items())
            if publish_info['type'] == 9:
                article_type = '群发'
                # 正常2 自己删除7 被举报违规8 未发送成功违规6
                if publish_info['sent_result']['msg_status'] ==2:
                    fans = publish_info['sent_status']['total']
                elif publish_info['sent_result']['msg_status'] ==7 or publish_info['sent_result']['msg_status'] ==8:
                    fans = publish_info['sent_status']['total']
                    # msg_fail_reason = publish_info['sent_result']['msg_fail_reason']
                elif publish_info['sent_result']['msg_status'] == 6:
                    # msg_fail_reason = publish_info['sent_result']['msg_fail_reason']
                    fail = 1
            for item in publish_info['appmsgex']:
                try:
                    # if item['update_time'] > 1645113602:
                    #     continue
                    # if item['update_time'] < 1672329600:
                    #     return True
                    print('文章数量',nums)
                    if nums > 5:
                       return True
                    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['update_time'])) # %H:%M:%S
                    title = item['title']
                    link = html.unescape(item['link'])
                    nums = nums+1
                    if is_down_copyright == 1 and item['copyright_type'] != 1:
                       print('过滤链接',link,date)
                       continue
                    print('文章链接',link,date)
                    copyright="否"
                    is_pay = '否'
                    author=item['author_name']
                    if item['is_deleted'] or fail == 1:
                        delete_status = "是"
                    province_name = country_name = comments_html=''
                    read_num,like_num,old_like_num,comments_num,reward_num,videos,audios='0','0','0','0','0','0','0'
                    if is_down_view == 1:
                        read_num,like_num,old_like_num,reward_num = view(link,appmsg_token,uin,key,pass_ticket)
                        if read_num == "error":
                            print('获取阅读数失败',link)
                            return True
                    if is_down == 1:
                        res = requests.get(link,proxies={'http': None,'https': None},verify=False, headers=headers)
                        content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com').replace('因网络连接问题，剩余内容暂无法加载。', '')+'<p style="display:none">下载作者：公众号苏生不惑 微信：sushengbuhuo</p>'
                        if is_down_comment == 1:
                            try:
                                comments_num,comments_html = comments(content,date,headers,url_comment,biz,uin,key,pass_ticket,link)
                            except Exception as e:
                                print('获取评论数失败',e,link)
                        try:
                            with open(date+'-'+trimName(item['title'])+'.html', 'w', encoding='utf-8') as f:
                                f.write(content+comments_html)
                        except Exception as err:
                            with open(date+'-'+str(random.randint(1,100))+'.html', 'w', encoding='utf-8') as f:
                                f.write(content+comments_html)
                        try:
                           country_name=re.search("countryName: '(.*?)'",content).group(1)
                           province_name=re.search("provinceName: '(.*?)'",content).group(1)
                           author = re.search(r'<meta name="author" content="(.*)"\s?/>', content).group(1)
                        except Exception as e:
                           pass
                        # if '<div class="pay__qrcode-title">微信扫一扫付费阅读本文</div>' in content:
                        #     is_pay = '是'
                    if item['copyright_type'] == 1:
                        copyright="是"
                    if item['is_pay_subscribe'] == 1:
                        is_pay="是"
                    #下载视频
                    if is_down_video:
                        try:
                            videos = video(res,headers,date,link,trimName(item['title']))
                        except Exception as e:
                            print('下载视频失败',e,link)
                    #下载音频
                    if is_down_audio:
                        try:
                            audios = audio(res,headers,date,trimName(item['title']))
                        except Exception as e:
                            print('下载音频失败',e,link)
                    #下载图片
                    if is_down_img:
                        try:
                            imgs(res.text,headers,date,trimName(item['title']))
                        except Exception as e:
                            print('下载图片失败',e,link)
                    #下载封面
                    if is_down_cover:
                        if not os.path.exists('cover'):
                            os.mkdir('cover')
                        try:
                            img_data = requests.get(item['cover'],verify=False, headers=headers)
                            with open('cover/'+date+'___'+trimName(item['title'])+'___'+trimName(item['digest'])+'.jpg','wb') as f6:
                                f6.write(img_data.content)
                        except Exception as e:
                            print('下载封面失败',e,link)
                    with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
                        f.write(date+','+trimName(item['title']) + ','+link+ ','+trimName(html.unescape(item['digest']))+ ','+author+','+item['cover']+','+''+','+copyright+ ','+str(item['itemidx'])+ ','+is_pay+ ','+country_name+','+province_name+','+article_type+','+delete_status+','+str(fans)+','+read_num+','+like_num+','+old_like_num+','+comments_num+ ','+reward_num+','+videos+','+audios+'\n')
                    with open(f'{fname}.md', 'a+', encoding='utf-8') as f2:
                        f2.write('[{}]'.format(date+'_'+item['title']) + '({})'.format(link)+ '\n\n'+'文章简介:'+html.unescape(item['digest'])+ '\n\n'+'文章作者:'+author+ '\n\n')
                    with open(f'{fname}.txt', 'a+', encoding='utf-8') as f3:
                        f3.write(link+'\n')
                except Exception as e:
                    print('publish_info错误信息',e);raise Exception(e)
        except Exception as err:
            print('publish_list错误信息',err);raise Exception(err)
    down(offset + count, fakeid, uin, key,pass_ticket,appmsg_token) 
def view(link,appmsg_token,uin,key,pass_ticket):
    # 获得mid,_biz,idx,sn
    mid = link.split("&")[1].split("=")[1]
    idx = link.split("&")[2].split("=")[1]
    sn = link.split("&")[3].split("=")[1]
    _biz = link.split("&")[0].split("_biz=")[1]
    url = "http://mp.weixin.qq.com/mp/getappmsgext"#获取详情页
    cookies = """appmsg_token   1250_6m0ocoY9nl4o2x32keziDa0Y2iBCt-5Z3p0NdsbWpu586MdzrewB-lB0I7uP0Vc0VrOOUTQSm2UsMEhn
rewardsn    
wxtokenkey  777
wxuin   647940102
devicetype  Windows10x64
version 6309080f
lang    zh_CN
pass_ticket Yl721JVL1gPqAK4B1s2yjxtIDo/e+5Xg7cfxBWRRUMoSuxu0h5GL74KFMFmQeTb9IMxm1tuziK2NbhGMVLMn/A==
wap_sid2    CIaQ+7QCEooBeV9IUGZZM1U5aW9kT3pvVWE0N2dfcWRPa2VEZHVROHpSWnk2ZEFUbkFyUUUwOGxFYWo5bHBEaFdxazBacDFaTWt5aEtDcjByNmcwLU9EYzQ2cVRGdjJwMmZVUjg3N3gtbk9kV3VvcEpQbGZGZmVmdTlTOWppYThEMU1Fbkl3SzMzR1I4QVNBQUF+MODOzqwGOA1AAQ==
    """
    headers = {
        "Cookie": re.sub('(\s+)','=',re.sub('\n',';',cookies)),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309001c) XWEB/6500"
    }
    data = {
        "is_only_read": "1",
        "is_temp_url": "0",
        "appmsg_type": "9",
        'reward_uin_count': '0'
    }
    params = {
        "__biz": _biz,
        "mid": mid,
        "sn": sn,
        "idx": idx,
        "key": key,
        "pass_ticket": pass_ticket,
        "appmsg_token": appmsg_token,
        "uin": uin,
        "wxtoken": "777",
    }

    content = requests.post(url, headers=headers, data=data, params=params).json()
    # print(params,content,content["appmsgstat"]["read_num"], content["appmsgstat"]["like_num"])
    if not 'appmsgstat' in content:
        return 'error','0','0','0'
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
    time.sleep(random.randint(1, 3))
    print("阅读数:"+str(readNum))
    print("点赞数:"+str(likeNum))
    print("在看数:"+str(old_like_num))
    return str(readNum), str(likeNum),str(old_like_num),str(reward_num)
def video(res, headers,date,article_url,title):
    # vid = re.search(r'wxv_.{19}',res.text).group(0)
    time.sleep(1)
    # print('视频id',vid)
    vids = re.findall(r'vid=(wxv_\d{19})',res.text)
    videos = re.findall(r"source_link\: xml \? getXmlValue\(\'video_page_info\.source_link\.DATA\'\) : \'http://v\.qq\.com/x/page/(.*?)\.html\'\,",res.text)
    num = 0
    if not os.path.exists('video'):
        os.mkdir('video')
    for i in videos:
        num+=1
        print(f'腾讯视频地址：http://v.qq.com/x/page/{i}.html')
        with open('视频链接合集.txt','a+') as f6:
            f6.write(f'http://v.qq.com/x/page/{i}.html'+'\n')
        with open('视频链接合集.csv','a+') as f:
            f.write(date+','+title+','+f'http://v.qq.com/x/page/{i}.html'+','+article_url+'\n')
    for vid in vids:
        num+=1
        # vid = vid.group(0)
        print('视频id',vid)
        url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
        data = requests.get(url,headers=headers,timeout=1).json()
        video_url = data['url_info'][0]['url']
        # video_data = requests.get(video_url,headers=headers)
        with open('视频链接合集.txt','a+') as f5:
            f5.write(video_url+'\n')
        with open('视频链接合集.csv','a+') as f2:
            f2.write(date+','+trimName(data['title'])+','+video_url+','+article_url+'\n')
        print('正在下载视频：'+trimName(data['title'])+'.mp4')
        # with open('video/'+date+'_'+trimName(data['title'])+'.mp4','wb') as f:
            # f.write(video_data.content)
    return str(num)

def audio(res,headers,date,title):
    # aid = re.search(r'"voice_id":"(.*?)"',res.text).group(1)
    aids = re.findall(r'"voice_id":"(.*?)"',res.text)
    time.sleep(1)
    num = 0
    if not os.path.exists('audio'):
        os.mkdir('audio')
    for id in aids:
        num +=1
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
        audio_data = requests.get(url,headers=headers)
        print('正在下载音频：'+title+'.mp3')
        with open('audio/'+date+'___'+trimName(title)+'___'+str(num)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
    return str(num)
def imgs(content,headers,date,title):
    imgs=re.findall('data-src="(.*?)"',content)
    time.sleep(1)
    num = 0
    if not os.path.exists('imgs'):
        os.mkdir('imgs')
    for i in imgs:
        num+=1
        img_data = requests.get(i,headers=headers)
        print('正在下载图片：'+i)
        with open('imgs/'+date+'___'+title+'___'+str(num)+'.jpg','wb') as f6:
            f6.write(img_data.content)
    return str(num)
def comments(content,date,headers,url_comment,biz,uin,key,pass_ticket,url):
    str_comment = re.search(r'var comment_id = "(.*)" \|\| "(.*)" \* 1;', content) or re.search(r"d.comment_id = xml \? getXmlValue\('comment_id.DATA'\) : '(.*)';", content)
    str_msg = re.search(r"var appmsgid = \"\" \|\| '' \|\| '(.*)'", content) or re.search(r"window.appmsgid = '' \|\| '' \|\| '(.*)';", content)  or re.search(r"var appmsgid = \"(.*)\" \|\| '' \|\| '';",content)
    str_token = re.search(r'window.appmsg_token = "(.*)";', content)
    str_title = re.search(r'var msg_title = \'(.*)\'', content) or re.search(r"window.msg_title = '(.*)' \|\| '';", content)
    comments_html = """
    <link rel="stylesheet" href="https://kbtxwer.gitee.io/wxMessage.css"><div class="discuss_container" id="js_cmt_main" style="display: block;">
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
        ret, status = resp['base_resp']['ret'], resp['base_resp']['errmsg']
        if ret != 0 and ret != -2:
            print("评论接口",comment_url)
            return '0',''
        if ret == 0 or status == 'ok':
            elected_comment = resp['elected_comment']
            print('评论数:',len(elected_comment))
            # with open(date+'_'+trimName(title_article)+'.csv', 'a+', encoding='utf-8') as f:
            #     f.write('评论时间'+','+'评论昵称' + ','+'评论内容'+ ','+'评论点赞数'+ '\n')
            for comment in elected_comment:
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
                comments_html = comments_html + f'<li class="js_comment_item discuss_item"><div class="discuss_item_hd"><div class="user_info"><div class="nickname_wrp"><img class="avatar" src="{logo_url}"><strong class="nickname">{nick_name}        来自{country_name}---{province_name}</strong></div></div></div><div class="discuss_message"><span class="discuss_status"></span><div class="discuss_message_content js_comment_content">{content}</div></div>'
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
            # with open('公众好文章留言数据.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
            #     writer = csv.writer(csvfile)
            #     writer.writerows(comments_excel)
            return str(len(elected_comment)),comments_html
        return '0',''
    return '0',''
down(0,fakeid,uin,key,pass_ticket,appmsg_token)