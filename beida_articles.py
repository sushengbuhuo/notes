headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 FirePHP/0.7.4",
    'Referer':'https://news.pku.edu.cn/wyyd/xwdt/index.htm'
}
import os,time,re,requests
requests.packages.urllib3.disable_warnings()
encoding = 'utf-8-sig'
def trimName(name):
    return name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，').replace('\n', '，').replace('\r', '，').replace(',', '，').replace('\u200b', '，').replace('\u355b', '，').replace('\u0488', '，').replace('•','')
with open(f'网站文章.csv', 'a+', encoding=encoding) as f:
    f.write('文章日期'+','+'文章标题' + ','+'文章链接'+ ','+'文章简介'+ '\n')
urls=['https://news.pku.edu.cn/ttxw/index.htm','https://news.pku.edu.cn/xwzh/index.htm','https://news.pku.edu.cn/ldhd/index.htm','https://news.pku.edu.cn/mtbdnew/index.htm','https://news.pku.edu.cn/jxky/index.htm','https://news.pku.edu.cn/wyyd/dslt/index.htm','https://news.pku.edu.cn/wyyd/wytd/index.htm','https://news.pku.edu.cn/wyyd/xxyg/index.htm','https://news.pku.edu.cn/wyyd/xwdt/index.htm']
urls=['https://news.pku.edu.cn/ztrd/xqesdfjxzc/index.htm','https://news.pku.edu.cn/ztrd/jjlh2023/index.htm','https://news.pku.edu.cn/ztrd/jyjxxljlxl/index.htm','https://news.pku.edu.cn/ztrd/xsjwlxsj/index.htm','https://news.pku.edu.cn/ztrd/ygl/index.htm','https://news.pku.edu.cn/ztrd/ygl/index.htm','https://news.pku.edu.cn/ztrd/sqdnyymj/index.htm']#专题没简介
for url in urls:
    res = requests.get(url,headers=headers, verify=False)
    pages = re.findall(r'<option value="(.*?)"\s*>\d+</option>',res.text,flags=re.S)
    flag = 0
    for p in pages:
        res = requests.get(os.path.dirname(url)+'/'+p,headers=headers, verify=False)
        print('开始',os.path.dirname(url)+'/'+p)
        res.encoding='utf-8'
        # li = re.findall(r'<li>.*?<div class="imgHover">(.*?)</div>.*?</li>',res.text,flags=re.S)
        # 先取范围再取标签
        li = re.search(r'<ul class="newsList03 shareList">(.*?)</ul>',res.text,flags=re.S).group(1)
        li = re.findall(r'<li>(.*?)</li>',li,flags=re.S)
        res.encoding='utf-8'
        if len(li) > 0:
            for i in li:
                # print(i)
                # item = re.search(r'<div class="item-txt">(.*?)</div>',i,flags=re.S)
                # if not item:
                #     item = re.search(r'<div class="item-lf">(.*?)</div>',i,flags=re.S)
                # item = item.group(1)
                # digest = re.search(r'<p>(.*?)</p>.*?</div>',i,flags=re.S).group(1)
                date=re.search(r'<span class="item-date">(.*?)<strong>(.*?)</strong></span>',i,flags=re.S)
                t = date.group(1).replace(' ','')+date.group(2).replace(' ','')
                if int(time.mktime(time.strptime(f"{t} 00:00:00", "%Y/%m/%d %H:%M:%S"))) < 1677600000:
                    flag = 1#退出外层循环
                    break
                # print(digest)
                if 1:
                    # title = re.search(r'<p>(.*?)</p>',item,flags=re.S).group(1)
                    item2 = re.search(r'<h3><a href="(.*?)">(.*?)</a></h3>',i,flags=re.S)
                    # print(title)
                    with open(f'网站文章.csv', 'a+', encoding=encoding) as f:
                        f.write(t+','+trimName(item2.group(2)) + ','+'https://news.pku.edu.cn'+item2.group(1).replace('../..','')+ ','+''+ '\n')
            if flag == 1:
                break
        if flag == 1:
            break