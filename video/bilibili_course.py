import requests
import csv
from urllib import parse
import json
import string
'''
1、出现的问题，json接口数据格式的提取
2、csv保存文件出现的换行错误
'''

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
}


def get_parse(result):
    content=[]
    items=result['result']
    for item in items:
        id=item['id']
        rank=item['rank_offset']
        print(rank)
        tag=item['tag']
        author=item['author']
        title=item['title']
        url=item['arcurl']
        play=item['play']
        favorites=item['favorites']
        video_review=item['video_review']
        pubdate=item['pubdate']
        con=[id,rank,tag,author,title,url,play,favorites,video_review,pubdate]
        content.append(con)
    save(content)


def save(content):
    with open('./study.csv', 'a', encoding='gb18030',newline='')as file:
        write = csv.writer(file)
        write.writerows(content)


def main():
    header = ['id', '排名', '标签', 'up主', '标题','播放url','播放次数','收藏数','投币数','更新时间']
    with open('./study.csv', 'a',encoding='gb18030',newline='')as f:
        write=csv.writer(f)
        write.writerow(header)
    type=['编程']
    types=['公开课','演讲','TED','哲学','课程','可汗学院','哈佛大学','北京大学','耶鲁大学','斯坦福大学','麻省理工','人工智能','百家讲坛','高数','万门大学','教育','学习','考试','英语','视频教程','讲座','线上课堂','编程','数学','语言','高考','高中','英语学习','物理','速成课','平面设计','设计','考研英语','PS教程','文化','历史','机器学习']
    for j in type:
        cate = parse.quote(j, safe=string.printable)
        for i in range(100):
            url='https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id=39&page={}&pagesize=20&jsonp=jsonp&keyword={}'.format(i,cate)
            response = requests.get(url, headers=headers)
            result = json.loads(response.text)
            print(url)
            get_parse(result)

#https://www.zhihu.com/question/59989404/answer/1164140056
if __name__=='__main__':
    # main()

    import requests#pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
    from pyquery import PyQuery as pq
    import pandas as pd
    urls = ['https://movie.douban.com/top250?start={}'.format(i) for i in range(0,250,25)]
    data = []
    # df = pd.DataFrame(columns=['排行','电影名','豆瓣评分','豆瓣链接',])
    for url in urls:
        res = pq(requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}).text)
        for item in res('.item').items():
            num = item.find('.pic em').text()
            title = item.find('.title').html()
            link = item.find('.pic a').attr('href')
            star = item.find('.rating_num').text()
            print(num, title, star, link)
            data.append([num, title, star, link])
    df = pd.DataFrame(data, columns=['排行','电影名','豆瓣评分','豆瓣链接'])        
    df.to_csv('豆瓣电影数据.csv', encoding='utf-8-sig')        