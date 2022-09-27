from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import xlwt
 
 
class ZhiHu():
    pubDate=0
    title=''
 
    def __init__(self,topicURL):  # 类的初始化操作
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}  # 给请求指定一个请求头来模拟chrome浏览器
        self.topicURL = topicURL  # 要访问的话题地址
    def getHtml(self,url):
        driver = webdriver.Chrome()
        driver.get(url)
        #点击查看全部回答按钮
        driver.find_element_by_class_name('QuestionMainAction').click()
        time.sleep(3)
        bs = BeautifulSoup(driver.page_source, 'lxml')
        #循环下拉
        while True:
            b = bs.find('button',{'class':'Button QuestionAnswers-answerButton Button--blue Button--spread'})
            if b!=None:
                break
            else:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        bs = BeautifulSoup(driver.page_source, 'lxml')
        global pubDate,title
        title = bs.find('h1', class_='QuestionHeader-title').string
        pubDate= json.loads(bs.find('script', {'type': 'application/ld+json'}).get_text())["pubDate"][0:10]
        html = bs.find_all('div',{'class':'List-item'})
        print(title+"\t:\t此问题总共有%d条回答"%len(html))
        return html
 
    def downLoadToTxt(self,html,path):
 
        for tag in html:
            content = []
            content.append(title)
            content.append(pubDate)
            # 获取回答内容
            answer = tag.find('div', class_='RichContent-inner').find('span').get_text()
            #获取回答人
            answerer = json.loads(tag.find('div',class_='ContentItem AnswerItem')['data-zop'])["authorName"]
            content.append(answerer)
            #回答时间
            time = tag.find('div',class_='ContentItem-time').find('span').get_text()[-10:]
            content.append(time)
            #获取赞同数
            upvoteCount = json.loads(tag.find('div',class_='ContentItem AnswerItem')['data-za-extra-module'])["card"]["content"]["upvote_num"]
            content.append(str(upvoteCount))
            #获取评论数
            commentCount = json.loads(tag.find('div',class_='ContentItem AnswerItem')['data-za-extra-module'])["card"]["content"]["comment_num"]
            content.append(str(commentCount))
            content.append(answer)
            with open(path, 'a') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                for tag in content:
                    f.write(tag+'\t')
                f.write('\n')
            f.close()
            print(answerer+'\n'+str(upvoteCount)+'\n'+str(commentCount)+'\n\n\n')
    def downLoadToExcel(self,html):
        result = []
        head = ['问题','发布时间','回答人','回答时间','赞同数','评论数','回答内容']
        result.append(head)
        for tag in html:
            content = []
            content.append(title)
            content.append(pubDate)
            # 获取回答内容
            answer = tag.find('div', class_='RichContent-inner').find('span').get_text()
            #获取回答人
            answerer = json.loads(tag.find('div',class_='ContentItem AnswerItem')['data-zop'])["authorName"]
            content.append(answerer)
            # 回答时间
            time = tag.find('div', class_='ContentItem-time').find('span').get_text()[-10:]
            content.append(time)
            #获取赞同数
            upvoteCount = json.loads(tag.find('div',class_='ContentItem AnswerItem')['data-za-extra-module'])["card"]["content"]["upvote_num"]
            content.append(str(upvoteCount))
            #获取评论数
            commentCount = json.loads(tag.find('div',class_='ContentItem AnswerItem')['data-za-extra-module'])["card"]["content"]["comment_num"]
            content.append(str(commentCount))
            content.append(answer)
            result.append(content)
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i, row in enumerate(result):
            for j, col in enumerate(row):
                booksheet.write(i, j, col)
        workbook.save(title+'.xls')
 
    def getAnswerItemURLs(self):
        driver = webdriver.Chrome()
        driver.get(self.topicURL)
        time.sleep(2)
        #下拉次数
        i=5
        # 循环下拉
        while i>0:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(3)
            i=i-1
        bs = BeautifulSoup(driver.page_source, 'lxml')
 
        #所有的回答
        AnswerItems=bs.find_all('div',class_='ContentItem AnswerItem')
 
        AnswerItemURLs=[]
        preURL="https://www.zhihu.com"
        for item in AnswerItems:
            tailURL=item.find('a')['href']
            URL=preURL+tailURL
            AnswerItemURLs.append(URL)
            print(URL)
        print("总共有%d条问题！"%len(AnswerItemURLs))
        return AnswerItemURLs
 
    def getArticleItemURLs(self):
        driver = webdriver.Chrome()
        driver.get(self.topicURL)
        time.sleep(2)
        i=5
        # 循环下拉
        while i>0:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(3)
            i=i-1
        bs = BeautifulSoup(driver.page_source, 'lxml')
 
        # 所有的专栏
        ArticleItems = bs.find_all('div', class_='ContentItem ArticleItem')
 
        ArticleItemURLs=[]
        preURL="https:"
        for item in ArticleItems:
            tailURL=item.find('a')['href']
            URL=preURL+tailURL
            ArticleItemURLs.append(URL)
            print(URL)
        print("总共有%d条问题！"%len(ArticleItemURLs))
        return ArticleItemURLs
 
zhihu = ZhiHu("https://www.zhihu.com/search?type=content&q=%E8%B0%B7%E6%AD%8C")
 #https://github.com/123gty/zhihu-sleep/blob/main/zhihu.py
AnswerItemURLs = zhihu.getAnswerItemURLs()
for url in AnswerItemURLs:
    html = zhihu.getHtml(url)
    zhihu.downLoadToExcel(html)
print("ok")