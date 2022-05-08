import bs4
import requests
import wordcloud
from tkinter import *
from tkinter import messagebox
import time#https://zhuanlan.zhihu.com/p/363759232
def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    res = requests.get(url, headers=headers)
    
    
    return res
def main():
    BV=e1.get()
    url='http://api.bilibili.com/x/web-interface/view?bvid=%s'%BV
    a=get_html(url)

    data=a.json()
    list_=data.get('data')
    cid=list_['pages'][0]['cid']
    url2='http://api.bilibili.com/x/v1/dm/list.so?oid=%s'%cid
    danmulist=get_html(url2)
    data=danmulist.content.decode('utf-8')
    soup = bs4.BeautifulSoup(data, 'lxml')
    result=soup.find_all('d')
    danmu=''
    danmudic={}
    n=1
    for i in result:
        a=i.text
        if a in danmudic:
            n+=1
        else:
            n=1
        danmudic[a]=n
        danmu+=a
        danmu+=','
    wc=wordcloud.WordCloud(font_path=r'C:\Windows\Font\simfang.ttf',background_color='white',height=800,width=1000)
    wc.generate(danmu)
    image=wc.to_image()
    def show():
        image.show()
    danmu_=sorted(danmudic.items(),key=lambda kv:kv[1],reverse=True)
    root.withdraw()
    root2=Tk()
    theButton =Button(root2,text='生成词云',command=show)
    theButton.pack(side=BOTTOM)
    sb=Scrollbar(root2)
    sb.pack(side=RIGHT,fill=Y)
    lb=Listbox(root2,yscrollcommand=sb.set)
    for i in  danmu_:
        lb.insert(END,i)
    lb.pack(side=LEFT,fill=BOTH)
    sb.config(command=lb.yview) 

root=Tk()
root.title('b站弹幕获取')
Label(root,text='请输入BV号:').grid(row=0,column=0)
e1=Entry(root)
e1.grid(row=0,column=1,padx=10,pady=5)
Button(root,text='获取弹幕',width=10,command=main)\
                .grid(row=3,column=1,sticky='w',padx=10,pady=10)