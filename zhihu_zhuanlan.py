import time
import re
import os
import requests,json
from bs4 import BeautifulSoup
#https://gitee.com/crossin/snippet/blob/master/get_zhihu/get_zhihu.py https://zhuanlan.zhihu.com/p/44918640
def get_list():
    url = 'https://www.zhihu.com/api/v4/columns/%s/articles?include=data[*].topics&limit=10' % author
    article_dict = {}
    while True:
        print('抓取中', url)
        try:
            resp = requests.get(url, headers=headers)
            content = resp.content.decode("utf-8")
            j = json.loads(content)
            #j = resp.json()
            data = j['data']
        except:
            print('抓取失败')

        for article in data:
            aid = article['id']
            akeys = article_dict.keys()
            if aid not in akeys:
                article_dict[aid] = article['title']

        if j['paging']['is_end']:
            break
        url = j['paging']['next']
        time.sleep(2)

    with open('zhihu_ids.txt', 'w', encoding='utf-8') as f:
        items = sorted(article_dict.items())
        for item in items:
            f.write('%s %s\n' % item)

def get_html(aid, title, index):
    title = title.replace('/', '／')
    title = title.replace('\\', '＼')
    file_name = '%03d. %s.html' % (index, title)
    if os.path.exists(file_name):
        print(title, '已经存在')
        return
    else:
        print('保存中', title)
    try:
        url = 'https://zhuanlan.zhihu.com/p/' + aid
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find(class_='Post-RichText').prettify()
        content = content.replace('data-actual', '')
        content = content.replace('h1>', 'h2>')
        content = re.sub(r'<noscript>.*?</noscript>', '', content)
        content = re.sub(r'src="data:image.*?"', '', content)
        content = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><h1>%s</h1>%s</body></html>' % (
            title, content)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
    except:
        print('保存 %s 失败', title)
    time.sleep(2)

def get_details():
    with open('zhihu_ids.txt', encoding='utf-8') as f:
        i = 1
        for line in f:
            lst = line.strip().split(' ')
            aid = lst[0]
            title = '_'.join(lst[1:])
            get_html(aid, title, i)
            i += 1

def to_pdf():
    import pdfkit
    print('导出 PDF...')
    htmls = []
    for root, dirs, files in os.walk('.'):
        htmls += [name for name in files if name.endswith(".html")]
    print(htmls)
    pdfkit.from_file(sorted(htmls), author + '.pdf')

if __name__ == '__main__':
    author = input('输入专栏名称')
    if not author:
        author = 'grapeot'
    headers = {
        'origin': 'https://zhuanlan.zhihu.com',
        'referer': 'https://zhuanlan.zhihu.com/%s' % author,
        'User-Agent': ('Mozilla/5.0'),
    }
    get_list()
    get_details()
    to_pdf()