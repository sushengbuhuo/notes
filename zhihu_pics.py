import urllib
import requests
from pyquery import PyQuery as pq
import os
from hashlib import md5
from multiprocessing.pool import Pool
#python爬取知乎回答图片 https://zhuanlan.zhihu.com/p/43408400  https://www.zhihu.com/question/310335618/answer/602970433

url = 'https://www.zhihu.com/api/v4/answers/1711691566?include=is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,collapsed_counts,reviewing_comments_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_author,voting,is_thanked,is_nothelp,upvoted_followees;author.is_blocking,is_blocked,is_followed,voteup_count,message_thread_token,badge[?(type=best_answerer)].topics'
headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Referer': 'https://www.zhihu.com/api/v4/questions/602970433',
        'x-requested-with': 'fetch',
        'cookie':'x'
    }
# res = requests.get(url,headers=headers,verify=False).json()
# print(res['content'])
# content = pq(res['content'])  # content 内容为 xml 格式的网页，用pyquery解析
# imgs_url = []
# imgs = content('figure noscript img').items()
# i = 0
# for img_url in imgs:
# 	i+=1
# 	imgs_url.append(img_url.attr('src'))
# 	tmp = requests.get(img_url.attr('src'),headers=headers,verify=False)
# 	with open('pics/'+str(i)+'.jpg', 'wb') as f:
# 		f.write(tmp.content)

# print('图片总数:'+str(len(imgs_url)))   
# exit()
import requests
from lxml import etree
import time
import re
from bs4 import BeautifulSoup
import json
#下载图片代码https://www.zhihu.com/question/299205851/answer/742197093

def get_img(url):
    res = requests.get(url,headers=headers)
    i = 1
    json_data = json.loads(res.text)
    datas = json_data['data']
    for data in datas:
        id = data['author']['name']
        content = data['content']
        imgs = re.findall('img src="(.*?)"',content,re.S)
        if len(imgs) == 0:
            pass
        else:
            for img in imgs:
                if 'jpg' in img:
                    res_1 = requests.get(img,headers=headers)
                    fp = open('pics/'+id + '+' + str(i) + '.jpg','wb')
                    fp.write(res_1.content)
                    i = i + 1
                    print(id,img)
if __name__ == '__main__':
    urls = ['https://www.zhihu.com/api/v4/questions/411390910/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default'.format(str(i)) for i in range(0,20,5)]
    # for url in urls:
        # get_img(url)
        # time.sleep(2)


#发送请求函数https://zhuanlan.zhihu.com/p/33375357
def getpage(header,id):
    for i in range(0,10):
        base_url = 'https://www.zhihu.com/api/v4/questions/'+str(id)+'/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent&offset=' + str(i) + '&limit=1&sort_by=default'
        print(base_url)
        response = requests.get(base_url, headers=header)
        html = response.text
        img_json = json.loads(html)
        # print(img_json)
        print('正在抓取知乎长腿小姐姐图片 第%s条评论'% i)
        contentpage(img_json)
        time.sleep(1)
#解析json数据
def contentpage(img_json):
    # try:
    data = img_json["data"][0]
    content = data["content"]
    # print(content)
    html = BeautifulSoup(content,'lxml')
    # 提取img标签 由于会抓到两张一页的图片所以每隔一个提取一次
    img_page = html.select('img')[::2]
    print(img_page)
    for i in img_page:
        address = i.get('src')
        print(address)
        imgpage(address)
    # except:
        # print('此评论没有图片')
#存储函数
def imgpage(address):
    #用图片地址后缀当图片名
    fname = re.sub(r'\?.*','',address).split('/')[-1]
    print(fname)
    response = requests.get(address,headers={
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Referer': 'https://www.zhihu.com/api/v4/questions/602970433',
        'x-requested-with': 'fetch',
    })
    #直接返回二进制数据
    html = response.content
    with open('周杰伦/'+ fname , 'wb') as f:
        f.write(html)

#https://www.zhihu.com/question/441362880
if __name__ == '__main__':
    print('开始抓取')
    getpage(headers,413007096)