import requests
import re
import os
from hashlib import md5
from requests.exceptions import RequestException
import bs4 as bs4
from requests import RequestException
from selenium import webdriver
import time
from matplotlib import pyplot as plt
import re
from wordcloud import WordCloud
import jieba
import pandas as pd
#豆瓣评论
# browser=webdriver.Chrome('D:/download/chromedriver')   
# data = []
# exclude = ['有','没有','是','不是','有没有','是不是','怎么','什么','为什么']
# for i in range(0,5):
#     url = 'https://www.douban.com/group/692739/discussion?start='+str(i*25)
#     browser.get(url)
#     time.sleep(1)
#     title = browser.find_element_by_css_selector('.olt')
#     tr_contents = title.find_elements_by_tag_name('tr')
#     dat = []
#     for tr in tr_contents[1:]:
#         lis = []
#         for td in tr.find_elements_by_css_selector('.title'):
#             lis.append(' '.join(jieba.cut(td.text,cut_all=True)))
#         dat.extend(lis)
#     data.extend(dat)
#     print(i)
# all_word = str(' '.join(data))
# all_word = all_word.replace('有','')
# all_word = all_word.replace('没有','')
# all_word = all_word.replace('有没有','')
# all_word = all_word.replace('是','')
# all_word = all_word.replace('不是','')
# all_word = all_word.replace('是不是','')
# for count in data:
#     if count in exclude:
#         print(count)
#         data.remove(count)
# print(all_word)   
# wordcloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf",background_color="black", width=600,height=300, max_words=200,min_font_size=8).generate(all_word)
# image=wordcloud.to_image()
# image.show()
# wordcloud.to_file("douban.jpg")
def get_page(url):#请求并获取豆瓣250的源码
    try:
        headers = {
        'Referer': 'https://movie.douban.com',
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 FirePHP/0.7.4',
        'Cookie':'douban-fav-remind=1; __utmc=30149280; __utmc=223695111; gr_user_id=5c335db6-6854-4284-a4c3-257c51e87658; __yadk_uid=hvtFnqY39w7ocCtPpz1dQQsfBtIl5YYb; bid=xqwYI9blZRQ; ll="108288"; viewed="7163250_6878988_3009821"; ap_v=0,6.0; _pk_id.100001.4cf6=5b244bd84f49df42.1560749771.3.1600398537.1571746912.; _pk_ses.100001.4cf6=*; __utma=30149280.1742808116.1560749776.1578622227.1600398538.6; __utmb=30149280.0.10.1600398538; __utmz=30149280.1600398538.6.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.174163658.1560749776.1571746921.1600398538.3; __utmb=223695111.0.10.1600398538; __utmz=223695111.1600398538.3.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
#Python 爬取豆瓣电影 http://www.justdopython.com/2020/01/18/douban-movie-top250-analysis-119/
#https://github.com/Swpan2018/Python/blob/master/%E7%88%AC%E8%99%AB/%E8%B1%86%E7%93%A3top250/douban_top250.py
def get_parse(html):#进行解析
    parse = re.compile('<li.*?div.*?"item".*?<a.*?img.*?src="(.*?)"'
                       '.*?div.*?"info".*?span.*?"title">(.*?)</span>'
                       '.*?div.*?"bd".*?p.*?>(.*?)<br>', re.S)
    parse_over = re.findall(parse, html)
    for item in parse_over:
        yield {
            "jpg": item[0].strip(),
            "title": item[1].strip(),
            "director": item[2].strip()
        }


def down_photo(photos_url):#下载图片
    if not os.path.exists('photo'):#查看当前路径下是否有这个文件
        os.mkdir('photo')#创建文件夹
    for photo_url in photos_url:
        try:
            photo = requests.get(photo_url)
            if photo.status_code == 200:
                name = 'photo' + os.path.sep + md5(photo.content).hexdigest() + '.jpg'
                with open(name, 'wb+') as f:
                    f.write(photo.content)
        except Exception:
            return None

def get_page_html(url):
    headers = {
        'Referer': 'https://movie.douban.com/chart',
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_movie_url(html):
    ans = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = soup.select('li > div.item')
    for item in items:
        href = item.select('div.info > div.hd > a')[0]['href']
        ans.append(href)
    return ans


# 【名称，链接。导演，国家，上映时间，类型，评分，[五星，四星，三星，二星，一星占比]，评价人数】
def get_movie_info(url):
    html = get_page_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    content = soup.find('div', id='content')

    title = content.find('span', property='v:itemreviewed').text
    year = content.find('span', class_='year').text[1:5]
    directors = content.find('span', class_='attrs').find_all('a')
    director = []
    for i in range(len(directors)):
        director.append(directors[i].text)

    country = content.find(text=re.compile('制片国家/地区')).next_element
    typeList = content.find_all('span', property='v:genre')
    type = []
    for object in typeList:
        type.append(object.text)

    average = content.find('strong', property='v:average').text
    votes = content.find('span', property='v:votes').text

    rating_per_items = content.find('div', class_='ratings-on-weight').find_all('div', class_='item')
    rating_per = [rating_per_items[0].find('span', class_='rating_per').text, rating_per_items[1].find('span', class_='rating_per').text]

    return {'title': title, 'url': url, 'director': "#".join(director), 'country': country, 'year': year, 'type': "#".join(type),
            'average': average, 'votes': votes, 'rating_per': "#".join(rating_per)}


def main():
    urls = []
    for i in range(1):
        start = i * 25
        url = 'https://movie.douban.com/top250?start=' + str(start) + '&filter='
        html = get_page_html(url)
        urls.append(get_movie_url(html))

    index = 0;
    for url in urls:
        ans = get_movie_info(url)
        print(index, ans)
        index = index + 1


def getUrls():
    url_init = 'https://movie.douban.com/top250?start={0}&filter='
    urls = [url_init.format(index * 25) for index in range(10)]
    return urls

def writeToFile(content):
    filename = 'douban250.txt'
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(content + '\n')
if __name__ == '__main__':
    #pass
    # for num in range(0, 250, 25):
    #     photos_url = []
    #     url = "https://movie.douban.com/top250?start=" + str(num)
    #     html = get_page(url)
    #     print(html)
    #     items = get_parse(html)
    #     movies = []
    #     for item in items:
    #         photos_url.append(item["jpg"])
    #         #print(item)
    #         movies.append(item)
    #     df = pd.DataFrame(data=movies, columns=[
    #     '图片', '标题', '导演'])
    #     df.to_csv('movies.csv', index=False,encoding="utf_8_sig")
    #     # down_photo(photos_url)
    #https://github.com/JustDoPython/python-100-day/blob/master/day-119/douban-movie-top250.py http://www.justdopython.com/2020/01/18/douban-movie-top250-analysis-119/
    # print(get_movie_info('https://movie.douban.com/subject/1292052/'))
    # os._exit()
    list_urls = getUrls()
    list_htmls = [get_page_html(url) for url in list_urls]
    movie_urls = [get_movie_url(html) for html in list_htmls]
    movie_url_list = []
    for url_list in movie_urls:
        movie_url_list += url_list

    # for url in movie_url_list:
        # print(url)

    movie_details = [get_movie_info(url) for url in movie_url_list]
    data = []
    for detail in movie_details:
        data.append(detail)
        writeToFile(str(detail))
        # print(detail)
    # df = pd.DataFrame(data)
    # df.to_csv("douban250.csv",encoding="utf_8_sig")