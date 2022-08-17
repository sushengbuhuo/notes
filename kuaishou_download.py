# -*- coding:utf-8 -*-
# @FileName  :mykuaishouUi.py https://www.52pojie.cn/thread-1668148-1-1.html
# @AuTho[url=home.php?mod=space&uid=686208]r[/url]    :kololi@52pojie
import os
import re
import subprocess
import threading
import time
import tkinter as tk
import tkinter.font as tkFont
import warnings
from datetime import datetime
 
import requests
 
LOG_LINE_NUM = 0
 
 
class App:
    def __init__(self, root):
        self.initUi(root)
        self.initData()
 
    def initData(self):
        self.urls = 'https://www.kuaishou.com/profile/3xqsuf66a4m3ujy'
        self.pcursor = ''
        self.nickname = ''
        self.datas = []
        self.status_download = True
        self.tag = 'odd'
        self.base_url = 'https://www.kuaishou.com/graphql'
        self.session = requests.Session()
        self.session.headers.update({
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'})
        self.starurl = 'https://www.kuaishou.com/brilliant'
        self.postdata = {
            "operationName span>": "visionProfilePhotoList",  # 对你没看错，就是有个”span>“
            "variables": {"userId": "3xn6jcvx7j3g2d2", "pcursor": "", "page": "profile"},
            "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  likeCount\n  viewCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n"
        }
 
    def initUi(self, root):
        # setting title
        root.title("KSDownloader kololi@52pojie")
        # setting window size
        width = 897
        height = 533
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
 
        ft = tkFont.Font(family='宋体', size=10)
        GLabel_515 = tk.Label(root)
        GLabel_515["font"] = ft
        GLabel_515["justify"] = "center"
        GLabel_515["text"] = "作者ID"
        GLabel_515.place(x=20, y=10, width=47, height=30)
 
        self.GLineEdit_508 = tk.Entry(root)
        self.GLineEdit_508["borderwidth"] = "1px"
        self.GLineEdit_508["justify"] = "center"
        self.GLineEdit_508["text"] = "path"
        self.GLineEdit_508['state'] = 'readonly'
        self.GLineEdit_508.place(x=90, y=50, width=610, height=30)
 
        self.GLineEdit_332 = tk.Entry(root)
        self.GLineEdit_332["borderwidth"] = "1px"
        self.GLineEdit_332["justify"] = "center"
        self.GLineEdit_332["text"] = "url"
        self.GLineEdit_332.place(x=90, y=10, width=231, height=30)
 
        self.GButton_333 = tk.Button(root)
        self.GButton_333["justify"] = "center"
        self.GButton_333["text"] = "开始下载"
        self.GButton_333.place(x=710, y=50, width=90, height=30)
        self.GButton_333['state'] = 'disable'
        self.GButton_333["command"] = self.GButton_333_command
 
        ft2 = tkFont.Font(family='宋体', size=12)
        self.GLineEdit_428 = tk.Text(root)
        self.GLineEdit_428["borderwidth"] = "1px"
        self.GLineEdit_428["font"] = ft2
        self.GLineEdit_428.place(x=10, y=90, width=881, height=427)
 
        self.GButton_676 = tk.Button(root)
        self.GButton_676["font"] = ft
        self.GButton_676["justify"] = "center"
        self.GButton_676["text"] = "停止下载"
        self.GButton_676['state'] = 'disable'
        self.GButton_676.place(x=810, y=50, width=74, height=30)
        self.GButton_676["command"] = self.GButton_676_command
 
        GButton_701 = tk.Button(root)
        GButton_701["font"] = ft
        GButton_701["justify"] = "center"
        GButton_701["text"] = "获取信息"
        GButton_701.place(x=330, y=10, width=70, height=30)
        GButton_701["command"] = self.GButton_701_command
 
        GLabel_100 = tk.Label(root)
        GLabel_100["font"] = ft
        GLabel_100["justify"] = "center"
        GLabel_100["text"] = "昵称"
        GLabel_100.place(x=410, y=10, width=43, height=30)
 
        GLabel_1 = tk.Label(root)
        GLabel_1["font"] = ft
        GLabel_1["justify"] = "center"
        GLabel_1["text"] = "条作品"
        GLabel_1.place(x=790, y=10, width=76, height=30)
 
        self.GLineEdit_690 = tk.Entry(root)
        self.GLineEdit_690["borderwidth"] = "1px"
        self.GLineEdit_690["font"] = ft
        self.GLineEdit_690["justify"] = "center"
        self.GLineEdit_690["text"] = "条作品"
        self.GLineEdit_690['state'] = 'readonly'
        self.GLineEdit_690.place(x=710, y=10, width=90, height=30)
 
        self.GLineEdit_281 = tk.Entry(root)
        self.GLineEdit_281["borderwidth"] = "1px"
        self.GLineEdit_281["font"] = ft
        self.GLineEdit_281["fg"] = "#333333"
        self.GLineEdit_281["justify"] = "center"
        self.GLineEdit_281["text"] = "昵称"
        self.GLineEdit_281['state'] = 'readonly'
        self.GLineEdit_281.place(x=460, y=10, width=240, height=31)
 
        GButton_55 = tk.Button(root)
        GButton_55["bg"] = "#efefef"
        GButton_55["font"] = ft
        GButton_55["fg"] = "#000000"
        GButton_55["justify"] = "center"
        GButton_55["text"] = "保存路径"
        GButton_55["relief"] = "groove"
        GButton_55.place(x=10, y=50, width=70, height=30)
        GButton_55["command"] = self.GButton_55_command
 
    def GButton_55_command(self):  # 打开文件夹
        path = self.GLineEdit_508.get()
        if path:
            self.open_fp(path)
 
    def GButton_701_command(self):  # 获取信息
        authorId = self.GLineEdit_332.get()
        self.status_download = True
        # self._log(authorId)
        if authorId:
            self.pcursor = ''
            self.postdata['variables']['userId'] = authorId
            self._log(f'--------------开始查询，请稍等-----------')
            obj1 = threading.Thread(target=self.analysis, args=({False}))
            obj1.setDaemon(True)
            obj1.start()
        else:
            self._log("请输入作者ID")
 
    def GButton_676_command(self):  # 停止下载
        self.status_download = False
        self.GButton_676['state'] = 'disable'
 
    def GButton_333_command(self):  # 开始下载
        self.status_download = True
        self.GButton_333['state'] = 'disable'
        self.GButton_676['state'] = 'active'
        self.pcursor = ''
        obj1 = threading.Thread(target=self.analysis, args=({True}))
        obj1.setDaemon(True)
        obj1.start()
 
    def analysis(self, flag):
        print(flag)
        page_num = 0
        len_feeds = 0
        nickname = '未找到该ID用户或者暂未发布作品'
        self._requests('get', self.starurl, decode_level=3)
        self.pcursor == ''
        while self.status_download:
            if self.pcursor == 'no_more':
                if flag:
                    self._log(f'--------------已全部完成下载！-----------')
                else:
                    self._log(f'--------------查询完成！-----------')
                break
            elif not self.status_download:
                self._log(f'--------------已停止下载！-----while------')
                break
            else:
                page_num += 1
                self.postdata['variables']['pcursor'] = self.pcursor
                json_data = self._requests('post', self.base_url, decode_level=2, json=self.postdata)
                if not json_data:
                    self._log(f'获取视频列表失败')
                    break
                feeds = json_data['data']['visionProfilePhotoList']['feeds']
                if feeds and len(feeds) > 0:
                    # 下一页 链接pcursor导入data
                    self.pcursor = json_data['data']['visionProfilePhotoList']['pcursor']
                    if flag:
                        self._log(f'……………………………………开始下载第{page_num}页数据……………………………………')
                        for feed in feeds:
                            if not self.status_download:
                                self._log(f'--------------已停止下载！--feed---------')
                                break
                            self.download_photoUrl(feed)
                    else:
                        len_feeds += len(feeds)
                        nickname = feeds[0]['author']['name'] if feeds[0]['author']['name'] else "未知"
                        self.GButton_333['state'] = 'active'
                else:
                    if page_num == 1:
                        self._log("未找到该ID用户或该用户暂未发布作品")
                    break
        if not flag:
            filepath = os.getcwd() + '\\' + 'ksdownloads' + '\\' + nickname
            self.GLineEdit_690['state'] = 'normal'
            self.GLineEdit_281['state'] = 'normal'
            self.GLineEdit_508['state'] = 'normal'
            self.GLineEdit_508.delete(0, 'end')
            self.GLineEdit_281.delete(0, 'end')
            self.GLineEdit_690.delete(0, 'end')
            self.GLineEdit_690.insert(0, f'{len_feeds}')
            self.GLineEdit_281.insert(0, f'{nickname}')
            self.GLineEdit_508.insert(0, f'{filepath}')
            self.GLineEdit_690['state'] = 'readonly'
            self.GLineEdit_281['state'] = 'readonly'
            self.GLineEdit_508['state'] = 'readonly'
 
    def download_photoUrl(self, feed):
        try:
            filepath = os.getcwd() + '/' + 'ksdownloads' + '/' + feed['author']['name'] if feed['author'][
                'name'] else os.getcwd() + '/' + 'ksdownloads' + '/' + '未知用户'
            self.nickname = feed['author']['name'] if feed['author']['name'] else "未知"
            caption = feed['photo']['caption']  # title
            photoUrl = feed['photo']['photoUrl']  # video link
            caption = re.sub('[ \\/:*?"<>|\n\t]', '', caption)
            likeCount = feed['photo']['likeCount']
            viewCount = feed['photo']['viewCount']
            self._log(f'{caption} {viewCount}次观看 {likeCount}人喜欢')
            caption = caption[:28] if len(caption) > 28 else caption
            if caption:
                video_data = self._requests('get', photoUrl, decode_level=3).content
                time_ns = time.time()
                self.save_video(os.path.normpath(filepath), caption + '_' + str(time_ns) + '.mp4', video_data, photoUrl)
        except Exception as e:
            self._log(f'错误:{e},获取数据失败,请检查主播ID是否正确,也可能cookies已过期!')
 
    def save_video(self, path, filename, video_data, url):
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.normpath(os.path.join(path, filename)), 'wb') as f:
            f.write(video_data)
            now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._log(f'  状态:[下载完成]')
            self.datas.append([now_time, filename, path, url])
 
    def open_fp(self, fp):
        """
        打开文件或文件夹
        :param fp: 需要打开的文件或文件夹路径
        """
        import platform
        systemType: str = platform.platform()  # 获取系统类型
        if 'mac' in systemType:  # 判断以下当前系统类型
            fp: str = fp.replace("\\", "/")  # mac系统下,遇到`\\`让路径打不开,不清楚为什么哈,觉得没必要的话自己可以删掉啦,18行那条也是
            subprocess.call(["open", fp])
        else:
            fp: str = fp.replace("/", "\\")  # win系统下,有时`/`让路径打不开
            try:
                os.startfile(fp)
            except:
                self._log("文件还未下载")
 
    def _requests(self, method, url, decode_level=1, retry=0, timeout=15, **kwargs):
        if method in ["get", "post"]:
            for _ in range(retry + 1):
                try:
                    warnings.filterwarnings('ignore')
                    response = getattr(self.session, method)(url, timeout=timeout, verify=False, **kwargs)
                    return response.text if decode_level == 1 else response.json() if decode_level == 2 else response
                except Exception as e:
                    self._log(e)
 
        return None
 
    def _log(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        self.GLineEdit_428.tag_config("even", background='#e0e0e0')
        self.GLineEdit_428.tag_config("odd", background='#ffffff')
        self.tag = 'odd' if self.tag == 'even' else 'even'
        if LOG_LINE_NUM <= 20:
 
            self.GLineEdit_428.insert('end', logmsg_in, self.tag)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.GLineEdit_428.delete(1.0, 2.0)
            self.GLineEdit_428.insert('end', logmsg_in, self.tag)
 
    def get_current_time(self):
        current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return current_time
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()