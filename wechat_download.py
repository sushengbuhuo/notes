import requests,pdfkit,json,time,datetime,os,re,html
from random import randint
import traceback
pass_ticket = 'zFEbbhJChxULq08vTWCQuVPe9nbv78Az7RapqXMzD0J/hHPc7G6Y6RNM8iNvMaE1'
app_msg_token = '1101_AOA3GqTDgjbfQwvJHH300bQWMJlT-3kgEn2eJQ~~'
biz = 'MzA4MDgzMTEzMw=='
uin = 'MTU0MTQzNjQwMw=='
key = '2049c8e06c26cfa52c56709e73d42a66aef9bbfe662ecd01ceaab2cd14f1495a46163050e25c1da2738ae43d90da7fe5a8ef3cbb3dae6512222cf3b1f73ae9b9aee2f1f3f6324bd4bbda50d7a530bc3b3f9c7f4a07414d3cd53cd612174daf2db0654c6ff6bcdbc91a53142cf219dfb0a53cee9019885c74cb3dbaa144011f4e'
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
            # 文章发布时间
            date = time.strftime('%Y-%m-%d', time.localtime(data['comm_msg_info']['datetime']))
            # if data['comm_msg_info']['datetime'] > 1609430400:
            #     continue
            # if data['comm_msg_info']['datetime'] < 1606752000:
            #     can_msg_continue = 0
            #     return True
            msg_info = data['app_msg_ext_info']
            #原创
            # if msg_info['copyright_stat'] == 11:
            if msg_info:
                # 文章标题
                title = msg_info['title']
                # 头条文章链接 如果删了为空
                url = msg_info['content_url']
                #次条文章数组字段解释https://zhuanlan.zhihu.com/p/104318974 is_multi=1有多篇文章 https://github.com/5zjk5/gongzonghao/blob/master/code/analysic.py https://python123.io/python/muxiatong/5dd14d1b71efdc10be55ee22
                child_msg_info = msg_info['multi_app_msg_item_list']
                # child_msg_info = []
                for child in child_msg_info:
                    if child['content_url']:
                        if is_down:
                            res = requests.get(child['content_url'],proxies={'http': None,'https': None},verify=False, headers=headers)
                            content = res.text.replace('data-src', 'src')
                            # #生成HTML 文件名不能有\/:*?"<>| 'gbk' codec can't encode character '\u200b' in position 293: illegal multibyte sequence
                            try:
                                with open(date+'_'+child['title'].replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.html', 'w', encoding='utf-8') as f:
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
                        
                        with open('拖鞋哥新传考研公众号文章列表.csv', 'a+', encoding='gbk') as f:
                            f.write(date+','+child['title'] + ','+html.unescape(child['content_url'])+ ','+child['digest']+ '\n')
                        with open('拖鞋哥新传考研公众号文章列表.md', 'a+', encoding='utf-8') as f:
                            f.write('[{}]'.format(date+'_'+child['title']) + '({})'.format(html.unescape(child['content_url']))+ '\n\n'+'文章简介:'+child['digest']+ '\n\n'+'文章作者:'+child['author']+ '\n\n')
                            # f.write(html.unescape(child['content_url'])+'\n')
                #文章摘要digest
                #文章封面cover
                if url:
                    if is_down:
                        res = requests.get(url,proxies={'http': None,'https': None},verify=False, headers=headers)
                        content = res.text.replace('data-src', 'src')
                        #生成HTML
                        try:
                            with open(date+'_'+title.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.html', 'w', encoding='utf-8') as f:
                                f.write(content)
                        except Exception as err:
                            with open(date+'_'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                                f.write(content)
                        #生成PDF
                        # try:
                        #    pdfkit.from_string(content,'./' + date + '_' + title.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.pdf')
                        # except Exception as err:
                        #    print(err)
                        # print(url + title + date + '成功')
                    #csv
                    with open('拖鞋哥新传考研公众号文章列表.csv', 'a+', encoding='gbk') as f:
                        f.write(date+','+title + ','+html.unescape(url)+ ','+msg_info['digest']+ '\n')
                    #生成markdown
                    with open('拖鞋哥新传考研公众号文章列表.md', 'a+', encoding='utf-8') as f:
                        # f.write('文章标题:'+date+'_'+title + '文章链接'+url+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面图地址:'+msg_info['cover']+ '\n')
                        f.write('[{}]'.format(date+'_'+title) + '({})'.format(html.unescape(url))+ '\n\n'+'文章简介:'+msg_info['digest']+ '\n\n'+'文章作者:'+msg_info['author']+ '\n\n')
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

down(163,biz,uin,key,pass_ticket)#设置一个offset取之前数据