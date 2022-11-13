import re
import time
import requests
cookies = {'cookie': ''}
#爬取微信公众号文章，并存在本地文本中 https://github.com/YPstar-yes/Crawl-WeChat-articles/blob/master/weixin.py
def get_content(query):
    url = 'https://mp.weixin.qq.com'
    #设置headers
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }

    #读取上一步获取到的cookies



    #登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，从这里获取token信息
    response = requests.get(url=url, cookies=cookies)
    token = re.findall(r'token=(\d+)', str(response.url))[0]

    #搜索微信公众号的接口地址
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    #搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
    query_id = {
        'action': 'search_biz',
        'begin': '0',
        'count': '5',
        'query': query,
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1'
        }
    #打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
    search_response = requests.get(search_url, cookies=cookies, headers=header, params=query_id)
    #取搜索结果中的第一个公众号
    lists = search_response.json().get('list')[0]
    #获取这个公众号的fakeid，后面爬取公众号文章需要此字段
    fakeid = lists.get('fakeid')

    #微信公众号文章接口地址
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    #搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
    query_id_data = {

        'action': 'list_ex',
        'begin': '0',#不同页，此参数变化，变化规则为每页加5
        'count': '5',
        'fakeid': fakeid,
        'type': '9',
        'query': '',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        }
    #打开搜索的微信公众号文章列表页
    appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
    #获取文章总数
    max_num = appmsg_response.json().get('app_msg_cnt')
    #每页至少有5条，获取文章总的页数，爬取时需要分页爬
    num = int(int(max_num) / 5)
    print('总页数：{}'.format(int(num)))
    #起始页begin参数，往后每页加5
    begin = 0
    while num + 1 > 0 :
        query_id_data = {
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),  # 不同页，此参数变化，变化规则为每页加5
            'count': '5',
            'fakeid': fakeid,
            'type': '9',
            'query': '',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',

            }
        print('正在翻页：--------------',begin)

        #获取每一页文章的标题和链接地址，并写入本地文本中
        query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
        fakeid_list = query_fakeid_response.json().get('app_msg_list')
        for item in fakeid_list:
            content_link=item.get('link')
            content_title=item.get('title')
            fileName=query+'.csv'
            with open(fileName,'a',encoding='utf-8-sig') as fh:
                fh.write(content_title+","+content_link+"\n")
        num -= 1
        begin = int(begin)
        begin+=5
        time.sleep(2)

if __name__=='__main__':
    try:
        #登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
        query= input('请输入你想爬取的公众号文章 ：')
        print("开始爬取公众号：" + query)
        get_content(query)
        print("爬取完成")
        # gzlist = ['微信派']
        # #登录之后，通过微信公众号后台提供的微信公众号文章接口爬取文章
        # for query in gzlist:
        #     #爬取微信公众号文章，并存在本地文本中
        #     print("开始爬取公众号："+query)
        #     get_content(query)
        #     print("爬取完成")
    except Exception as e:
        print(str(e))