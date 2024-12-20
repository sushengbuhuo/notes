import requests
import json
import re
import time
import os,csv,random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.exceptions import ConnectionError
def get_cookie():
    cookie = ''
    if os.path.exists('cookie.txt'):
        with open('cookie.txt', encoding='utf-8') as f:
            cookie = f.read().replace('\n','')
    return cookie
class zhihu_answer():
    question_id = 0
    begin_id = 0
    similar_question_url_list = []
    copy_list = []
    question_count = 20
    def __init__(self, begin_id, question_id, question_count=20,cookie=''):
        self.cookie = cookie
        self.begin_id = begin_id
        self.question_id = question_id
        self.question_count = question_count
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 FirePHP/0.7.4',
            "cookie": self.cookie,
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'referer':'https://www.zhihu.com'
        }

    def get_headers(self, api_url):
        # star = 'd_c0='
        # end = ';'
        # if self.cookie == "":
        #     raise Exception("请输入知乎cookie")
        # cookie_mes = self.cookie[self.cookie.index(star):].replace(star, '')
        # cookie_mes = cookie_mes[:cookie_mes.index(end)]
        # parse_url = api_url.replace("https://www.zhihu.com", "")
        # f = "+".join(["101_3_2.0", parse_url, cookie_mes])
        # fmd5 = hashlib.new('md5', f.encode()).hexdigest()
        # with open('g_encrypt.js', 'r', encoding="utf-8") as f:
        #     ctx1 = execjs.compile(f.read(), cwd='node_modules')
        # encrypt_str = "2.0_%s" % ctx1.call('b', fmd5)
        # self.header["x-app-za"] = 'OS=Web'
        # self.header["x-zse-93"] = "101_3_2.0"
        # self.header["x-zse-96"] = encrypt_str
        # print(self.header["x-zse-96"])
        return self.header
    def fetch_data(self,url):
        for attempt in range(3):
            try:
                response = requests.get(url, headers=self.header, verify=False, timeout=(5, 10))
                json_result = json.loads(response.content)
                return json_result
            except ConnectionError as e:
                print(f"下载失败，第 {attempt + 1} 次尝试: {e}")
                time.sleep(2)  # 等待一段时间后重试
        print("下载失败")
        return None
    def get_answer(self, question_id, limit=1,total_num=10):
        now = 0 - limit
        # total_num = self.get_total(question_id)
        # limit = min(total_num, limit)
        content_list = []
        author_name_list = []
        author_id_list = []
        author_url_token_list = []
        created_time_list = []
        updated_time_list = []
        answer_id_list = []
        dict = {}
        offset = 0
        # for i in range(0, total_num // limit):
        #     now = now + limit;now=0
        #     url = "https://www.zhihu.com/api/" \
        #           "v4/questions/{question_id}/answers?include=data%5B*%5D." \
        #           "is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_co" \
        #           "llapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse" \
        #           "_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_co" \
        #           "unt%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvote" \
        #           "up_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2C" \
        #           "updated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labe" \
        #           "led%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%" \
        #           "2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D" \
        #           ".url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings." \
        #           "table_of_content.enabled&offset={now}&limit={limit}&sort_by=default&platform=desktop".format(
        #         question_id=str(question_id), limit=limit, now=now)
        #     response = requests.get(url, headers=self.get_headers(url), verify=False)
        #     json_result = json.loads(response.content);
        #     data = json_result["data"]
        #     print("\r爬取进度:" + str(round(i / (total_num // limit) * 100, 2)) + "%", end="", flush=True)
            # for i in data:
            #     content_list.append(i["content"])
            #     author_name_list.append(i['author']['name'])
            #     author_id_list.append(i['author']['id'])
            #     author_url_token_list.append(i['author']['url_token'])
        url = "https://www.zhihu.com/api/" \
                  "v4/questions/{question_id}/feeds?include=data%5B*%5D." \
                  "is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_co" \
                  "llapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse" \
                  "_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_co" \
                  "unt%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvote" \
                  "up_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2C" \
                  "updated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labe" \
                  "led%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%" \
                  "2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D" \
                  ".url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings." \
                  "table_of_content.enabled&offset=0&limit=5&sort_by=default&platform=desktop".format(
                question_id=str(question_id))
        while True:
            # response = requests.get(url, headers=self.header, verify=False, timeout=(5, 10))
            json_result = self.fetch_data(url)
            data = json_result["data"]
            time.sleep(random.randint(2, 5))
            print('开始下载',offset)
            if len(data) == 0:
                break
            offset += 5#;print(data[0]['target']["content"])
            if offset % 100 == 0:
                print('等待一会')
                time.sleep(random.randint(30, 60))
            if offset > 1000:
                break
            for i in data:
                # if i['target']['created_time'] < 1664553600 and i['target']['created_time'] > 1504195200:
                #     continue
                content_list.append(i['target']["content"])
                author_name_list.append(i['target']['author']['name'])
                author_id_list.append(i['target']['author']['id'])
                answer_id_list.append(i['target']['id'])
                author_url_token_list.append(i['target']['author']['url_token'])
                created_time_list.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['target']['created_time'])))
                updated_time_list.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['target']['updated_time'])))
                # html
                
            url=json_result['paging']['next']
        dict["content_list"] = content_list
        dict["author_name_list"] = author_name_list
        dict["author_id_list"] = author_id_list
        dict["author_url_token_list"] = author_url_token_list
        dict["created_time"] = created_time_list
        dict["updated_time"] = updated_time_list
        dict["answer_id_list"] = answer_id_list
        return dict

    def format_content(self, content_list):
        text_list = []
        pre = re.compile('>(.*?)<')
        for i in content_list:
            text = ''.join(pre.findall(i))
            text_list.append(text)
        return text_list

    def get_question_title(self, question_id):
        url = "https://www.zhihu.com/api/v4/questions/{question_id}/feeds?include=data%5B%2A%5D.is_normal%2Cadmin_closed_" \
              "comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_stick" \
              "y%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%" \
              "2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cr" \
              "elevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authoriz" \
              "ed%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url" \
              "%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_" \
              "of_content.enabled&limit={limit}&offset=0&platform=desktop&sort_by=default".format(
            question_id=str(question_id), limit=20)
        # print(url)
        response = requests.get(url, headers=self.header, verify=False)#;print(response.text)
        json_result = json.loads(response.content)#;print(response,666,json_result,url)
        data = json_result["data"]
        title = data[0]['target']['question']['title']
        return title

    def single_answer(self, question_id,type):
        question_title = self.trimName(self.get_question_title(question_id))
        print("问题标题：" + question_title + "，问题id：" + str(question_id))
        # print("爬取ing.....请等待，等待时间依据回答数量而定")
        result_dict = self.get_answer(question_id, 20)
        comments = []
        book_data = {}
        num = 0
        content = f'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>{question_title}</h1>'
        # self.get_answer(question_id)
        text_list = self.format_content(result_dict['content_list'])
        # print('回答',text_list)
        try:
            # with open(question_title + ".txt", mode="w",
            #           encoding='utf-8') as f:
            #     f.write("问题：" + question_title + "\n")
            #     f.write("问题id：" + str(question_id) + "\n\n")
            #     for i in range(0, len(text_list)):
            #         f.write("回答者id：" + result_dict["author_id_list"][i] + "\n")
            #         f.write("回答者空间地址：" + result_dict["author_url_token_list"][i] + "\n")
            #         f.write("回答者昵称：" + result_dict["author_name_list"][i] + "\n")
            #         f.write("回答的内容：" + text_list[i] + "\n\n")
            # f.close()
            for i in range(0, len(text_list)):
                num +=1
                result = re.findall(r'《(.*?)》', text_list[i])
                for name in result:
                    book_data[name] = book_data.get(name, 0) + 1
                answer='https://www.zhihu.com/answer/'+str(result_dict["answer_id_list"][i])
                created_time=result_dict["created_time"][i]
                comments.append([
                    answer,
                    'https://www.zhihu.com/people/'+result_dict["author_url_token_list"][i],
                    result_dict["author_name_list"][i],
                    text_list[i],
                    created_time,
                    result_dict["updated_time"][i]]
                    )
                content+=f'<p>回答{num}、<strong>回答链接:<a href="{answer}">{answer}</a> 发布时间: {created_time}</strong></p>'+result_dict["content_list"][i].replace('src="data:', '').replace('data-actualsrc', 'src')
            content+='</body></html>'
            with open(str(question_id)+'.html', 'w', encoding='utf-8') as f:
                f.write(content)    
            #统计书名
            if type == 2:
                self.books(book_data,question_id)
            if type == 1:
                for i in result_dict['content_list']:
                    pass
                    # self.imgs(i,str(question_id))
            with open(str(question_id)+'_'+question_title+'.csv', 'a+', encoding='utf-8-sig', newline='') as csvfile:
                 writer = csv.writer(csvfile)
                 writer.writerow(['回答链接','回答者主页','回答者昵称','回答内容','回答发布时间','回答更新时间'])
                 writer.writerows(comments)
        except Exception as err:
            print('错误信息',err)
        finally:
            print("\ndone")

    def trimName(self,name):
        return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，')
    def imgs(self,data,id):
        imgs = re.findall('img src="(.*?)"',data,re.S)
        if not os.path.isdir(id):
            os.mkdir(id)
        if len(imgs) == 0:
            pass
        else:
            for img in imgs:
                if 'jpg' in img:
                    try:
                        print('正在下载图片',img)
                        res = requests.get(img,headers=self.get_headers(img), verify=False)
                        with open(id + '/' + str(re.search('https://(.*?)/\d+/(.*)\.jpg',img).group(2)) + '.jpg','wb') as fp:
                            fp.write(res.content)
                    except Exception as e:
                        print('下载失败',e)
                    
if __name__ == '__main__':
    print('本工具更新于2024年12月12日，获取最新版本请关注公众号玩转互联网达人')
    qid = input("公众号玩转互联网达人提示你，请输入知乎问题id：")
    cookie = get_cookie()
    # type = input('苏生不惑提示你，请输入抓取类型，1下载图片，2提取关键词：')
    zhihu = zhihu_answer(qid,qid,20,cookie)
    zhihu.single_answer(qid,1)
