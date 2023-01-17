import requests,pdfkit,json,time,datetime,os,re,html,pandas,csv
from random import randint
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def comments(content,date,headers,url_comment,biz,uin,key,pass_ticket,url,title):
    str_comment = re.search(r'var comment_id = "(.*)" \|\| "(.*)" \* 1;', content) or re.search(r"d.comment_id = xml \? getXmlValue\('comment_id.DATA'\) : '(.*)';", content)
    str_msg = re.search(r"var appmsgid = \"\" \|\| '' \|\| '(.*)'", content) or re.search(r"window.appmsgid = '' \|\| '' \|\| '(.*)';", content) or re.search(r"var appmsgid = \"(.*)\" \|\| '' \|\| '';",content)
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
    # print(str_comment,str_msg,str_token,str_title)
    if str_comment and str_msg and str_token:
        comment_id = str_comment.group(1)  # 评论id(固定)
        app_msg_id = str_msg.group(1)  # 票据id(非固定)
        appmsg_token = str_token.group(1)  # 票据token(非固定)
        title_article = str_title.group(1)
        rand_title = str(randint(1,10))
        data_comments = []
        comments_excel = []
        #https://github.com/happyjared/python-learning/blob/master/wechat/wx_mps.py
        # p/104318974 
        #抓包工具Charles安装 https://xie.infoq.cn/article/4cfb8c32a7bb9a4121390c2e6
        # comment_url = url_comment+'?action=getcomment&scene=0&__biz={0}&appmsgid={1}&idx=1&comment_id={2}&offset=0&limit=100&pass_ticket={3}&wxtoken=777&devicetype=android-26&clientversion=26060739&appmsg_token={4}&x5=1&f=json&uin={5}&key={6}'.format(biz, app_msg_id, comment_id,pass_ticket, app_msg_token,uin ,key)
        comment_url = url_comment+f'?action=getcomment&scene=0&appmsgid={app_msg_id}&idx=1&comment_id={comment_id}&offset=0&limit=100&send_time=&sessionid=1644213099&enterid=1644285387&uin={uin}&key={key}&pass_ticket={pass_ticket}&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6305002e&__biz={biz}&appmsg_token={appmsg_token}&x5=0&f=json'
        resp = requests.get(comment_url, headers=headers,verify=False).json()
        ret, status = resp['base_resp']['ret'], resp['base_resp']['errmsg']
        print(comment_url)
        if ret == 0 or status == 'ok':
            elected_comment = resp['elected_comment']
            print('评论数:',len(elected_comment))
            with open('留言数据.csv', 'a+', encoding='utf-8-sig') as f:
                f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'评论昵称'+','+'评论头像' +','+'评论内容' + ','+'评论时间'+ ','+'评论点赞数'+ ','+'评论回复'+ ','+'评论国家'+ ','+'评论省份'+ '\n')
            for comment in elected_comment:
                nick_name = comment.get('nick_name')  # 昵称
                logo_url = comment.get('logo_url')  # 头像
                # comment_time = datetime.fromtimestamp(comment.get('create_time'))  # 评论时间
                comment_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment.get('create_time')))
                comment_content = comment.get('content')  # 评论内容
                content_id = comment.get('content_id')  # id
                like_num = comment.get('like_num')  # 点赞数
                reply_list = comment.get('reply_new')['reply_list']  # 回复数据
                ip_info = comment.get('ip_wording')
                province_name = country_name = ''
                if ip_info:
                	country_name = ip_info['country_name']
                	province_name = ip_info['province_name']
                reply_content = reply_list[0]['content'] if len(reply_list) > 0 else ''
                data_comments.append([comment_time,nick_name,comment_content,like_num,reply_content])
                comments_excel.append([date,title,url,nick_name,logo_url,comment_content,comment_time,like_num,reply_content,country_name,province_name])
                # print(comment_time,nick_name,content,like_num)
                comments_html = comments_html + f'<li class="js_comment_item discuss_item"><div class="discuss_item_hd"><div class="user_info"><div class="nickname_wrp"><img class="avatar" src="{logo_url}"><strong class="nickname">{nick_name}        来自{country_name}---{province_name}</strong></div></div></div><div class="discuss_message"><span class="discuss_status"></span><div class="discuss_message_content js_comment_content">{comment_content}</div></div>'
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
            # dataframe = pandas.DataFrame(data_comments,columns=['评论时间','评论昵称','评论内容','评论点赞数','回复内容','评论发布国家','评论发布省份'])
            # dataframe.to_csv(date+'_'+trimName(title_article)+'.csv',encoding='utf_8_sig',index=False)
            comments_html = comments_html + '</ul></div></div>'
            with open('留言数据.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(comments_excel)
            # return str(len(elected_comment)),comments_html
        try:
            with open(date+'-'+title+'.html', 'w', encoding='utf-8') as f:
                f.write(content+comments_html)
        except Exception as err:
            with open(date+'-'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                f.write(content+comments_html)
        # try:
        #    pdfkit.from_string(content,'./' + date + '-' + title.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')+'.pdf')
        # except Exception as err:
        #    print(err)
def export():
    pass_ticket = 'x5kau7YEFBPrsiLFDgaK5ESu2X+T2JtlLS/jkY8iQK6jKG4ZqmTtj+ZLN5ISmXjaX174Y5QrtlVsQaDX+S7+qw=='
    biz = ''
    uin = ''
    key = '35d95579dc097501db08072744de78d4e409460d9ee1fbacef7c4ca9a6c3ff2524221b015db05a852fc9dfb828f7b855d5fef85850fbbe0867b4f7902b710686a4997e7fb69275f6858eea3c6d9d0a17f838c6b23608ce711f3c6b18b1d243b3309edfb46e4e38a591d69754ab38852d717578ff664c2304cb79ebc8833b06fc'
    url_comment = 'https://mp.weixin.qq.com/mp/appmsg_comment'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
    }
    urls = []
    with open(f'历史文章.txt', 'r') as f:
        urls=f.readlines()
    for i in urls:
        res = requests.get(i,proxies={'http': None,'https': None},verify=False, headers=headers)
        content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
        title = re.search(r'var msg_title = \'(.*)\'', content)
        ct = re.search(r'var ct = "(.*)";', content)
        cover = re.search(r'<meta property="og:image" content="(.*)"\s?/>', content)
        if not title:
           title = re.search(r'window\.msg_title = \'(.*?)\'', content)
        if not ct:
           ct = re.search(r'window\.ct = \'(.*?)\'', content)
        cover = cover.group(1)
        title = title.group(1)
        ct = ct.group(1)
        date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
        print(date,title)
        comments(content,date,headers,url_comment,biz,uin,key,pass_ticket,html.unescape(i),title)
export()