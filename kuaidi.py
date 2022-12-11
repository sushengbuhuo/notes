import requests
import tkinter as tk
from tkinter import *
import threading
#https://www.52pojie.cn/thread-1722476-1-1.html
import requests
import tkinter as tk
from tkinter import *
import threading
import re
class jiemian():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('快递停发区域查询')
        self.size = self.root.geometry('300x400')
        self.sende_email_label = tk.Label(self.root, text='省份').place(x=0, y=0)
        self.send_get_label = tk.Label(self.root, text='市区').place(x=0, y=20)
        self.set_subject_label = tk.Label(self.root, text='县城').place(x=0, y=40)
        self.send_get_name_label = tk.Label(self.root, text='门牌号').place(x=0, y=60)
        self.start = tk.Button(self.root, text='开始查询', command=lambda: jiemian.thread(self))
        self.start.place(x=200, y=50)
        self.send_get_name_label_read = tk.Label(self.root, text='自动识别').place(x=0, y=80)
        self.send_email_entry1 = tk.Entry(self.root)
        self.send_email_entry1.place(x=55, y=81)
        self.send_email_entry = tk.Entry(self.root)
        self.send_email_entry.place(x=55, y=0)
        self.send_get_entry = tk.Entry(self.root)
        self.send_get_entry.place(x=55, y=20)
        self.set_subject_entry = tk.Entry(self.root)
        self.set_subject_entry.place(x=55, y=40)
        self.send_get_name_entry = tk.Entry(self.root)
        self.send_get_name_entry.place(x=55, y=60)
        self.txt = Text(self.root)
        self.txt.place(x=0, y=100)
        self.root.mainloop()
 
    def kuaidi(self):
        self.txt.delete("1.0", "end")
        if self.send_email_entry1.get()!='':
            PATTERN1 = r'([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市)){0,1}([\u4e00-\u9fa5]{2,7}?(?:区|市|州)){0,1}([\u4e00-\u9fa5]{2,7}?(?:县|区)){0,1}([\u4e00-\u9fa5]{2,7}?(?:镇|乡)){0,1}([\u4e00-\u9fa5]{2,7}?(?:村|街|街道)){0,1}([\d]{1,3}?(号)){0,1}'
            # \u4e00-\u9fa5 匹配任何中文
            # {2,5} 匹配2到5次
            # ? 前面可不匹配
            # (?:pattern) 如industr(?:y|ies) 就是一个比 'industry|industries' 更简略的表达式。意思就是说括号里面的内容是一个整体是以y或者ies结尾的单词
            pattern = re.compile(PATTERN1)
            p1 = ''
            p2 = ''
            p3 = ''
            p4 = ''
            p5 = ''
            p6 = ''
            m = pattern.search(self.send_email_entry1.get())
            if not m:
                print('None')
            if m.lastindex >= 1:
                p1 = m.group(1)
            if m.lastindex >= 2:
                p2 = m.group(2)
            if m.lastindex >= 3:
                p3 = m.group(3)
            if m.lastindex >= 4:
                p4 = m.group(4)
            if m.lastindex >= 5:
                p5 = m.group(5)
            if m.lastindex >= 6:
                p6 = m.group(6)
            if p1 == '' or None:
                self.txt.insert(END, '没有匹配到省份\n')
            if p2 == '' or None:
                self.txt.insert(END, '没有匹配到市或区\n')
            if p3 == '' or None:
                self.txt.insert(END, '没有匹配到县城或区\n')
            if p4 == '':
                p4 = '人民政府'
            out = '%s|%s|%s|%s|%s|%s' % (p1, p2, p3, p4, p5, p6)
            print(out)
            requests.packages.urllib3.disable_warnings()
            url = 'https://p.kuaidi100.com/apicenter/order.do?method=expressStopInquiries'
            header = {'Host': 'p.kuaidi100.com', 'Connection': 'keep-alive', 'xweb_xhr': '1',
                      'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF',
                      'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*',
                      'Sec-Fetch-Site': 'cross-site',
                      'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                      'Referer': 'https://servicewechat.com/wx6885acbedba59c14/683/page-frame.html',
                      'Accept-Language': 'en-us,en',
                      'Accept-Encoding': 'gzip, deflate', 'Content-Length': '476'}
            data = {'platform': 'WWW', 'toProvince': p1, 'toCity': p2, 'toArea': p3,
                    'toAddress': p4+p5+p6}
 
            res = requests.request(method='POST', url=url, headers=header, data=data, verify=False)
 
            res = res.json()
            # print(res)
            kuaidi = res['data']['toReachable']
            for i in kuaidi:
                if i['expressCode'] == 'yuantong':
                    i['expressCode'] = '圆通'
                if i['expressCode'] == 'shentong':
                    i['expressCode'] = '申通'
                if i['expressCode'] == 'zhongtong':
                    i['expressCode'] = '中通'
                if i['expressCode'] == 'yunda':
                    i['expressCode'] = '韵达'
                if i['expressCode'] == 'jtexpress':
                    i['expressCode'] = '极兔'
                if i['expressCode'] == 'debangkuaidi':
                    i['expressCode'] = '德邦'
                if i['expressCode'] == 'jd':
                    i['expressCode'] = '京东'
                if i['expressCode'] == 'shunfeng':
                    i['expressCode'] = '顺丰'
                if i['expressCode'] == 'youzhengguonei':
                    i['expressCode'] = '邮政'
            for i in kuaidi:
 
                if i['reachable'] == 1:
                    s = str(i['expressCode'] + '：已经开通\n')
                    self.txt.insert(END, s)
                if i['reachable'] == 0:
                    s = str(i['expressCode'] + '：停发\n')
                    self.txt.insert(END, s)
 
        else :
 
            requests.packages.urllib3.disable_warnings()
            url = 'https://p.kuaidi100.com/apicenter/order.do?method=expressStopInquiries'
            header = {'Host': 'p.kuaidi100.com', 'Connection': 'keep-alive', 'xweb_xhr': '1',
                      'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF',
                      'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'Sec-Fetch-Site': 'cross-site',
                      'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty',
                      'Referer': 'https://servicewechat.com/wx6885acbedba59c14/683/page-frame.html', 'Accept-Language': 'en-us,en',
                      'Accept-Encoding': 'gzip, deflate', 'Content-Length': '476'}
            self.province=self.send_email_entry.get()
            self.city=self.send_get_entry.get()
            self.area=self.set_subject_entry.get()
            self.adddress=self.send_get_name_entry.get()
            data = {'platform': 'WWW', 'toProvince':self.province , 'toCity':self.city , 'toArea':self.area , 'toAddress': self.adddress }
 
            res = requests.request(method='POST', url=url, headers=header, data=data, verify=False)
 
            res = res.json()
            #print(res)
            kuaidi = res['data']['toReachable']
            for i in kuaidi:
                if i['expressCode']=='yuantong':
                    i['expressCode']='圆通'
                if i['expressCode']=='shentong':
                    i['expressCode']='申通'
                if i['expressCode']=='zhongtong':
                    i['expressCode']='中通'
                if i['expressCode']=='yunda':
                    i['expressCode']='韵达'
                if i['expressCode'] == 'jtexpress':
                    i['expressCode'] = '极兔'
                if i['expressCode'] == 'debangkuaidi':
                    i['expressCode'] = '德邦'
                if i['expressCode'] == 'jd':
                    i['expressCode'] = '京东'
                if i['expressCode'] == 'shunfeng':
                    i['expressCode'] = '顺丰'
                if i['expressCode'] == 'youzhengguonei':
                    i['expressCode'] = '邮政'
            for i in kuaidi:
 
                if i['reachable'] == 1:
                    s=str(i['expressCode'] + '：已经开通\n')
                    self.txt.insert(END, s)
                if i['reachable'] ==0 :
                    s=str(i['expressCode'] + '：停发\n')
                    self.txt.insert(END, s)
 
    def thread(self):
        self.thread=threading.Thread(target=lambda :self.kuaidi())
        self.thread.setDaemon(True)
        self.thread.start()
if __name__=='__main__':
    jiemian()    