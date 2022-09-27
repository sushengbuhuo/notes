import requests
import re
import os
from hashlib import md5
from requests.exceptions import RequestException
import bs4
from requests import RequestException
from selenium import webdriver
import time
from matplotlib import pyplot as plt
import re
from wordcloud import WordCloud
import jieba
import pandas as pd

def request_url(url):
    headers = {
        'Referer': 'https://movie.douban.com',
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text
def movie_info(html):
    urls = []
    data = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    items = soup.select('li > div.item')
    for item in items:
        #urls.append(item.select('div.info > div.hd > a')[0]['href'])
        desc_item = item.select('div.info > div.bd > p.quote > span')
        desc = ''
        if desc_item is not None and len(desc_item) > 0:
        	desc = desc_item[0].text
        data.append({
        	'url':item.select('div.info > div.hd > a')[0]['href'],
        	'title':item.select('div.info > div.hd > a > span')[0].text,
            'rank':item.select('div.pic > em')[0].text,
            'score':item.select('div.info > div.bd > div.star > span.rating_num')[0].text,
            'desc':desc,
        	})
    return data
def movie_info2(url):
    html = request_url(url)
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
    category = []
    for object in typeList:
        category.append(object.text)

    average = content.find('strong', property='v:average').text
    votes = content.find('span', property='v:votes').text

    rating_per_items = content.find('div', class_='ratings-on-weight').find_all('div', class_='item')
    rating_per = [rating_per_items[0].find('span', class_='rating_per').text, rating_per_items[1].find('span', class_='rating_per').text]

    return {'title': title, 'url': url, 'director': ",".join(director), 'country': country, 'year': year,
            'average': average, 'votes': votes}

if __name__ == '__main__':
    urls = ['https://movie.douban.com/top250?start={0}&filter='.format(i * 25) for i in range(10)]
    #movie_list = [request_url(url) for url in urls]
    movie_list = []
    for url in urls:
    	movie_list.append(request_url(url))
    	time.sleep(1)
    movie_url_list = [movie_info(movie) for movie in movie_list]
    # print(movie_url_list)
    data = []
    for j in movie_url_list:
    	for k in j:
    		data.append(k)
    print(data)
    #movie_urls = sum(movie_url_list,[])
    #print(movie_urls)
    #movies = [movie_info(url) for url in movie_urls]
    #df = pd.DataFrame(sum(movies,[]))
    df = pd.DataFrame(data)
    df.to_csv("douban_movie.csv",encoding="utf_8_sig",index=False)