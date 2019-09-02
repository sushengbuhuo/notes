import re
import requests
import json
import os
import pdfkit
import shutil
import datetime
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import unquote
#https://github.com/wbsabc/zsxq-spider

ZSXQ_ACCESS_TOKEN = '2B9BA4A2-8CAB-3A7C-32E7-' # 登录后Cookie中的Token
GROUP_ID = '141281112142'                                  # 知识星球中的小组ID
PDF_FILE_NAME = '知识星球.pdf'                               # 生成PDF文件的名字
DOWLOAD_PICS = False                                        # 是否下载图片 True | False 下载会导致程序变慢
DOWLOAD_COMMENTS = True                                    # 是否下载评论
ONLY_DIGESTS = False                                       # True-只精华 | False-全部
FROM_DATE_TO_DATE = False                                  # 按时间区间下载
EARLY_DATE = '2017-05-25T00:00:00.000+0800'                # 最早时间 当FROM_DATE_TO_DATE=True时生效 为空表示不限制 形如'2017-05-25T00:00:00.000+0800'
LATE_DATE = '2019-09-25T00:00:00.000+0800'                 # 最晚时间 当FROM_DATE_TO_DATE=True时生效 为空表示不限制 形如'2017-05-25T00:00:00.000+0800'
DELETE_PICS_WHEN_DONE = True                               # 运行完毕后是否删除下载的图片
DELETE_HTML_WHEN_DONE = True                               # 运行完毕后是否删除生成的HTML
COUNTS_PER_TIME = 30                                       # 每次请求加载几个主题 最大可设置为30
DEBUG = False                                              # DEBUG开关
DEBUG_NUM = 120                                            # DEBUG时 跑多少条数据后停止 需与COUNTS_PER_TIME结合考虑

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h1>{title}</h1>
<br>{author} - {cretime}<br>
<p>{text}</p>
</body>
</html>
"""
htmls = []
num = 0

def get_data(url):

    OVER_DATE_BREAK = False

    global htmls, num
        
    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN',
        'Connection':'keep-alive',
        'Cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216777c5cbc1c06-0e956f1670bd95-38082f5c-2073600-16777c5cbc2ab6%22%2C%22%24device_id%22%3A%2216777c5cbc1c06-0e956f1670bd95-38082f5c-2073600-16777c5cbc2ab6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; abtest_env=product; zsxq_access_token=0FBA189E-6562-984C-B495-',
        'DNT':'1',
        'Host':'api.zsxq.com',
        'Origin':'https://wx.zsxq.com',
        'Referer':'https://wx.zsxq.com/dweb2/index/group/init',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.7.5000',
        'X-Request-Id':'bb7071a27-9a8f-9a09-3350-88844325b86',
        'X-Signature':'cd5b01d81872b72e081bf29432db69db9b0d9850',
        'X-Timestamp':'1567396494',
        'X-Version':'1.10.17'
    }
    
    rsp = requests.get(url, headers=headers)
    print(url,headers,rsp.json())
    """
    cat temp.json
    {
      "succeeded": true,
      "resp_data": {
        "topics": []
      }
    }
    cat temp.css
    h1 {font-size:40px; color:red; text-align:center;}
    p {font-size:30px;}
    img{
    	max-width:100%;
    	margin:20px auto;
    	height:auto;
    	border:0;
    	outline:0
    	-webkit-box-shadow: 1px 4px 16px 8px #5CA2BE;
        -moz-box-shadow: 1px 4px 16px 8px #5CA2BE;
        box-shadow: 1px 4px 16px 8px #5CA2BE;
        /*set the images aligned*/
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    """
    with open('temp.json', 'w', encoding='utf-8') as f: # 将返回数据写入temp.json方便查看
        f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))
    
    with open('temp.json', encoding='utf-8') as f:
        for topic in json.loads(f.read()).get('resp_data').get('topics'):
            if FROM_DATE_TO_DATE and EARLY_DATE.strip():
                if topic.get('create_time') < EARLY_DATE.strip():
                    OVER_DATE_BREAK = True
                    break

            content = topic.get('question', topic.get('talk', topic.get('task', topic.get('solution'))))

            anonymous = content.get('anonymous')
            if anonymous:
                author = '匿名用户'
            else:
                author = content.get('owner').get('name')

            cretime = (topic.get('create_time')[:23]).replace('T', ' ')

            text = content.get('text', '')
            text = handle_link(text)
            title = str(num) + '_' + cretime[:16]
            num += 1
            if topic.get('digested') == True:
                title += '_精华'

            if DOWLOAD_PICS and content.get('images'):
                soup = BeautifulSoup(html_template, 'html.parser')
                images_index = 0
                for img in content.get('images'):
                    url = img.get('large').get('url')
                    local_url = './images/' + str(num - 1) + '_' + str(images_index) + '.jpg'
                    images_index += 1
                    urllib.request.urlretrieve(url, local_url)
                    img_tag = soup.new_tag('img', src=local_url)
                    soup.body.append(img_tag)
                html_img = str(soup)
                html = html_img.format(title=title, text=text, author=author, cretime=cretime)
            else:
                html = html_template.format(title=title, text=text, author=author, cretime=cretime)

            if topic.get('question'):
                answer_author = topic.get('answer').get('owner').get('name', '')
                answer = topic.get('answer').get('text', "")
                answer = handle_link(answer)

                soup = BeautifulSoup(html, 'html.parser')
                answer_tag = soup.new_tag('p')

                answer = '【' + answer_author + '】 回答：<br>' + answer
                soup_temp = BeautifulSoup(answer, 'html.parser')
                answer_tag.append(soup_temp)

                soup.body.append(answer_tag)
                html = str(soup) 
			
            files = content.get('files')
            if files:
                files_content = '<i>文件列表(需访问网站下载) :<br>'
                for f in files:
                    files_content += f.get('name') + '<br>'
                files_content += '</i>'
                soup = BeautifulSoup(html, 'html.parser')
                files_tag = soup.new_tag('p')
                soup_temp = BeautifulSoup(files_content, 'html.parser')
                files_tag.append(soup_temp)
                soup.body.append(files_tag)
                html = str(soup)

            comments = topic.get('show_comments')
            if DOWLOAD_COMMENTS and comments:
                soup = BeautifulSoup(html, 'html.parser')
                hr_tag = soup.new_tag('hr')
                soup.body.append(hr_tag)
                for comment in comments:
                    comment_str = ''
                    if comment.get('repliee'):
                        comment_str = '[' + comment.get('owner').get('name') + ' 回复 ' + comment.get('repliee').get('name') + '] : ' + handle_link(comment.get('text'))
                    else:
                        comment_str = '[' + comment.get('owner').get('name') + '] : ' + handle_link(comment.get('text'))

                    comment_tag = soup.new_tag('p')
                    soup_temp = BeautifulSoup(comment_str, 'html.parser')
                    comment_tag.append(soup_temp)
                    soup.body.append(comment_tag)
                html = str(soup)

            htmls.append(html)

    # DEBUG 仅导出部分数据时使用
    if DEBUG and num >= DEBUG_NUM:
       return htmls

    if OVER_DATE_BREAK:
        return htmls

    next_page = rsp.json().get('resp_data').get('topics')
    if next_page:
        create_time = next_page[-1].get('create_time')
        if create_time[20:23] == "000":
            end_time = create_time[:20]+"999"+create_time[23:]
            str_date_time = end_time[:19]
            delta = datetime.timedelta(seconds=1)
            date_time = datetime.datetime.strptime(str_date_time, '%Y-%m-%dT%H:%M:%S')
            date_time = date_time - delta
            str_date_time = date_time.strftime('%Y-%m-%dT%H:%M:%S')
            end_time = str_date_time + end_time[19:]
        else :
            res = int(create_time[20:23])-1
            end_time = create_time[:20]+str(res).zfill(3)+create_time[23:] # zfill 函数补足结果前面的零，始终为3位数
        end_time = quote(end_time)
        if len(end_time) == 33:
            end_time = end_time[:24] + '0' + end_time[24:]
        next_url = start_url + '&end_time=' + end_time
        print(next_url)
        get_data(next_url)

    return htmls

def handle_link(text):
    soup = BeautifulSoup(text, "html.parser")

    mention = soup.find_all('e', attrs={'type' : 'mention'})
    if len(mention):
        for m in mention:
            mention_name = m.attrs['title']
            new_tag = soup.new_tag('span')
            new_tag.string = mention_name
            m.replace_with(new_tag)

    hashtag = soup.find_all('e', attrs={'type' : 'hashtag'})
    if len(hashtag):
        for tag in hashtag:
            tag_name = unquote(tag.attrs['title'])
            new_tag = soup.new_tag('span')
            new_tag.string = tag_name
            tag.replace_with(new_tag)

    links = soup.find_all('e', attrs={'type' : 'web'})
    if len(links):
        for link in links:
            title = unquote(link.attrs['title'])
            href = unquote(link.attrs['href'])
            new_a_tag = soup.new_tag('a', href=href)
            new_a_tag.string = title
            link.replace_with(new_a_tag)

    text = str(soup)
    text = re.sub(r'<e[^>]*>', '', text).strip()
    text = text.replace('\n', '<br>')
    return text

def make_pdf(htmls):
    html_files = []
    for index, html in enumerate(htmls):
        file = str(index) + ".html"
        html_files.append(file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(html)

    options = {
        "user-style-sheet": "temp.css",
        "page-size": "Letter",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "cookie": [
            ("cookie-name1", "cookie-value1"), ("cookie-name2", "cookie-value2")
        ],
        "outline-depth": 10,
    }
    try:
        pdfkit.from_file(html_files, PDF_FILE_NAME, options=options)
    except Exception as e:
        pass

    if DELETE_HTML_WHEN_DONE:
        for file in html_files:
            os.remove(file)

    print("电子书生成成功！")

if __name__ == '__main__':
    images_path = r'./images'
    if DOWLOAD_PICS:
        if os.path.exists(images_path):
            shutil.rmtree(images_path)
        os.mkdir(images_path)

    # 仅精华
    #start_url = 'https://api.zsxq.com/v1.10/groups/481818518558/topics?scope=digests&count=30'
    # 全部
    #start_url = 'https://api.zsxq.com/v1.10/groups/481818518558/topics?count=30'
    start_url = ''
    if ONLY_DIGESTS:
        start_url = 'https://api.zsxq.com/v1.10/groups/' + GROUP_ID + '/topics?scope=digests&count=' + str(COUNTS_PER_TIME)
    else:
        start_url = 'https://api.zsxq.com/v1.10/groups/' + GROUP_ID + '/topics?scope=all&count=' + str(COUNTS_PER_TIME)

    url = start_url
    if FROM_DATE_TO_DATE and LATE_DATE.strip():
        url = start_url + '&end_time=' + quote(LATE_DATE.strip())
    make_pdf(get_data(url))

    if DOWLOAD_PICS and DELETE_PICS_WHEN_DONE:
        shutil.rmtree(images_path) 
