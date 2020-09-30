import requests,pdfkit,json,time,datetime,os
biz = 'MzA5NjEwNjE0OQ=='#随公众号改变
uin = 'NjQ3OTQwMTAy'#不变
key = '041bb01ba83758f926c1f592b1d52bf64bb2c93ae98f4377cde97f854c32e4b57ef9a9e69eedd8a38b742303e94ca2f881978a6d3e58f90ce21eb736bf43230889c3ef378a24d8ca35436da7518b8e48dba1ab10c759ad6dd2b4f2261629bf9cb5a4b4805fa1df60ed51a543cfaf06ddea839b850c2baddaa28c954f1a3ed06a'
def parse(offset, biz, uin, key):
    # url前缀
    url = "https://mp.weixin.qq.com/mp/profile_ext"
    # 请求头https://www.zhihu.com/people/zywu-43
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
    proxies = {
        'https': None,
        'http': None,
    }
    # 重要参数https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5ODIzNDExMg==&f=json&offset=48&count=10&is_ok=1&scene=124&uin=MTU0MTQzNjQwMw%3D%3D&key=a42654d5f06828b5d9e40deca0ea5f73004fecbf9ae4cfe0d37653465b623e26d82d0948a73d3cdf4fffd5df19bebafed06815f22f05bac0e5679625c86bb429885529cea1973bfb4d9f18481e624a0cea7cd12932fb55e7ed892ccd6dcda141737cf5ed9811d477cd90cdf4d8371a8b1bdd63de15e193787fc75f186cdf41b5&pass_ticket=FjDlSKDCqgdl0E5WNMPJLuBO3eeqP%2FdrlM1Q8%2FzEHxisVbm7ZVemLp6VeXsrLd0i&wxtoken=&appmsg_token=1074_NFjOFA%252FiWPMoGcRLiG7SzMUc-NoJp7QhKSYmYw~~&x5=0&f=json
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
    # 发送请求，获取响应
    response = requests.get(url, headers=headers, params=param, proxies=proxies)
    response_dict = response.json()
    print(response_dict)
    next_offset = response_dict['next_offset']
    can_msg_continue = response_dict['can_msg_continue']
    general_msg_list = response_dict['general_msg_list']
    data_list = json.loads(general_msg_list)['list']
    htmls = []
    # print(data_list)
    for data in data_list:
        try:
            # 文章发布时间
            date = time.strftime('%Y-%m-%d', time.localtime(data['comm_msg_info']['datetime']))
            msg_info = data['app_msg_ext_info']
            #原创
            if msg_info['copyright_stat'] == 11:
                # 文章标题
                title = msg_info['title']
                # 文章链接
                url = msg_info['content_url']
                #文章摘要digest
                #文章封面cover

                res = requests.get(url,proxies={'http': None,'https': None},verify=False, headers=headers)
                content = res.text.replace('data-src', 'src')
                filename=str(int(time.time()))+'.html'
                #生成HTML文件
                #htmls.append(filename)
                with open(date+'_'+title+'.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                #生成Excel
                #with open('wechat2.csv', 'a+', encoding='gbk') as f:
                #    f.write(title.replace(',', '，')+','+msg_info['digest'].replace(',', '，')+',' + msg_info['cover'].replace(',', '，') + ',' +url.replace(',', '，')+','+str(date)+ '\n')
                #生成markdown
                with open('wechat.md', 'a+', encoding='utf-8') as f:
                    f.write('[{}]'.format(title) + '({})'.format(url)+ '\n')
                #生成PDF
                #try:
                #    pdfkit.from_string(content,'./' + date + '_' + title.replace(' ', '')+'.pdf')
                #except Exception as err:
                #    print(err)
                # 部分文章标题含特殊字符，不能作为文件名
                    #f = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
                    #pdfkit.from_string(content,f)
                    # 自己定义存储路径（绝对路径）
                #finally:
                #    os.remove(filename)
                #pdfkit.from_url(url, './' + date + title + '.pdf') #图片获取不到
                print(url + title + date + '成功')
        except Exception as err:
            print(err)
    #try:
        #pdfkit.from_file(htmls,'公众号文章备份.pdf')
    #except:
    #    pass
    if can_msg_continue == 1:
        #time.sleep(1)
        parse(next_offset,biz,uin,key)
        return True
    else:
        print('爬取完毕')
        return False


parse(229,biz,uin,key)