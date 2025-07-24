import requests
import re
import os
import time
import sys
import html
import demjson
import urllib3
from random import randint
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QFrame, QProgressBar, QMessageBox, 
                            QFileDialog, QGroupBox, QStatusBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class DownloadThread(QThread):
    """下载线程，处理网络请求和文件下载"""
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool)
    
    def __init__(self, url, headers):
        super().__init__()
        self.url = url
        self.headers = headers
        self.is_running = True
        
    def run(self):
        """线程执行函数"""
        try:
            self.log_signal.emit(f"本工具由微信公众号 苏生不惑 开发，更新于2025年7月25日，获取所有文章阅读数留言数据微信联系sushengbuhuo")
            self.status_signal.emit("正在分析文章...")
            self.log_signal.emit(f"开始处理链接：{self.url}")
            
            # 获取初始页面
            response = requests.get(self.url, headers=self.headers, timeout=30)
            
            # 提取页面中的所有文章链接 https://mp.weixin.qq.com/s/N06MuZ4ZFv2AtzDcLpzVxw https://mp.weixin.qq.com/s/1giyAGqs1kV4c_WuCX29KA 
            urls = re.findall('<a.*?href="(https?://mp.weixin.qq.com/s\?.*?)"', response.text);urls=[]
            urls.insert(0, self.url)  # 将原始链接放在第一位
            urls = [x for x in urls if x != '']
            
            self.log_signal.emit(f"找到 {len(urls)} 篇文章链接")
            total_links = len(urls)
            # if int(time.time()) > 1756723002:
            #     self.log_signal.emit(f"未知错误，获取最新可用版本关注公众号 苏生不惑")
            #     return
            # 处理每个链接
            for i, mp_url in enumerate(urls):
                if not self.is_running:
                    break
                    
                self.status_signal.emit(f"正在处理链接 {i+1}/{total_links}")
                self.progress_signal.emit(int((i+1) / total_links * 100))
                self.log_signal.emit(f"\n处理第 {i+1}/{total_links} 个链接：{mp_url}")
                
                try:
                    # 获取文章内容
                    res = requests.get(html.unescape(mp_url), proxies={'http': None, 'https': None}, verify=False, headers=self.headers, timeout=30)
                    content = res.text.replace('data-src', 'src').replace('//res.wx.qq.com', 'https://res.wx.qq.com')
                    
                    # 随机延时，避免请求过于频繁
                    delay = randint(1, 2)
                    time.sleep(delay)
                    
                    # 提取文章标题和时间
                    title = re.search(r'var msg_title = \'(.*)\'', content) or re.search(r'window.title = "(.*)"', content)
                    ct = re.search(r'var ct = "(.*)";', content) or re.search(r"d\.ct = xml \? getXmlValue\('ori_create_time\.DATA'\) \: '(.*)'", content)
                    
                    if not title:
                        title = re.search(r'window\.msg_title = \'(.*?)\'', content)
                    if not ct:
                        ct = re.search(r'window\.ct = \'(.*?)\'', content)
                    
                    if title and ct:
                        title = title.group(1)
                        ct = ct.group(1)
                        date = time.strftime('%Y-%m-%d', time.localtime(int(ct)))
                        
                        self.log_signal.emit(f'开始下载：{date} {title}')
                        
                        # 下载视频
                        self.video(res, date, title, mp_url)
                        self.images(res, self.headers,date, title)
                        self.cover(res, self.headers,date, title)
                        self.audio(res, self.headers,date, title)
                    else:
                        self.log_signal.emit("无法下载文章，跳过此链接")
                        
                except Exception as e:
                    self.log_signal.emit(f"处理链接时出错：{str(e)}")
                    continue
            
            if self.is_running:
                self.status_signal.emit("下载完成")
                self.log_signal.emit("\n下载完成！")
                self.finished_signal.emit(True)
            else:
                self.log_signal.emit("\n下载已中断")
                self.finished_signal.emit(False)
                
        except Exception as e:
            self.log_signal.emit(f"下载过程中发生错误：{str(e)}")
            self.finished_signal.emit(False)
    def replace_name(self, filename):
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*','\n','#']
        for char in invalid_chars:
            filename = filename.replace(char, ' ')
        return filename        
    def images(self, res,headers,date,title):
        if not self.is_running:
            return
            
        if not os.path.exists('images'):
            os.makedirs('images')
        imgs=re.findall('data-src="(.*?)"',res.text)
        imgs2= re.findall("cdn_url: '(.*?)',",res.text)
        imgs.extend(imgs2)
        time.sleep(1)
        num = 0;
        title=date+'_'+self.replace_name(html.unescape(title.replace('.','')))
        for i in imgs:
            if not re.match(r'^https?://.*',i):
                continue
            num+=1
            img_data = requests.get(i,headers=headers)
            self.log_signal.emit('正在下载图片：'+i)
            ext = '.jpg'
            if 'wx_fmt=gif' in i:
                ext = '.gif'
            with open(f'images/'+title+'_'+str(num)+ext,'wb') as f6:
                f6.write(img_data.content)
        
    def cover(self, res,headers,date,title):
        if not self.is_running:
            return
            
        if not os.path.exists('cover'):
            os.makedirs('cover')
        cover_url = re.search(r'<meta property="og:image" content="(.*)"\s?/>', res.text)
        if not cover_url:
            return False
        cover_url = cover_url.group(1)
        if not cover_url:
            return False
        cover_data = requests.get(cover_url,headers=headers)
        self.log_signal.emit('正在下载封面：'+cover_url)
        with open('cover/'+date+'_'+self.replace_name(title)+'.jpg','wb') as f:
            f.write(cover_data.content)
    def audio(self, res,headers,date,title):
        if not self.is_running:
            return
        if not os.path.exists('audio'):
            os.makedirs('audio')
        aids = re.findall(r'"voice_id":"(.*?)"',res.text)
        if not aids:
            aids = re.findall(r'voiceid\s*:\s*"(.*?)"',res.text)
        time.sleep(2)
        tmp = 0
        for id in aids:
            tmp +=1
            url = f'https://res.wx.qq.com/voice/getvoice?mediaid={id}'
            audio_data = requests.get(url,headers=headers)
            if not audio_data.content:
                continue
            self.log_signal.emit('正在下载音频：'+title+'.mp3')
            with open('audio/'+date+'_'+self.replace_name(title)+'_'+str(tmp)+'.mp3','wb') as f5:
                f5.write(audio_data.content)
    def video(self, res, date, title, article_url):
        """下载视频文件"""
        if not self.is_running:
            return
            
        if not os.path.exists('video'):
            os.makedirs('video')
            self.log_signal.emit("创建视频保存文件夹")
            
        # 尝试从响应中提取视频信息
        vinfo = re.findall(r'window\.__mpVideoTransInfo\s+\=\s+([\s\S]*?)\];', res.text, flags=re.S)
        if not vinfo:
            vinfo = re.findall(r'mp_video_trans_info:\s+([\s\S]*?)\],', res.text, flags=re.S)
            
        num = 0
        for v in vinfo:
            if not self.is_running:
                return
                
            v_url = re.search(r"url:\s+'(.*?)',", v)
            if not v_url:
                v_url = re.search(r"url:\s+\('(.*?)'\)", v)
                
            if v_url:
                video_url = html.unescape(v_url.group(1).replace(r'\x26', '&'))
                num += 1
                self.log_signal.emit(f'正在下载视频：{title}.mp4 ({num}/{len(vinfo)})')
                
                try:
                    # 下载视频
                    video_data = requests.get(video_url, headers=self.headers, timeout=30)
                    
                    # 保存视频链接到CSV文件
                    # with open('视频链接合集.csv', 'a+', encoding='utf-8-sig') as f4:
                        # f4.write(f'{date},{title},{video_url},{article_url}\n')
                    title = self.replace_name(title)
                    # 保存视频文件
                    filename = f'video/{date}_{title}_{str(num)}.mp4'
                    with open(filename, 'wb') as f:
                        f.write(video_data.content)
                    
                    self.log_signal.emit(f'视频下载完成：{filename}')
                    
                except Exception as e:
                    self.log_signal.emit(f'下载视频失败：{str(e)}')
                
                # 随机延时，避免请求过于频繁
                delay = randint(1, 2)
                time.sleep(delay)
                
    def stop(self):
        """停止线程运行"""
        self.is_running = False
        self.wait()

class WeChatVideoDownloader(QMainWindow):
    """微信公众号视频下载器主窗口"""
    def __init__(self):
        super().__init__()
        
        # 设置中文字体
        font = QFont()
        font.setFamily("SimHei")
        font.setPointSize(10)
        self.setFont(font)
        
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
            'referer': 'https://mp.weixin.qq.com',
        }
        
        # 初始化UI
        self.init_ui()
        
        # 状态变量
        self.download_thread = None
        self.is_downloading = False
        
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口标题和大小
        self.setWindowTitle("微信公众号图片视频音频下载器 by微信公众号 苏生不惑，获取所有文章阅读数留言数据微信联系sushengbuhuo")
        self.setGeometry(300, 300, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # URL输入区域
        url_group = QGroupBox("输入公众号文章链接")
        url_layout = QHBoxLayout()
        
        url_label = QLabel("链接:")
        self.url_input = QLineEdit("")
        self.url_input.setMinimumWidth(500)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        
        url_group.setLayout(url_layout)
        main_layout.addWidget(url_group)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        self.download_btn = QPushButton("开始下载")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.clicked.connect(self.start_download)
        
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_download)
        
        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.clicked.connect(self.clear_log)
        
        btn_layout.addWidget(self.download_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(btn_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # 日志区域
        log_group = QGroupBox("下载日志")
        log_layout = QVBoxLayout()
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setLineWrapMode(QTextEdit.WidgetWidth)
        
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group, 1)  # 让日志区域占据剩余空间
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
    def log(self, message):
        """添加日志到日志区域"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.append(f"[{timestamp}] {message}")
        
    def update_status(self, message):
        """更新状态栏消息"""
        self.statusBar.showMessage(message)
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        
    def start_download(self):
        """开始下载过程"""
        url = self.url_input.text().strip()
        if not url or url == "https://mp.weixin.qq.com/s/":
            url = 'https://mp.weixin.qq.com/s/3FITW3SXv8JGBkYD8SsW_g'
            # QMessageBox.critical(self, "错误", "请输入有效的公众号文章链接")
            # return
        
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.download_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # 创建并启动下载线程
        self.download_thread = DownloadThread(url, self.headers)
        self.download_thread.log_signal.connect(self.log)
        self.download_thread.status_signal.connect(self.update_status)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()
        
    def stop_download(self):
        """停止下载过程"""
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.stop()
            
        self.is_downloading = False
        self.download_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.update_status("已停止")
        self.log("下载已停止")
        
    def clear_log(self):
        """清空日志区域"""
        self.log_output.clear()
        
    def download_finished(self, success):
        """下载完成回调函数"""
        self.is_downloading = False
        self.download_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            QMessageBox.information(self, "完成", "下载完成！")
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.is_downloading:
            reply = QMessageBox.question(
                self, '确认', '正在下载中，是否要退出程序？',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
            if reply == QMessageBox.Yes:
                self.stop_download()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置全局样式
    app.setStyle('Fusion')
    
    # 确保中文正常显示
    font = QFont("SimHei")
    app.setFont(font)
    
    window = WeChatVideoDownloader()
    window.show()
    sys.exit(app.exec_())