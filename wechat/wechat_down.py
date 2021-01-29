import requests,pdfkit,json,time,datetime,os,re
pass_ticket = '4dOq1rjVAWILjJzcwRK0nem4nOQWw0tmQQN76uUZxyVtxuC+37NPuONdMuDn3nol'
biz = 'MzA4NTEzNDgyOA=='
uin = 'NjQ3OTQwMTAy'
key = 'd37330a9c208494c77e53a5abc41f5a575b32290ae6ef191c14509663500eeb77964b12056131564858f2581c7f65175c63add046cce5cfa9f412626b464d134b8987870f4500304b81ee35470c5f1700aafab72bb4e39aeb39f7cc6a7280701985adab16531d6efe70e8aa60f740e3f49831ec62c69faf104b8847b50a95559'
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
    print(response_dict)
    next_offset = response_dict['next_offset']
    can_msg_continue = response_dict['can_msg_continue']
    general_msg_list = response_dict['general_msg_list']
    data_list = json.loads(general_msg_list)['list']
    time.sleep(2)
    htmls = []
    # print(data_list)
    for data in data_list:
        try:
            # 文章发布时间
            date = time.strftime('%Y-%m-%d', time.localtime(data['comm_msg_info']['datetime']))
            msg_info = data['app_msg_ext_info']
            #原创
            # if msg_info['copyright_stat'] == 11:
            if msg_info:
                # 文章标题
                title = msg_info['title']
                # 文章链接
                url = msg_info['content_url']
                #文章摘要digest
                #文章封面cover
                res = requests.get(url,proxies={'http': None,'https': None},verify=False, headers=headers)
                content = res.text.replace('data-src', 'src')
                # str_comment = re.search(r'var comment_id = "(.*)" \|\| "(.*)" \* 1;', content)
                # str_msg = re.search(r"var appmsgid = '' \|\| '(.*)'\|\|", content)
                # str_token = re.search(r'window.appmsg_token = "(.*)";', content)
                # res_info = requests.post(url_info+'?f=json&mock=&uin={0}&key={1}&pass_ticket={2}&wxtoken=777&devicetype=Windows%26nbsp%3B7%26nbsp%3Bx64&clientversion=6300002f&__biz={3}&appmsg_token=1087_YK%252B9eT1mfR89MJPGHME9zpu8biw-1h8D7pkyvXLxC4sGbLQIu6qHhWgfSz9k8LtTxfhN92qRoEZkgfwZ&x5=0&f=json', headers=headers, verify=False).json()

                # if str_comment and str_msg and str_token:
                    # comment_id = str_comment.group(1)  # 评论id(固定)
                    # app_msg_id = str_msg.group(1)  # 票据id(非固定)
                    # appmsg_token = str_token.group(1)  # 票据token(非固定)
                    # resp = requests.get(url_comment+'?action=getcomment&scene=0&__biz={0}&appmsgid={1}&idx=1&comment_id={2}&offset=0&limit=100&uin=777&key=777&pass_ticket={3}&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token={4}&x5=1&f=json'format(biz, app_msg_id, comment_id,pass_ticket, appmsg_token), headers=headers, verify=False).json()
                    # print(resp)

                #生成markdown
                with open('绒绒168公众号文章列表.md', 'a+', encoding='utf-8') as f:
                    # f.write('文章标题:'+date+'_'+title + '文章链接'+url+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面图地址:'+msg_info['cover']+ '\n')
                    f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n\n'+'文章简介:'+msg_info['digest']+ '\n\n')
                    # f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n\n'+'简介:'+msg_info['digest']+ '\n\n'+'封面图地址:'+msg_info['cover']+ '\n\n')
                    # f.write('[{}]'.format(date+'_'+title) + '({})'.format(url)+ '\n'+'简介:'+msg_info['digest']+ '\n'+'封面:'+'![{}]'.format(title) + '({})'.format(msg_info['cover'])+ '\n')
                #生成HTML
                # try:
                #     with open(date+'_'+title+'.html', 'w', encoding='utf-8') as f:
                #         f.write(content)
                # except Exception as err:
                #     with open(date+'_'+'.html', 'w', encoding='utf-8') as f:
                #         f.write(content)
                #生成PDF
                # try:
                #    pdfkit.from_string(content,'./' + date + '_' + title.replace(' ', '')+'.pdf')
                # except Exception as err:
                #    print(err)
                # print(url + title + date + '成功')
        except Exception as err:
            print(err)
    if can_msg_continue == 1:
        down(next_offset,biz,uin,key,pass_ticket)
        return True
    else:
        print('done')
        return False

down(0,biz,uin,key,pass_ticket)