import requests,pdfkit,json,time,datetime,os,re,html,pandas,csv
from random import randint
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pass_ticket = 'UdslZ/Gnj6CVrNquCj9u91JYifUEq9DcoY7Wu7Hku4eOxc8O1HneQ39tkBKcGUn+'
app_msg_token = '1101_AOA3GqTDgjbfQwvJHH300bQWMJlT-3kgEn2eJQ~~'
biz = 'MzIyMjg2ODExMA=='
uin = 'MTU0MTQzNjQwMw=='
key = 'c2f41d68125c239d35862f0f09c748e1e470ff8df134638ee863b470d9edfb55a74d5c2cea3e95d5dfb1b586185bc73f649639e84565b45bd1991be8b00cc72ebf8ebefa8f91dd4805b047f51da7b8dc2b94e949fb881f9056d3ee193a0f051c29bd356f1d63d0b331a044b793623ed7a2f99c7b4421515c69f0d1e84b3e3fbc'
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
    # print(param)
    response = requests.get(url, headers=headers, params=param, proxies=proxies)
    response_dict = response.json()
    # print(response_dict)
    next_offset = response_dict['next_offset']
    print(offset,next_offset)
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
    htmls = []
    encoding = 'utf-8-sig'
    is_down = 1
    is_down_video = 0
    is_down_audio = 0
    is_down_view = 0
    is_down_cover = 0
    is_down_img = 0
    is_down_comment = 1
    is_all = 1
    fname = '2022公众号历史文章列表'
    #csv gbk编码问题'gbk'，建议使用utf-8 codec can't encode character '\u200b' in position 293: illegal multibyte sequence wechat=pd.read_csv('公众号历史文章列表.csv',encoding='utf-8')
    #wechat=pd.read_csv('2021刘备我祖公众号历史文章列表.csv',encoding='utf-8',on_bad_lines='skip')
    #wechat.to_csv('2021刘备我祖公众号历史文章列表2.csv',encoding='utf_8_sig',index=False)
    if offset == 0:
        with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
            f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章简介'+ ','+'文章作者'+','+'文章封面'+','+'原文链接'+','+'是否原创'+ ','+'文章位置'+ ','+'阅读数'+','+'在看数'+','+'点赞数'+ ','+'评论数'+'\n')
    # if offset:
    #     can_msg_continue = 0
    #     return True
    # print(data_list)
    for data in data_list:
        try:
            # 文章发布时间 如何爬取微信公众号的所有文章https://xuzhougeng.top/archives/wechatarticleparseri %Y-%m-%d %H:%M:%S
            date = time.strftime('%Y-%m-%d', time.localtime(data['comm_msg_info']['datetime']))
            # if data['comm_msg_info']['datetime'] > 1643644804:
            #     continue
            if data['comm_msg_info']['datetime'] < 1640966400:
                can_msg_continue = 0
                return True
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
                    if child['content_url'] and is_all:
                        if is_down:
                            res = requests.get(child['content_url'],proxies={'http': None,'https': None},verify=False, headers=headers)
                            content = res.text.replace('data-src', 'src')
                            # #生成HTML 文件名不能有\/:*?"<>| 
                            try:
                                with open(date+'_'+trimName(child['title'])+'.html', 'w', encoding='utf-8') as f:
                                    f.write(content)
                            except Exception as err:
                                with open(date+'_'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                                    f.write(content)
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
                                video(res,headers)
                            except Exception as e:
                                print(e)
                        #下载音频
                        if is_down_audio:
                            try:
                                audio(res,headers,date,trimName(child['title']))
                            except Exception as e:
                                print(e)
                        #下载图片
                        if is_down_img:
                            try:
                                imgs(res.text,headers,date,position)
                            except Exception as e:
                                print(e)
                        #下载封面
                        if is_down_cover:
                            try:
                                img_data = requests.get(child['cover'],verify=False, headers=headers)
                                with open(date+'_____'+trimName(child['title'])+'_____'+trimName(child['digest'])+'.jpg','wb') as f6:
                                    f6.write(img_data.content)
                            except Exception as e:
                                print(e)
                        try:
                            read_num,like_num,old_like_num,comments_num='0','0','0','0'
                            if is_down_view == 1:
                                read_num,like_num,old_like_num = view(html.unescape(child['content_url']))
                            if is_down_comment == 1:
                            	comments_num = comments(res.text,date,headers,url_comment,biz,uin,key,pass_ticket)
                        except Exception as e:
                            read_num,like_num,old_like_num,comments_num='0','0','0','0'
                        copyright = '否'
                        if child['copyright_stat'] == 11:
                            copyright = '是'
                        # print(read_num,like_num,old_like_num,child['content_url'])
                        with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
                            f.write(date+','+trimName(child['title']) + ','+html.unescape(child['content_url'])+ ','+trimName(child['digest'])+ ','+child['author']+','+child['cover']+','+child['source_url']+','+copyright+ ','+str(position)+ ','+read_num+','+like_num+','+old_like_num+','+comments_num+'\n')
                        with open(f'{fname}.md', 'a+', encoding='utf-8') as f2:
                            f2.write('[{}]'.format(date+'_'+child['title']) + '({})'.format(html.unescape(child['content_url']))+ '\n\n'+'文章简介:'+child['digest']+ '\n\n'+'文章作者:'+child['author']+ '\n\n')
                        with open(f'{fname}.txt', 'a+', encoding='utf-8') as f3:
                            f3.write(html.unescape(child['content_url'])+'\n')
                #文章摘要digest
                #文章封面cover
                if url:
                    if is_down:
                        res = requests.get(url,proxies={'http': None,'https': None},verify=False, headers=headers)
                        content = res.text.replace('data-src', 'src')
                        #生成HTML
                        # try:
                        #     with open(date+'_'+trimName(title)+'.html', 'w', encoding='utf-8') as f:
                        #         f.write(content)
                        # except Exception as err:
                        #     with open(date+'_'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                        #         f.write(content)
                        #生成PDF
                        # try:
                        #    pdfkit.from_string(content,'./' + date + '_' + title.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.pdf')
                        # except Exception as err:
                        #    print(err)
                        # print(url + title + date + '成功')
                    # with open(f'{fname}.txt', 'a+', encoding=encoding) as f:
                        # f.write(title +'\n')
                    #获取阅读数在看数点赞数
                    try:
                        read_num,like_num,old_like_num,comments_num='0','0','0','0'
                        if is_down_view == 1:
                            read_num,like_num,old_like_num = view(html.unescape(url))
                        if is_down_comment == 1:
                        	comments_num = comments(res.text,date,headers,url_comment,biz,uin,key,pass_ticket)
                    except Exception as e:
                        read_num,like_num,old_like_num,comments_num='0','0','0','0'
                    #下载视频
                    if is_down_video:
                        try:
                            video(res,headers)
                        except Exception as e:
                            print(e)
                    #下载音频
                    if is_down_audio:
                        try:
                            audio(res,headers,date,trimName(title))
                        except Exception as e:
                            print(e)
                    #下载图片
                    if is_down_img:
                        try:
                            imgs(res.text,headers,date,position,trimName(title))
                        except Exception as e:
                            print(e)
                    #下载封面
                    if is_down_cover:
                        try:
                            img_data = requests.get(msg_info['cover'],verify=False, headers=headers)
                            with open(date+'_____'+trimName(title)+'_____'+trimName(msg_info['digest'])+'.jpg','wb') as f7:
                                f7.write(img_data.content)
                        except Exception as e:
                            print(e)
                    copyright = '否'
                    if msg_info['copyright_stat'] == 11:
                        copyright = '是'
                    #csv
                    with open(f'{fname}.csv', 'a+', encoding=encoding) as f:
                        f.write(date+','+trimName(title) + ','+html.unescape(url)+ ','+trimName(msg_info['digest'])+','+ msg_info['author'] +','+msg_info['cover']+','+msg_info['source_url']+ ','+copyright+ ','+'1'+ ','+read_num+','+like_num+','+old_like_num+ ','+comments_num+'\n')
                    #生成markdown
                    with open(f'{fname}.md', 'a+', encoding='utf-8') as f2:
                        # f.write('文章标题:'+date+'_'+title + '文章链接'+url+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面图地址:'+msg_info['cover']+ '\n')
                        f2.write('[{}]'.format(date+'_'+title) + '({})'.format(html.unescape(url))+ '\n\n'+'文章简介:'+msg_info['digest']+ '\n\n'+'文章作者:'+msg_info['author']+ '\n\n')
                        
                        # f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n\n'+'简介:'+msg_info['digest']+ '\n\n'+'封面图地址:'+msg_info['cover']+ '\n\n')
                        # f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面:'+'![{}]'.format(title) + '({})'.format(msg_info['cover'])+ '\n')
                    with open(f'{fname}.txt', 'a+', encoding='utf-8') as f3:
                         f3.write(html.unescape(url)+'\n')
                    #生成Word 
                    #end
                
                
        except Exception as err:
            print('错误信息',err)
    if can_msg_continue == 1:
        down(next_offset,biz,uin,key,pass_ticket)
        return True
    else:
        print('done')
        return False
def view(url):
    # with open('公众号文章.txt', 'a', encoding='utf-8') as f3:
        # f3.write(content +'\n')
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
    appmsg_token='1151_SzVftkrTg7cXXXJ%2Ft-H06ZklVy3tdMUBtOm5eo_DwdK2DIyzTn-_xJ88HSBXrz_Rr0hegCOFDoAF7Y4c'
    headers = {
    "Cookie": 'pgv_pvid=3462479730;sd_userid=26861634200545809;sd_cookie_crttime=1634200545809;tvfe_boss_uuid=2462cb91e2efc262;ua_id=BbSW7iXpRV9kLjy3AAAAAJnbZGccv_XAw3N3660mGLU=;pac_uid=0_d6687c556b618;wxuin=1541436403;lang=zh_CN;rewardsn=;wxtokenkey=777;appmsg_token=1151_SzVftkrTg7cXXXJ%2Ft-H06ZklVy3tdMUBtOm5eo_DwdK2DIyzTn-_xJ88HSBXrz_Rr0hegCOFDoAF7Y4c;devicetype=Windows10x64;version=6305002e;pass_ticket=UdslZ/Gnj6CVrNquCj9u91JYifUEq9DcoY7Wu7Hku4eOxc8O1HneQ39tkBKcGUn+;wap_sid2=CPPngd8FEp4BeV9ITTFBSEd5ak5JU1FvSzhQdWZOSW82N2pHdFk1SFRmc1dIcmF5MFYtQUtkQmxSV1ZneW55SW1Idjdsd2pGZXV2UGp4YXI1UmhjcTlvWWRLS3hlRnJhSUZPSjZmd1hIMERseGZMdDFoNkp3RS1sa0RQQ0pGdmZBazZUZmh2V0l6WVlTVlZTZk9fWEJ2THBreGRPX2tMV0FoZEVnQUEwkOKIkAY4DUAB;',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)"
    }
    origin_url = "https://mp.weixin.qq.com/mp/getappmsgext?"
    appmsgext_url = origin_url + "__biz={}&mid={}&sn={}&idx={}&appmsg_token={}&x5=1".format(biz, mid, sn, idx, appmsg_token)
    res = requests.post(appmsgext_url, headers=headers, data=data).json()
    print(appmsgext_url,res)
    return str(res["appmsgstat"]["read_num"]), str(res["appmsgstat"]["like_num"]), str(res["appmsgstat"]["old_like_num"])
def video(res, headers):
    vid = re.search(r'wxv_.{19}',res.text).group(0)
    time.sleep(2)
    if vid:
        url = f'https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&vid={vid}'
        data = requests.get(url,headers=headers).json()
        video_url = data['url_info'][0]['url']
        video_data = requests.get(video_url,headers=headers)
        print('正在下载视频：'+trimName(data['title'])+'.mp4')
        with open(trimName(data['title'])+'.mp4','wb') as f4:
            f4.write(video_data.content)

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
        with open(date+'___'+title+'.mp3','wb') as f5:
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
def comments(content,date,headers,url_comment,biz,uin,key,pass_ticket):
    str_comment = re.search(r'var comment_id = "(.*)" \|\| "(.*)" \* 1;', content)
    str_msg = re.search(r"var appmsgid = \"\" \|\| '' \|\| '(.*)'", content)
    str_token = re.search(r'window.appmsg_token = "(.*)";', content)
    str_title = re.search(r'var msg_title = \'(.*)\'', content)
    if str_comment and str_msg and str_token:
        comment_id = str_comment.group(1)  # 评论id(固定)
        app_msg_id = str_msg.group(1)  # 票据id(非固定)
        appmsg_token = str_token.group(1)  # 票据token(非固定)
        title_article = str_title.group(1)
        rand_title = str(randint(1,10))
        data_comments = []
        #https://github.com/happyjared/python-learning/blob/master/wechat/wx_mps.py
        #https://zhuanlan.zhihu.com/p/104318974 https://github.com/JustDoPython/python-100-day
        #抓包工具Charles安装https://xie.infoq.cn/article/4cfb8c32a7bb9a4121390c2e6
        # comment_url = url_comment+'?action=getcomment&scene=0&__biz={0}&appmsgid={1}&idx=1&comment_id={2}&offset=0&limit=100&pass_ticket={3}&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token={4}&x5=1&f=json&uin={5}&key={6}'.format(biz, app_msg_id, comment_id,pass_ticket, app_msg_token,uin ,key)
        comment_url = url_comment+f'?action=getcomment&scene=0&appmsgid={app_msg_id}&idx=1&comment_id={comment_id}&offset=0&limit=100&send_time=&sessionid=1644213099&enterid=1644285387&uin={uin}&key={key}&pass_ticket={pass_ticket}&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6305002e&__biz={biz}&appmsg_token={appmsg_token}&x5=0&f=json'
        resp = requests.get(comment_url, headers=headers,verify=False).json()
        ret, status = resp['base_resp']['ret'], resp['base_resp']['errmsg']
        if ret == 0 or status == 'ok':
            elected_comment = resp['elected_comment']
            print('评论数:',len(elected_comment),comment_url)
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
                reply_content = reply_list[0]['content'] if len(reply_list) > 0 else ''
                data_comments.append([comment_time,nick_name,content,like_num,reply_content])
                print(comment_time,nick_name,content,like_num)
                
                # try:
                #     with open(date+'_'+trimName(title_article)+'.csv', 'a+', encoding='utf-8') as f:
                #         f.write(comment_time+','+nick_name + ','+trimName(content)+ ','+str(like_num)+ '\n')
                # except Exception as err:
                #     print(err)
                #     with open(date+'_'+rand_title+'.csv', 'a+', encoding='utf-8') as f:
                #         f.write(comment_time+','+nick_name + ','+trimName(content)+ ','+str(like_num)+ '\n')
            with open(date+'_'+trimName(title_article)+'.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
                 writer = csv.writer(csvfile)
                 writer.writerow(['评论时间','评论昵称','评论内容','评论点赞数','回复内容'])
                 writer.writerows(data_comments)
            # dataframe = pandas.DataFrame(data_comments,columns=['评论时间','评论昵称','评论内容','评论点赞数'])
            # dataframe.to_csv(date+'_'+trimName(title_article)+'.csv',encoding='utf_8_sig',index=False)
            return str(len(elected_comment))
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
down(0,biz,uin,key,pass_ticket)#设置一个offset取之前数据