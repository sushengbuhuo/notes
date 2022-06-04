import requests,json,time,os,re
from tqdm import tqdm
#https://github.com/L-M-Sherlock/zhihubackup
def getdata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
        "x-api-version": "3.0.91",
    }
    r = requests.get(url, headers=headers)
    return json.loads(r.text)
types = {"answer":"回答","article":"文章","pin":"想法"}
def makedirs(username, target_type):
    try:
        os.makedirs(os.path.join("./" ,username, target_type))
    except OSError:
        pass

def down(username):
    api = f"https://www.zhihu.com/api/v3/moments/{username}/activities?desktop=true"
    t = tqdm()
    num = 0
    while True:
        jdata = getdata(api)
        for dd in jdata['data']:
            target = dd['target']
            if 'author' not in target or target["author"]["url_token"] != username:
                continue
            target_type = types.get(target['type'])
            makedirs(username, target_type)
            saved = ["<meta charset=\"UTF-8\">"]
            if 'question' in target and 'title' in target['question']:
                saved.append(target['question']['title'])
            for saved_type in ('title', 'content', 'updated_time'):
                if saved_type in target:
                    if type(target[saved_type]) is not list:
                        raw = str(target[saved_type])
                        if saved_type == 'content':
                            # 显示图片
                            raw = show_img(raw)
                        saved.append(raw)
                    else:
                        for tt in target[saved_type]:
                            for saved_type2 in ('content', 'url'):
                                if saved_type2 in tt:
                                    saved.append(tt[saved_type2])
            if target_type == '想法':
                title = ''
                created=target['created']
            elif target_type == '回答':
                title = target['question']['title']
                created=target['created_time']
            else:
                title = target['title']
                created=target['created']
            print('正在下载',target_type,target['url'])
            # if title != '':
            num+=1
            if 'api' in target['url']:
                target['url'] = target['url'].replace('api', 'www').replace('answers', 'answer')
            with open(os.path.join("./", username, "zhihu.csv"), 'a+', encoding='utf-8-sig') as f:
                if num == 1:
                    f.write(','.join(['标题','链接','类型', '\n']))
                title = title.replace('\"', '').replace(',','，')
                f.write(','.join([title, target['url'].replace("https://",""), target_type, '\n']))
            title = '-' + validate_title(title) if title != '' else ''
            with open(os.path.join("./", username, target_type, "%s%s.html" % (time.strftime('%Y-%m-%d', time.localtime(created)), title)), 'w', encoding='utf-8') as f:
                f.write('\n'.join(saved))
            t.update(1)
        paging = jdata['paging']
        if paging['is_end']:
            break
        api = paging['next']

def save_record(current_api, username):
    with open(username, 'w') as f:
        f.write(current_api)

def read_record(username):
    if os.path.isfile(username):
        with open(username) as f:
            return f.read().strip()
    else:
        return None

def validate_title(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)
    return new_title

def show_img(raw):
    pattern = re.compile(r'(?<=</noscript>).*?(?=</figure>)')
    raw = pattern.sub('', raw)
    pattern = re.compile(r'</*noscript>')
    raw = pattern.sub('', raw)
    return raw
name = input("苏生不惑提示你请输入知乎id：")
down(name)