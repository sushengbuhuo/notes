import time
import random
import requests
#需要一个公众号 s/fEjoOCbmZWKFFiBwbdeERA zhihu.com/p/379062852
def get_headers():
    headers = {
        "Cookie": '',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    return headers
def get_params():
    
    begin = "0"
    params = {
        "sub": "list",
        "search_field":"null",
        "sub_action": "list_ex", 
        "begin": begin,
        "free_publish_type": "1",
        "count": "5",
        "fakeid": 'MjM5NjM4MDAxMg==',
        "type": "101_1",
        "token": '',
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
    return params
def get_article_list(headers, params):
    i = 0
    column_name = "aid,appmsgid,author_name,title,cover_img,digest,link,create_time"
    article_list_path = "wechat_article_list.csv"
    url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
    with open(article_list_path, "a") as f:
        f.write(column_name + '\n')
    while True:
        begin = i * 5
        params["begin"] = str(begin)
        # 随机暂停几秒，避免过快的请求导致过快的被查到
        time.sleep(random.randint(1,10))
        resp = requests.get(url, headers=headers, params = params, verify=False)
        # 微信流量控制, 退出
        if resp.json()['base_resp']['ret'] == 200013:
            print("frequencey control, stop at {}".format(str(begin)))
            time.sleep(3600)
            continue
        
        if i == "0":
            total_count = eval(resp.json()['publish_page'])['total_count']
            print("We have "+str(tatal_count) + " articles.")
    
        publish_list = eval(resp.json()['publish_page'])['publish_list']
        # 如果返回的内容中为空则结束
        if len(publish_list) == 0:
            print("all ariticle parsed")
            break
    
        for publish in publish_list:
            publish = eval(publish['publish_info'].replace("true","True").replace("false","False"))['appmsgex'][0]
            info = '"{}","{}","{}","{}","{}","{}","{}","{}"'.format(str(publish["aid"]), \
                str(publish['appmsgid']), str(publish['author_name']), \
                str(publish['title'].replace("\n","").replace(",",";")), \
                str(publish['cover']), str(publish['digest'].replace("\n","").replace(",",";")), \
                str(publish['link']), str(publish['create_time']))
            with open(article_list_path, "a") as f:
                f.write(info+'\n')
            print("\n".join(info.split(",")))
            print("\n\n---------------------------------------------------------------------------------\n")

        # 翻页
        i += 1
def main():
    headers = get_headers()
    params = get_params()
    get_article_list(headers, params)
if __name__ == '__main__':
    main()