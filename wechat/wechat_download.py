import requests,pdfkit,json,time,datetime,os,re,html,pandas,csv
from random import randint
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pass_ticket = '04ed0rTsxg2MkarlY0DcE0dk2vpdT42TMfZJn86CGsOAX1m8/5Ybj8fmBKBH23w0'
app_msg_token = '1101_AOA3GqTDgjbfQwvJHH300bQWMJlT-3kgEn2eJQ~~'
biz = ''
uin = ''
key = ''
nums = 1
def down(offset, biz, uin, key,pass_ticket):
    url = "https://mp.weixin.qq.com/mp/profile_ext"
    url_comment = 'https://mp.weixin.qq.com/mp/appmsg_comment'
    url_info = 'https://mp.weixin.qq.com/mp/getappmsgext'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
    proxies = {
        'https': None,
        'http': None,
    }
    param = {
        'action': 'getmsg',
        '__biz': biz,
        'f': 'json',
        'offset': offset,
        'count': '10',
        'is_ok': '1',
        'scene': '124',
        'uin': uin,
        'key': key,
        'wxtoken': '',
        'x5': '0',
    }

    response = requests.get(url, headers=headers, params=param, proxies=proxies)
    response_dict = response.json()
    # print(response_dict)
    next_offset = response_dict['next_offset']
    print('抓取位置',offset,next_offset)
    can_msg_continue = response_dict['can_msg_continue']
    general_msg_list = response_dict['general_msg_list']
    data_list = json.loads(general_msg_list)['list']
    # if data_list[0]['comm_msg_info']['datetime'] < 1600418023:
    #     can_msg_continue = 0
    #     return True
    # with open(f'{offset}.json', 'a+', encoding='utf-8') as f:
    #     f.write(response.text)
    # return True
    time.sleep(2)
    htmls = [];global nums
    encoding = 'utf-8-sig'
    is_down = 0
    is_down_video = 0
    is_down_audio = 0
    is_down_view = 0
    is_down_cover = 0
    is_down_img = 0
    is_down_comment = 0
    is_all = 1
    fname = '公众号历史文章'
    #csv gbk编码问题'gbk'，建议使用utf-8 codec can't encode character '\u200b' in position 293: illegal multibyte sequence wechat=pd.read_csv('公众号历史文章列表.csv',encoding='utf-8',error_bad_lines=False) For Pandas < 1.3.0
    #wechat=pd.read_csv('2021刘备我祖公众号历史文章列表.csv',encoding='utf-8',on_bad_lines='skip')
    #wechat.to_csv('2021刘备我祖公众号历史文章列表2.csv',encoding='utf_8_sig',index=False)
    if offset == 0:
        with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
            f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章简介'+ ','+'文章作者'+','+'文章封面'+','+'原文链接'+','+'是否原创'+ ','+'文章位置'+ ','+'是否付费'+','+'文章发布国家'+ ','+'文章发布省份'+ ','+'阅读数'+','+'在看数'+','+'点赞数'+ ','+'留言数'+'\n')
        # with open('历史文章留言数据.csv', 'a+', encoding='utf-8-sig', newline='') as ff:
        	# ff.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'评论昵称'+ ','+'评论内容'+','+'评论点赞数'+','+'留言回复'+','+'留言时间'+','+'国家'+','+'省份'+'\n')
    # if offset:
    #     can_msg_continue = 0
    #     return True
    # print(data_list)
    for data in data_list:
        try:
            # 文章发布时间 如何爬取微信公众号的所有文章https://xuzhougeng.top/archives/wechatarticleparseri %Y-%m-%d %H:%M:%S
            date = time.strftime('%Y-%m-%d', time.localtime(data['comm_msg_info']['datetime']))
            # if data['comm_msg_info']['datetime'] > 1656604800:
            #     continue
            # if data['comm_msg_info']['datetime'] < 1656645639:
            #     can_msg_continue = 0
            #     return True
            msg_info = data['app_msg_ext_info']
            #原创 Python 也可以分析公众号https://cloud.tencent.com/developer/article/1698155
            # if msg_info['copyright_stat'] == 11:
            if msg_info:
                # 文章标题
                title = msg_info['title']
                # 头条文章链接 如果删了为空
                url = msg_info['content_url']
                #次条文章数组字段解释https://zhuanlan.zhihu.com/p/104318974 is_multi=1有多篇文章 https://github.com/5zjk5/gongzonghao/blob/master/code/analysic.py https://python123.io/python/muxiatong/5dd14d1b71efdc10be55ee22
                child_msg_info = msg_info['multi_app_msg_item_list']
                # print(msg_info)
                # exit(1)
                # child_msg_info = []
                position = 1
                for child in child_msg_info:
                    position+=1
                    if child['content_url'] and is_all:# and child['copyright_stat'] == 11:
                        print('文章链接',html.unescape(child['content_url']))
                        comments_html = ''
                        province_name = country_name = ''
                        is_pay = '否'
                        print('文章数量',nums)
                        # if nums > 365:
                        #    can_msg_continue = 0
                        #    return True
                        try:
                            read_num,like_num,old_like_num,comments_num='0','0','0','0'
                            if is_down_view == 1:
                                read_num,like_num,old_like_num = view(html.unescape(child['content_url']))
                        except Exception as e:
                            print('获取阅读数失败',e,child['content_url'])
                            read_num,like_num,old_like_num,comments_num='0','0','0','0'
                        if is_down:
                            res = requests.get(child['content_url'],proxies={'http': None,'https': None},verify=False, headers=headers)
                            content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')+'<p style="display:none">下载作者：公众号苏生不惑 微信：sushengbuhuo</p>'
                            try:
                               country_name=re.search("countryName: '(.*?)'",content).group(1)
                               province_name=re.search("provinceName: '(.*?)'",content).group(1)
                            except Exception as e:
                               pass
                            # if 'xxx' not in content and 'xxx' not in content:
                            #     continue
                            # if '壁纸' not in child['title']:
                            #     continue
                            if is_down_comment == 1:
                            	try:
                            		comments_num,comments_html = comments(res.text,date,headers,url_comment,biz,uin,key,pass_ticket,html.unescape(child['content_url']))
                            	except Exception as e:
                            		print('获取评论数失败',e,child['content_url'])
                            	# print(comments_num,comments_html)
                            if '<div class="pay__qrcode-title">微信扫一扫付费阅读本文</div>' in content:
                               is_pay = '是'
                            # #生成HTML 文件名不能有\/:*?"<>| 
                            try:
                                with open(date+'-'+trimName(child['title'])+'.html', 'w', encoding='utf-8') as f:
                                    f.write(content+comments_html)
                            except Exception as err:
                                with open(date+'-'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                                    f.write(content+comments_html)
                            #生成PDF
                            # try:
                            #    pdfkit.from_string(content,'./' + date + '_' + child['title'].replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.pdf')
                            # except Exception as err:
                            #    print(err)
                            # print(url + child['title'] + date + '成功')
                        # with open(f'{fname}.txt', 'a+', encoding=encoding) as f:
                            # f.write(title + '\n')
                        #下载视频
                        if is_down_video:
                            try:
                                video(res,headers,date)
                            except Exception as e:
                                print('下载视频失败',e,child['content_url'])
                        #下载音频
                        if is_down_audio:
                            try:
                                audio(res,headers,date,trimName(child['title']))
                            except Exception as e:
                                print('下载音频失败',e,child['content_url'])
                        #下载图片
                        if is_down_img:
                            try:
                                imgs(res.text,headers,date,position,trimName(child['title']))
                            except Exception as e:
                                print('下载图片失败',e,child['content_url'])
                        #下载封面
                        if is_down_cover:
                            try:
                                img_data = requests.get(child['cover'],verify=False, headers=headers)
                                with open(date+'_____'+trimName(child['title'])+'_____'+trimName(child['digest'])+'.jpg','wb') as f6:
                                    f6.write(img_data.content)
                            except Exception as e:
                                print('下载封面失败',e,child['content_url'])
                        
                        copyright = '否'
                        if child['copyright_stat'] == 11:
                            copyright = '是'
                        # print(read_num,like_num,old_like_num,child['content_url'])
                        nums = nums+1
                        with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
                            f.write(date+','+trimName(child['title']) + ','+html.unescape(child['content_url'])+ ','+trimName(child['digest'])+ ','+trimName(child['author'])+','+child['cover']+','+child['source_url'].replace(',', '，')+','+copyright+ ','+str(position)+ ','+is_pay+ ','+country_name+','+province_name+','+read_num+','+like_num+','+old_like_num+','+comments_num+'\n')
                        with open(f'{fname}.md', 'a+', encoding='utf-8') as f2:
                            f2.write('[{}]'.format(date+'_'+child['title']) + '({})'.format(html.unescape(child['content_url']))+ '\n\n'+'文章简介:'+child['digest']+ '\n\n'+'文章作者:'+child['author']+ '\n\n')
                        with open(f'{fname}.txt', 'a+', encoding='utf-8') as f3:
                            f3.write(html.unescape(child['content_url'])+'\n')
                #文章摘要digest
                #文章封面cover
                if url:#  and msg_info['copyright_stat'] == 11:
                    #获取阅读数在看数点赞数
                    print('文章链接',html.unescape(url))
                    comments_html = ''
                    province_name = country_name = ''
                    is_pay = '否'
                    print('文章数量',nums)
                    # if nums > 365:
                    #    can_msg_continue = 0
                    #    return True
                    try:
                        read_num,like_num,old_like_num,comments_num='0','0','0','0'
                        if is_down_view == 1:
                            read_num,like_num,old_like_num = view(html.unescape(url))
                    except Exception as e:
                        print('获取阅读数失败',e,url)
                        read_num,like_num,old_like_num,comments_num='0','0','0','0'
                    if is_down:
                        res = requests.get(url,proxies={'http': None,'https': None},verify=False, headers=headers)
                        content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')+'<p style="display:none">下载作者：公众号苏生不惑 微信：sushengbuhuo</p>'
                        try:
                        	country_name=re.search("countryName: '(.*?)'",content).group(1)
                        	province_name=re.search("provinceName: '(.*?)'",content).group(1)
                        except Exception as e:
                        	pass
                        # if 'xxx' not in content and 'xxx' not in content:
                        #     continue
                        # if '壁纸' not in title:
                        #     continue
                        if is_down_comment == 1:
                        	try:
                        		comments_num,comments_html = comments(res.text,date,headers,url_comment,biz,uin,key,pass_ticket,html.unescape(url))
                        	except Exception as e:
                        		print('获取评论数失败',e,url)
                        	# print(comments_num,comments_html)
                        if '<div class="pay__qrcode-title">微信扫一扫付费阅读本文</div>' in content:
                            is_pay = '是'
                        #生成HTML
                        try:
                            with open(date+'-'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
                                f.write(content+comments_html)
                        except Exception as err:
                            with open(date+'-'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                                f.write(content+comments_html)
                        #生成PDF
                        # try:
                        #    pdfkit.from_string(content,'./' + date + '_' + title.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.pdf')
                        # except Exception as err:
                        #    print(err)
                        # print(url + title + date + '成功')
                    # with open(f'{fname}.txt', 'a+', encoding=encoding) as f:
                        # f.write(title +'\n')
                    
                    #下载视频
                    if is_down_video:
                        try:
                            video(res,headers,date)
                        except Exception as e:
                            print('下载视频失败',e,url)
                    #下载音频
                    if is_down_audio:
                        try:
                            audio(res,headers,date,trimName(title))
                        except Exception as e:
                            print('下载音频失败',e,url)
                    #下载图片
                    if is_down_img:
                        try:
                            imgs(res.text,headers,date,position,trimName(title))
                        except Exception as e:
                            print('下载图片失败',e,url)
                    #下载封面
                    if is_down_cover:
                        try:
                            img_data = requests.get(msg_info['cover'],verify=False, headers=headers)
                            with open(date+'_____'+trimName(title)+'_____'+trimName(msg_info['digest'])+'.jpg','wb') as f7:
                                f7.write(img_data.content)
                        except Exception as e:
                            print('下载封面失败',e,url)
                    copyright = '否'
                    if msg_info['copyright_stat'] == 11:
                        copyright = '是'
                    nums = nums+1;
                    #csv
                    with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
                        f.write(date+','+trimName(title) + ','+html.unescape(url)+ ','+trimName(msg_info['digest'])+','+ trimName(msg_info['author']) +','+msg_info['cover']+','+msg_info['source_url'].replace(',', '，')+ ','+copyright+ ','+'1'+ ','+is_pay+ ','+country_name+','+province_name+','+read_num+','+like_num+','+old_like_num+ ','+comments_num+'\n')
                    #生成markdown
                    with open(f'{fname}.md', 'a+', encoding='utf-8') as f2:
                        # f.write('文章标题:'+date+'_'+title + '文章链接'+url+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面图地址:'+msg_info['cover']+ '\n')
                        f2.write('[{}]'.format(date+'_'+title) + '({})'.format(html.unescape(url))+ '\n\n'+'文章简介:'+msg_info['digest']+ '\n\n'+'文章作者:'+msg_info['author']+ '\n\n')
                        # f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面:'+'![{}]'.format(title) + '({})'.format(msg_info['cover'])+ '\n')
                    with open(f'{fname}.txt', 'a+', encoding='utf-8') as f3:
                         f3.write(html.unescape(url)+'\n')
                    #生成Word 
                    #end
                # return True
            
        except Exception as err:
            print('错误信息',err)
    # return True
    if can_msg_continue == 1:
        down(next_offset,biz,uin,key,pass_ticket)
        return True
    else:
        print('done')
        return False
def view(url):
    # biz=re.search('var biz = "" \|\| "(.*?)"\;',content,re.M).group(1)
    biz=re.search('biz=(.*?)&',url).group(1)
    sn=re.search('sn=(.*?)&',url).group(1)
    mid=re.search('mid=(.*?)&',url).group(1)
    idx=re.search('idx=(.*?)&',url).group(1)
    time.sleep(2)
    data = {
    "is_only_read": "1",
    "is_temp_url": "0",                
    "appmsg_type": "9", # https://www.its203.com/article/wnma3mz/78570580 https://github.com/wnma3mz/wechat_articles_spider
    }
    #appmsg_token和cookie变化
    appmsg_token='1184_9a6un5aIzuaPPMVFm1AyNA61cYROciaRIjeMBneateinBPbxQ3IdRm2-rbCnQUPmYUq5XvoAEU1uBDTo'
    headers = {
    "Cookie": 'rewardsn=;wxtokenkey=777;wxuin=1541436403;devicetype=Windows10x64;version=6307062c;lang=zh_CN;pass_ticket=p4SXc5aL71p5rr64zaCA5s1oIQYMb3HOcavGxSmuAb5CmE1OGH/ob3/ohnhwqDAr;appmsg_token=1184_9a6un5aIzuaPPMVFm1AyNA61cYROciaRIjeMBneateinBPbxQ3IdRm2-rbCnQUPmYUq5XvoAEU1uBDTo;wap_sid2=CPPngd8FEooBeV9IRW1wM2Y4NDNoTUxGZ3l3ay1DOHFMbW03a0ZENlQxTi14ektCaUY3OHRjcHJ3eUtiTHQ1eWw2OVphTkM0eFNjSE5NS1dRTzNjRnZ2dU5GbVdFbzRGRVp5OF8yTTY5eDhJZi1fREUweUt2YTNJQVQ2ZFhfMnYwQzBlU1c0WGoxNzBYMFNBQUF+MLagq5kGOA1AAQ==;',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)"
    }
    origin_url = "https://mp.weixin.qq.com/mp/getappmsgext?"
    appmsgext_url = origin_url + "__biz={}&mid={}&sn={}&idx={}&appmsg_token={}&x5=1".format(biz, mid, sn, idx, appmsg_token)
    res = requests.post(appmsgext_url, headers=headers, data=data).json()
    print('阅读数',res["appmsgstat"]["read_num"])
    return str(res["appmsgstat"]["read_num"]), str(res["appmsgstat"]["like_num"]), str(res["appmsgstat"]["old_like_num"])
def video(res, headers,date):
    vid = re.search(r'wxv_.{19}',res.text).group(0)
    time.sleep(2)
    print('视频id',vid)
    if vid:
        url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
        data = requests.get(url,headers=headers,timeout=1).json()
        video_url = data['url_info'][0]['url']
        # video_data = requests.get(video_url,headers=headers,timeout=1)
        print('正在下载视频：'+trimName(data['title'])+'.mp4')
        with open('视频链接合集.csv','a+') as f4:
            f4.write(date+','+trimName(data['title'])+','+video_url+'\n')
        with open('视频链接合集.txt','a+') as f5:
            f5.write(video_url+'\n')
        # with open(date+'___'+trimName(data['title'])+'.mp4','wb') as f4:
            # f4.write(video_data.content)

def audio(res,headers,date,title):
    # aid = re.search(r'"voice_id":"(.*?)"',res.text).group(1)
    aids = re.findall(r'"voice_id":"(.*?)"',res.text)
    time.sleep(2)
    tmp = 0
    for id in aids:
        tmp +=1
        url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
        audio_data = requests.get(url,headers=headers)
        print('正在下载音频：'+title+'.mp3')
        with open(date+'___'+trimName(title)+'___'+str(tmp)+'.mp3','wb') as f5:
            f5.write(audio_data.content)
def imgs(content,headers,date,position,title):
    imgs=re.findall('data-src="(.*?)"',content)
    time.sleep(2)
    num = 0
    for i in imgs:
        num+=1
        img_data = requests.get(i,headers=headers)
        print('正在下载图片：'+i)
        with open(date+'___'+title+'___'+str(position)+'___'+str(num)+'.jpg','wb') as f6:
            f6.write(img_data.content)
def comments(content,date,headers,url_comment,biz,uin,key,pass_ticket,url):
    str_comment = re.search(r'var comment_id = "(.*)" \|\| "(.*)" \* 1;', content) or re.search(r"d.comment_id = xml \? getXmlValue\('comment_id.DATA'\) : '(.*)';", content)
    str_msg = re.search(r"var appmsgid = \"\" \|\| '' \|\| '(.*)'", content) or re.search(r"window.appmsgid = '' \|\| '' \|\| '(.*)';", content)
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
        rand_title = str(randint(1,10))
        data_comments = []
        comments_excel = []
        #https://github.com/happyjared/python-learning/blob/master/wechat/wx_mps.py
        #https://zhuanlan.zhihu.com/p/104318974 https://github.com/JustDoPython/python-100-day
        #抓包工具Charles安装https://xie.infoq.cn/article/4cfb8c32a7bb9a4121390c2e6
        # comment_url = url_comment+'?action=getcomment&scene=0&__biz={0}&appmsgid={1}&idx=1&comment_id={2}&offset=0&limit=100&pass_ticket={3}&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token={4}&x5=1&f=json&uin={5}&key={6}'.format(biz, app_msg_id, comment_id,pass_ticket, app_msg_token,uin ,key)
        comment_url = url_comment+f'?action=getcomment&scene=0&appmsgid={app_msg_id}&idx=1&comment_id={comment_id}&offset=0&limit=100&send_time=&sessionid=1644213099&enterid=1644285387&uin={uin}&key={key}&pass_ticket={pass_ticket}&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6305002e&__biz={biz}&appmsg_token={appmsg_token}&x5=0&f=json'
        resp = requests.get(comment_url, headers=headers,verify=False).json()
        ret, status = resp['base_resp']['ret'], resp['base_resp']['errmsg']
        # print(comment_url)
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
            # with open('文章留言数据.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
            #     writer = csv.writer(csvfile)
            #     writer.writerows(comments_excel)
            return str(len(elected_comment)),comments_html
        return '0',''
    return '0',''
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
down(0,biz,uin,key,pass_ticket)#设置一个offset取之前数据