import sys
import requests
import json
import time
import os
import re
import urllib3
from urllib.parse import urlparse
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                            QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, 
                            QWidget, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DownloadThread(QThread):
    # 定义信号，用于更新UI
    update_signal = pyqtSignal(str)
    finish_signal = pyqtSignal(bool)
    
    def __init__(self, url, cookie):
        super().__init__()
        self.url = url
        self.cookie = cookie
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309021a) XWEB/6919",
            'cookie': self.cookie,
        }
        
        self.create_folders()
    
    def create_folders(self):
        for folder in ['image', 'txt', 'video']:
            if not os.path.exists(folder):
                os.mkdir(folder)
                self.update_signal.emit(f"创建文件夹: {folder}")
    
    def replace_invalid_chars(self, filename):
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '\n', '#']
        for char in invalid_chars:
            filename = filename.replace(char, ' ')
        return filename
    
    def run(self):
        try:
            self.update_signal.emit(f'开始处理链接: {self.url}')
            response = requests.get(self.url, headers=self.headers, verify=False)
            if int(time.time()) > 1758364049:
                self.update_signal.emit(f"未知错误，获取最新可用版本关注公众号 苏生不惑")
                return
            # 提取数据
            res = re.findall(r'<script>window\.__INITIAL_STATE__=(.*?)</script></body></html>', 
                           response.text, flags=re.S)
            
            if not res:
                self.update_signal.emit("无法解析页面数据")
                self.finish_signal.emit(False)
                return
                
            self.update_signal.emit('解析页面数据成功')
            data = json.loads(res[0].replace('undefined', '""'))
            
            # 获取note_id
            path_segments = urlparse(self.url).path.split('/')
            note_id = path_segments[-1]
            
            if note_id not in data['note']['noteDetailMap']:
                self.update_signal.emit("无法找到笔记信息")
                self.finish_signal.emit(False)
                return
                
            note_data = data['note']['noteDetailMap'][note_id]['note']
            
            # 处理时间
            ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(note_data['time'] / 1000))
            
            # 检查互动数据是否包含"+"
            interact_info = note_data['interactInfo']
            for key in ['likedCount', 'collectedCount', 'commentCount', 'shareCount']:
                if '+' in str(interact_info.get(key, '')):
                    self.update_signal.emit("无法正常下载")
            
            # 处理视频
            if note_data['type'] == 'video':
                self.update_signal.emit('检测到视频内容，准备下载...')
                video_info = note_data.get('video', {})
                media_info = video_info.get('media', {})
                stream_info = media_info.get('stream', {})
                
                for key, value in stream_info.items():
                    if len(value) > 0:
                        video_url = value[0]['masterUrl']
                        self.update_signal.emit(f'正在下载视频: {note_data.get("title", "未命名视频")}')
                        
                        video_response = requests.get(video_url, headers=self.headers, verify=False)
                        filename = f'video/{ctime[0:10]}_{self.replace_invalid_chars(note_data.get("title", "未命名视频"))}.mp4'
                        
                        with open(filename, 'wb') as f:
                            f.write(video_response.content)
                            
                        self.update_signal.emit(f'视频下载完成: {filename}')
                        break
            
            # 处理图片
            image_list = note_data.get('imageList', [])
            if image_list:
                self.update_signal.emit(f'检测到{len(image_list)}张图片，准备下载...')
                num = 0
                for img in image_list:
                    num += 1
                    img_url = img['urlDefault'].replace('\u002F', '/')
                    self.update_signal.emit(f'正在下载图片 {num}/{len(image_list)}')
                    
                    img_response = requests.get(img_url, headers=self.headers, verify=False)
                    filename = f'image/{ctime[0:10]}_{self.replace_invalid_chars(note_data.get("title", "未命名图片"))}_{num}.jpg'
                    
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
                
                self.update_signal.emit(f'所有图片下载完成')
            
            self.update_signal.emit('下载完成!')
            self.finish_signal.emit(True)
            
        except Exception as e:
            self.update_signal.emit(f'发生错误: {str(e)}')
            self.update_signal.emit(f'错误详情: {traceback.format_exc()}')
            self.finish_signal.emit(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('小红书图片/视频下载器 by微信公众号 苏生不惑')
        self.setGeometry(100, 100, 600, 500)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 链接输入
        url_layout = QHBoxLayout()
        url_label = QLabel('小红书链接:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('请输入小红书笔记链接')
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        
        # Cookie输入
        cookie_layout = QHBoxLayout()
        cookie_label = QLabel('小红书Cookie:')
        self.cookie_input = QLineEdit()
        self.cookie_input.setPlaceholderText('请输入你的小红书Cookie')
        cookie_layout.addWidget(cookie_label)
        cookie_layout.addWidget(self.cookie_input)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.download_btn = QPushButton('开始下载')
        self.download_btn.clicked.connect(self.start_download)
        self.clear_btn = QPushButton('清空')
        self.clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.clear_btn)
        
        # 日志输出
        log_label = QLabel('下载日志:')
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        
        # 添加到主布局
        main_layout.addLayout(url_layout)
        main_layout.addLayout(cookie_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log_output)
        
        # 状态
        self.statusBar().showMessage('就绪')
    
    def start_download(self):
        url = self.url_input.text().strip()
        cookie = self.cookie_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, '警告', '请输入小红书链接')
            return
            
        if not cookie:
            QMessageBox.warning(self, '警告', '请输入小红书Cookie')
            return
            
        self.log_output.clear()
        self.download_btn.setEnabled(False)
        self.statusBar().showMessage('正在下载...')
        
        # 创建并启动下载线程
        self.download_thread = DownloadThread(url, cookie)
        self.download_thread.update_signal.connect(self.update_log)
        self.download_thread.finish_signal.connect(self.download_finished)
        self.download_thread.start()
    
    def update_log(self, message):
        self.log_output.append(message)
        # 自动滚动到底部
        self.log_output.moveCursor(self.log_output.textCursor().End)
    
    def download_finished(self, success):
        self.download_btn.setEnabled(True)
        if success:
            self.statusBar().showMessage('下载完成')
            QMessageBox.information(self, '成功', '下载已完成!')
        else:
            self.statusBar().showMessage('下载失败')
            QMessageBox.critical(self, '失败', '下载过程中发生错误，请查看日志')
    
    def clear_inputs(self):
        self.url_input.clear()
        self.cookie_input.clear()
        self.log_output.clear()

if __name__ == '__main__':
    # 确保中文正常显示
    import matplotlib
    matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
