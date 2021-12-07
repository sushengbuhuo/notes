import requests,pdfkit,json,time,datetime,os,re,html
from random import randint
import traceback
pass_ticket = 'zFEbbhJChxULq08vTWCQuVPe9nbv78Az7RapqXMzD0J/hHPc7G6Y6RNM8iNvMaE1'
app_msg_token = '1101_AOA3GqTDgjbfQwvJHH300bQWMJlT-3kgEn2eJQ~~'
biz = 'MzIxNDA0MTExMg=='
uin = 'MTU0MTQzNjQwMw=='
key = '0ade026c69fdcfd58ccda92337c0749890c53129b044fa86636de3e60121eef280648df16265e4aa61362377e1f8f73e5f4622c52eb49070a4ca323b56ef10b6c2e790ff34ce0edef41593a4c0572463c64fa11e8a90466fb13a8e7dc638f7785b14e9979061c86c5c3a3b9d2ade107f528b32af86addfd7e8649aa3133dcfdb'
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
    print(response_dict)
    next_offset = response_dict['next_offset']
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
    is_down = 1
    # print(data_list)
    for data in data_list:
        try:
            # 文章发布时间 如何爬取微信公众号的所有文章https://xuzhougeng.top/archives/wechatarticleparseri
            date = time.strftime('%Y-%m-%d', time.localtime(data['comm_msg_info']['datetime']))
            # if data['comm_msg_info']['datetime'] > 1622531305:
            #     continue
            # if data['comm_msg_info']['datetime'] < 1633242094:
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
                for child in child_msg_info:
                    if child['content_url']:
                        if is_down:
                            res = requests.get(child['content_url'],proxies={'http': None,'https': None},verify=False, headers=headers)
                            content = res.text.replace('data-src', 'src')
                            # #生成HTML 文件名不能有\/:*?"<>| 'gbk' codec can't encode character '\u200b' in position 293: illegal multibyte sequence
                            # try:
                            #     with open(date+'_'+child['title'].replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.html', 'w', encoding='utf-8') as f:
                            #         f.write(content)
                            # except Exception as err:
                            #     with open(date+'_'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                            #         f.write(content)
                            #生成PDF
                            # try:
                            #    pdfkit.from_string(content,'./' + date + '_' + child['title'].replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.pdf')
                            # except Exception as err:
                            #    print(err)
                            # print(url + child['title'] + date + '成功')
                        # with open('广东画院公众号文章列表.txt', 'a+', encoding='gbk') as f:
                            # f.write(title + '\n')
                        try:
                            read_num,like_num,old_like_num = view(content,html.unescape(child['content_url']))
                        except Exception as e:
                            read_num,like_num,old_like_num='0','0','0'
                        # print(read_num,like_num,old_like_num,child['content_url'])
                        with open('深圳卫健委公众号文章列表.csv', 'a+', encoding='gbk') as f:
                            f.write(date+','+child['title'] + ','+html.unescape(child['content_url'])+ ','+child['digest'].replace('\n', ' ').replace('\r', ' ')+ ','+read_num+','+like_num+','+old_like_num+'\n')
                        # with open('深圳卫健委公众号文章列表.md', 'a+', encoding='utf-8') as f2:
                            # f2.write('[{}]'.format(date+'_'+child['title']) + '({})'.format(html.unescape(child['content_url']))+ '\n\n'+'文章简介:'+child['digest']+ '\n\n'+'文章作者:'+child['author']+ '\n\n')
                            # f.write(html.unescape(child['content_url'])+'\n')
                #文章摘要digest
                #文章封面cover
                if url:
                    if is_down:
                        res = requests.get(url,proxies={'http': None,'https': None},verify=False, headers=headers)
                        content = res.text.replace('data-src', 'src')
                        #生成HTML
                        # try:
                        #     with open(date+'_'+title.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.html', 'w', encoding='utf-8') as f:
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
                    # with open('广东画院公众号文章列表.txt', 'a+', encoding='gbk') as f:
                        # f.write(title +'\n')
                    #获取阅读数在看数点赞数
                    try:
                        read_num,like_num,old_like_num = view(content,html.unescape(url))
                    except Exception as e:
                        read_num,like_num,old_like_num='0','0','0'
                    #csv
                    with open('深圳卫健委公众号文章列表.csv', 'a+', encoding='gbk') as f:
                        f.write(date+','+title + ','+html.unescape(url)+ ','+msg_info['digest'].replace('\n', ' ').replace('\r', ' ')+ ','+read_num+','+like_num+','+old_like_num+ '\n')
                    #生成markdown
                    # with open('深圳卫健委公众号文章列表.md', 'a+', encoding='utf-8') as f2:
                        # f.write('文章标题:'+date+'_'+title + '文章链接'+url+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面图地址:'+msg_info['cover']+ '\n')
                        # f2.write('[{}]'.format(date+'_'+title) + '({})'.format(html.unescape(url))+ '\n\n'+'文章简介:'+msg_info['digest']+ '\n\n'+'文章作者:'+msg_info['author']+ '\n\n')
                        # f.write(html.unescape(url)+'\n')
                        # f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n\n'+'简介:'+msg_info['digest']+ '\n\n'+'封面图地址:'+msg_info['cover']+ '\n\n')
                        # f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面:'+'![{}]'.format(title) + '({})'.format(msg_info['cover'])+ '\n')
                    #生成Word 
                    #end
                # str_comment = re.search(r'var comment_id = "(.*)" \|\| "(.*)" \* 1;', content)
                # str_msg = re.search(r"var appmsgid = \"\" \|\| '' \|\| '(.*)'", content)
                # str_token = re.search(r'window.appmsg_token = "(.*)";', content)
                # str_title = re.search(r'var msg_desc = "(.*)";', content)
                # if str_comment and str_msg and str_token:
                #     comment_id = str_comment.group(1)  # 评论id(固定)
                #     app_msg_id = str_msg.group(1)  # 票据id(非固定)
                #     appmsg_token = str_token.group(1)  # 票据token(非固定)
                #     title_article = str_title.group(1)
                #     #https://github.com/happyjared/python-learning/blob/master/wechat/wx_mps.py
                #     #https://zhuanlan.zhihu.com/p/104318974 https://github.com/JustDoPython/python-100-day
                #     #抓包工具Charles安装https://xie.infoq.cn/article/4cfb8c32a7bb9a4121390c2e6
                #     comment_url = url_comment+'?action=getcomment&scene=0&__biz={0}&appmsgid={1}&idx=1&comment_id={2}&offset=0&limit=100&pass_ticket={3}&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token={4}&x5=1&f=json&uin={5}&key={6}'.format(biz, app_msg_id, comment_id,pass_ticket, app_msg_token,uin ,key)
                #     resp = requests.get(comment_url, headers=headers,verify=False).json()
                #     ret, status = resp['base_resp']['ret'], resp['base_resp']['errmsg']
                #     if ret == 0 or status == 'ok':
                #         elected_comment = resp['elected_comment']
                #         for comment in elected_comment:
                #             nick_name = comment.get('nick_name')  # 昵称
                #             logo_url = comment.get('logo_url')  # 头像
                #             # comment_time = datetime.fromtimestamp(comment.get('create_time'))  # 评论时间
                #             comment_time=time.strftime('%Y-%m-%d', time.localtime(comment.get('create_time')))
                #             content = comment.get('content')  # 评论内容
                #             content_id = comment.get('content_id')  # id
                #             like_num = comment.get('like_num')  # 点赞数
                #             # reply_list = comment.get('reply')['reply_list']  # 回复数据
                #             # print(comment_time,nick_name,content,like_num)
                #             try:
                #                 with open(date+'_'+title_article+'.txt', 'a+', encoding='utf-8') as f:
                #                     f.write(comment_time+','+nick_name + ','+content+ ','+str(like_num)+ '\n')
                #             except Exception as err:
                #                 with open(date+'.txt', 'a+', encoding='utf-8') as f:
                #                     f.write(comment_time+','+nick_name + ','+content+ ','+str(like_num)+ '\n')
                
        except Exception as err:
            print(err)
    if can_msg_continue == 1:
        down(next_offset,biz,uin,key,pass_ticket)
        return True
    else:
        print('done')
        return False
def view(content,url):
    # with open('公众号文章.txt', 'a', encoding='utf-8') as f3:
        # f3.write(content +'\n')
    biz=re.search('var biz = "" \|\| "(.*?)"\;',content,re.M).group(1)
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
    appmsg_token='1142_iZnQ%2Btmnp%2BNLAP86Fm7H-Vtp88XFsElJvINgxQR2CL7Vw8lecv7EqXw_vEVMnwv6MG8wbNl4lz3Md7uK'
    headers = {
    "Cookie": 'pgv_pvid=3462479730;sd_userid=26861634200545809;sd_cookie_crttime=1634200545809;tvfe_boss_uuid=2462cb91e2efc262;ua_id=BbSW7iXpRV9kLjy3AAAAAJnbZGccv_XAw3N3660mGLU=;pac_uid=0_d6687c556b618;wxuin=1541436403;lang=zh_CN;rewardsn=;wxtokenkey=777;appmsg_token=1142_iZnQ%2Btmnp%2BNLAP86Fm7H-Vtp88XFsElJvINgxQR2CL7Vw8lecv7EqXw_vEVMnwv6MG8wbNl4lz3Md7uK;devicetype=Windows10x64;version=63040026;pass_ticket=49VtuZM5BD+2FwRgVp/qQe+RJZ7htI6chbyYY0kyLTD2sRTalhGiv3ZoCuHvUkax;wap_sid2=CPPngd8FEooBeV9ISFFMZzBwS1BObEZfUUpIZGVHT2luUkRJTjVLc2JSYlJBNnZrRUcza1A1dGt1R3M3ZnpBSVF5YmZVVFZJb3JyRlRJNFd2ckplUEkwZ0tBOXE2eU5BbHFWS0FsSFpFTGFXS1FlWGNwNENaaFE2RkRRQ2FRaUcwdDV4cmhuWjVrcWNWUVNBQUF+MJ2YvI0GOA1AAQ==;',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)"
    }
    origin_url = "https://mp.weixin.qq.com/mp/getappmsgext?"
    appmsgext_url = origin_url + "__biz={}&mid={}&sn={}&idx={}&appmsg_token={}&x5=1".format(biz, mid, sn, idx, appmsg_token)
    res = requests.post(appmsgext_url, headers=headers, data=data).json()
    print(appmsgext_url,res)
    return str(res["appmsgstat"]["read_num"]), str(res["appmsgstat"]["like_num"]), str(res["appmsgstat"]["old_like_num"])
down(0,biz,uin,key,pass_ticket)#设置一个offset取之前数据