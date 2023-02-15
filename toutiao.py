import os
import requests
import json
import execjs
import traceback,urllib3,time,re
from random import randint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 输入关键字keyword，爬取相关内容的文章信息，并存储（excel） https://github.com/BATFOR/HeadlineCrawer
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
class NewToutiao():
    def __init__(self,url,max_behot_time):
        self.max_behot_time = max_behot_time
        self.url = url
        self.session = requests.Session()
        self.get_ttcid()
        self.get_ttwebid()
        self.get_MONITOR_WEB_ID()
        self.cookie = self.get_cookie()
        self.filename = ''
        self.down = 1
        headers = {
            'authority': 'www.toutiao.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '',
            'referer': self.url,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'x-csrftoken': 'undefined'
        }
        with open(f'{self.filename}.csv', 'a+', encoding='utf-8-sig') as f:
            f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章简介'+ ','+'文章作者'+','+'文章封面'+','+'阅读数'+','+'评论数'+','+'点赞数'+'\n')
        while True:
            content = self.get_data()
            time.sleep(2)
            if not content or not content['data']:
                break
            for i in content['data']:
                if not i.get('item_id'):
                    continue
                if self.down and i['article_genre'] == 'article':
                    res = requests.get('https://www.toutiao.com/article/'+i['item_id'],verify=False, headers=headers)
                    print('https://www.toutiao.com/article/'+i['item_id'])
                    fav = re.search(r'aria-label="点赞(.*?)"', res.text).group(1)
                    try:
                        comments_html = re.search(r'<div class="article-content">(.*)</article></div>', res.text).group(1)
                        article_content = f'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div class="article-content">{comments_html}</article></div></body></html>'
                        with open('html/'+trimName(i['title'])+'.html', 'w', encoding='utf-8') as f:
                            f.write(article_content)
                    except Exception as err:
                        print('出错了',err,i['item_id'],'https://www.toutiao.com/article/'+i['item_id'])
                        with open('html/'+str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
                            f.write(article_content)
                image_url = ''
                if i.get('image_list'):
                    image_url=i['image_list'][0]['url']
                with open(f'{self.filename}.csv', 'a+', encoding='utf-8-sig') as f2:
                     f2.write(trimName(i['behot_time'])+','+trimName(i['title'])+','+ 'https://www.toutiao.com/article/'+i['item_id']+ ','+trimName(i['abstract'])+ ','+trimName(i['source'])+','+image_url+','+ i['go_detail_count']+ ','+i['comments_count']+ ','+str(fav)+'\n')
            #下载微头条
            # for i in content['data']:
            #     if not i.get('stream_cell'):
            #         continue
            #     if self.down and i['stream_cell']['id']:
            #         res = requests.get('https://www.toutiao.com/w/'+str(i['stream_cell']['id']),verify=False, headers=headers)
            #         print('https://www.toutiao.com/w/'+str(i['stream_cell']['id']))
            #         try:
            #             comments_html = re.search(r'<div class="wtt-content">(.*)</article></div>', res.text).group(1)
            #             article_content = f'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><div class="wtt-content">{comments_html}</article></div></body></html>'
            #             with open(trimName(str(i['stream_cell']['id']))+'.html', 'w', encoding='utf-8') as f:
            #                 f.write(article_content)
            #         except Exception as err:
            #             print('error:https://www.toutiao.com/w/'+str(i['stream_cell']['id']))
            #             with open(str(randint(1,10))+'.html', 'w', encoding='utf-8') as f:
            #                 f.write(article_content)
            #     with open(f'{self.filename}.csv', 'a+', encoding='utf-8-sig') as f2:
            #          f2.write('https://www.toutiao.com/w/'+str(i['stream_cell']['id'])+'\n')
            # break

    # 获取Cookie参数的ttwebid  https://github.com/wangluozhe/NewToutiao/blob/main/sign.js
    def get_ttwebid(self):
        url = self.url
        urlsp = requests.utils.urlparse(url)
        path = urlsp.path
        headers = {
            'authority': 'www.toutiao.com',
            'method': 'GET',
            'path': path,
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': self.url,
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        self.session.get(url,headers=headers)

    # 获取Cookie参数的ttcid和ttscid
    def get_ttcid(self):
        url = "https://xxbg.snssdk.com/websdk/v1/getInfo?q=hQ3ewVF18TVgg%2BT46gUA3rL3a662wbibusC0iq%2FdxTNU4%2Ba1VbLoQvv6N6B8o5iJhvvqvsdoxhjhF5Sx7pcBTpjKhtrdtrpl12CV83KshkeGwAOtOhiNQNX29cbom8hWNiQ7LD660DTo41%2B8WIPxyJCJHLq5u5DtZz823N9uRR7yBb5Gx7GOvpMHywMEPngg4GEcHH5Qdr13ngRmpkaYpLJKyFgSo6MYd3hlFVIJWP8yFn4ZqLzC9n8jxKr5oS%2BAcGoPrk8Q3w0MqXW7DDIsrHI2CSeq4OVbvXEfRl3nM1rF3UErEiXK0R1VKKSY2CERh6U684P7%2F0ObD8AYwZlNzv97DTvhILkLSw3bRW2L5Z9gB6zOcoBbjRE2I1byO0pMYsLUmy0i9klQBip3EYeruV64DqTr%2BwInfKI%2FbohYAwaRzrEHJ%2Ba3nBI1HR%2BUhxvrefPOfVD0bkTt1GmOOv%2B9w6JXK1OBgTDr%2Bh0uCGaEc8PiYxfphBNXLb%2BU9VokCOQdF9jjjhH2MFUN2a2vL%2FOQC2Gm0cFXr5wMjj1QDdRAhfIeHNvEyvLy8dLcq1V3bpMIWEmG7ZaimgFoYzDvCf9Kxcjh2aYJdMqgGbeZzGwT1WPdc715QEGM4%2F4CURPd3YoqyCqc5CjCeBZR2ZGjWD6RECIPpnmlhqmNeTomiTs1b9xl%2BvK3AVeoIBslWV8LTYYV5T8aZUDt26f8U01dimXYUtIFS%2BvDFXflvo3hu%2BzlETGbgIgWHcYJMrMoZSqs3S%2FpC5pTv6XOua3%2FFn6YzXrFgnVZrt2%2F6CkqDbdX9mcow2RGevsGEGkGwRWM%2BVw8KhVQvQ2Lv2nNhm%2Fj%2FB0HvP%2B3QMqquQeUMQLfVF9XFGMbnEz3NMFc3OY5qyU6lMwOyh6kKPDkqQ9A1PU2mAl3r6LXK1%2Fpyf2%2BfmnyHYceHL3qbG3VB2j0GN0ZpUhgk8F6jXHJvLuIhyn3l8zFDBHRXPgst55j6V0komW92crSzrOL2n1U6ufVGT8J5Rbk71OgfVHhp76fleR9bI%2FDcU1zP1QAqSg53F1fx17p5hk7wGS7kLzs%2BitMbcd80CPe5nM5qTW9Z67fR1Z%2BYchk5JVVMG8Wtap2T9IC%2FpG2QjUCIAx%2BabgV0oKr8p8JRriL0pDyRo6GR3D983UN2NkL2pfyR9si8E%3D%3D&callback=_7210_1599898331166"
        headers = {
            'authority': 'xxbg.snssdk.com',
            'method': 'GET',
            'path': '/websdk/v1/getInfo?q=hQ3ewVF18TVgg%2BT46gUA3rL3a662wbibusC0iq%2FdxTNU4%2Ba1VbLoQvv6N6B8o5iJhvvqvsdoxhjhF5Sx7pcBTpjKhtrdtrpl12CV83KshkeGwAOtOhiNQNX29cbom8hWNiQ7LD660DTo41%2B8WIPxyJCJHLq5u5DtZz823N9uRR7yBb5Gx7GOvpMHywMEPngg4GEcHH5Qdr13ngRmpkaYpLJKyFgSo6MYd3hlFVIJWP8yFn4ZqLzC9n8jxKr5oS%2BAcGoPrk8Q3w0MqXW7DDIsrHI2CSeq4OVbvXEfRl3nM1rF3UErEiXK0R1VKKSY2CERh6U684P7%2F0ObD8AYwZlNzv97DTvhILkLSw3bRW2L5Z9gB6zOcoBbjRE2I1byO0pMYsLUmy0i9klQBip3EYeruV64DqTr%2BwInfKI%2FbohYAwaRzrEHJ%2Ba3nBI1HR%2BUhxvrefPOfVD0bkTt1GmOOv%2B9w6JXK1OBgTDr%2Bh0uCGaEc8PiYxfphBNXLb%2BU9VokCOQdF9jjjhH2MFUN2a2vL%2FOQC2Gm0cFXr5wMjj1QDdRAhfIeHNvEyvLy8dLcq1V3bpMIWEmG7ZaimgFoYzDvCf9Kxcjh2aYJdMqgGbeZzGwT1WPdc715QEGM4%2F4CURPd3YoqyCqc5CjCeBZR2ZGjWD6RECIPpnmlhqmNeTomiTs1b9xl%2BvK3AVeoIBslWV8LTYYV5T8aZUDt26f8U01dimXYUtIFS%2BvDFXflvo3hu%2BzlETGbgIgWHcYJMrMoZSqs3S%2FpC5pTv6XOua3%2FFn6YzXrFgnVZrt2%2F6CkqDbdX9mcow2RGevsGEGkGwRWM%2BVw8KhVQvQ2Lv2nNhm%2Fj%2FB0HvP%2B3QMqquQeUMQLfVF9XFGMbnEz3NMFc3OY5qyU6lMwOyh6kKPDkqQ9A1PU2mAl3r6LXK1%2Fpyf2%2BfmnyHYceHL3qbG3VB2j0GN0ZpUhgk8F6jXHJvLuIhyn3l8zFDBHRXPgst55j6V0komW92crSzrOL2n1U6ufVGT8J5Rbk71OgfVHhp76fleR9bI%2FDcU1zP1QAqSg53F1fx17p5hk7wGS7kLzs%2BitMbcd80CPe5nM5qTW9Z67fR1Z%2BYchk5JVVMG8Wtap2T9IC%2FpG2QjUCIAx%2BabgV0oKr8p8JRriL0pDyRo6GR3D983UN2NkL2pfyR9si8E%3D%3D&callback=_7210_1599898331166',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': self.url,
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        self.session.get(url,headers=headers)

    # 获取Cookie参数的MONITOR_WEB_ID
    def get_MONITOR_WEB_ID(self):
        url = "https://i.snssdk.com/slardar/sdk.js?bid=toutiao_web_pc"
        headers = {
            'authority': 'i.snssdk.com',
            'method': 'GET',
            'path': '/slardar/sdk.js?bid=toutiao_web_pc',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin':'https://www.toutiao.com',
            'referer': self.url,
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        self.session.get(url, headers=headers)

    # 获取Cookie参数的s_v_web_id
    def get_s_v_web_id(self):
        ctx = execjs.compile("""
            function to_base36() {
                var t = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split("")
                  , e = t.length
                  , n = (new Date).getTime().toString(36)
                  , r = [];
                r[8] = r[13] = r[18] = r[23] = "_",
                r[14] = "4";
                for (var o, i = 0; i < 36; i++)
                    r[i] || (o = 0 | Math.random() * e,
                    r[i] = t[19 == i ? 3 & o | 8 : o]);
                console.log("verify_" + n + "_" + r.join(""));
                return "verify_" + n + "_" + r.join("");
            }
            """)
        return ctx.call('to_base36')

    # 合并Cookie
    def get_cookie(self):
        cookie = ''
        for key, value in self.session.cookies.get_dict().items():
            cookie += key + '=' + value + '; '
        cookie += 's_v_web_id=' + self.get_s_v_web_id()
        return cookie

    # 获取_signature参数
    def get_signature(self,url):
        signature = os.popen('node get_toutiao_sign.js {url}'.format(url='"'+url+'"')).read()
        return "&_signature=" + signature.replace('\n','').replace(' ','')

    # 获取结果
    def get_data(self):
        token = self.url.split('/')[-2]
        base_url = 'https://www.toutiao.com/toutiao'
        path = '/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token={token}&max_behot_time={max_behot_time}'.format(token=token,max_behot_time=self.max_behot_time)
        # path = '/api/pc/list/user/feed?category=profile_all&app_name=toutiao_web&token={token}&max_behot_time={max_behot_time}'.format(token=token,max_behot_time=self.max_behot_time)
        base_url += path
        signature = self.get_signature(base_url)
        path += signature
        base_url += signature
        headers = {
            'authority': 'www.toutiao.com',
            'method': 'GET',
            'path': path,
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': self.cookie,
            'referer': self.url,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'x-csrftoken': 'undefined'
        }
        print('请求地址',base_url)
        response = self.session.get(base_url.replace('/toutiao',''),headers=headers,timeout=10)#;print(response.text)
        content = json.loads(response.text)
        if not content['has_more']:
            return ''
        self.max_behot_time = content['next']['max_behot_time']
        return content

if __name__ == '__main__':
    id = input("请输入头条id：")
    if not os.path.exists('html'):
        os.mkdir('html')
    if not id:
        id="MS4wLjABAAAAfDAPKkWGH5h-e8zzOAyTUoCSK_DszWR5nxEf9paqwG8"
    NewToutiao(f'https://www.toutiao.com/c/user/token/{id}/',0)