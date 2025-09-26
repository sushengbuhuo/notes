import sys
import os
import re
import html
import time
import random
import traceback
import urllib3
import requests
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QProgressBar, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DownloadThread(QThread):
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    download_complete = pyqtSignal(str)
    update_total_progress = pyqtSignal(int)
    
    def __init__(self, url, cookie, save_dir):
        super().__init__()
        self.url = url
        self.cookie = cookie
        self.save_dir = save_dir
        
    def run(self):
        try:
            self.update_status.emit("本工具由微信公众号 苏生不惑 开发，更新于2025年9月25日，获取所有微博数据微信联系sushengbuhuo")
            # if int(time.time()) > 1761373182:
            #     self.update_status.emit(f"未知错误，获取最新可用版本关注公众号 苏生不惑 ，回复 微博")
            #     return
            self.update_status.emit("正在解析微博链接...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat",
                'referer': 'https://weibo.com/1744395855/NkD5bjvPC',
                "Cookie": self.cookie,
            }
            
            # 解析URL获取mid
            m = re.search(r'https://(www\.)?weibo\.com/\d+/(.*)', self.url)
            if not m:
                self.update_status.emit("错误: 无效的微博链接")
                self.download_complete.emit("failed")
                return
                
            mid_code = m.group(2)
            mid = self.reverse_cut_to_length(mid_code, self.base62_decode, 4, 7)
            
            # 获取微博内容
            api_url = f'https://weibo.com/ajax/statuses/show?id={mid}&locale=zh-CN&isGetLongText=true'
            # self.update_status.emit(f"正在获取微博内容: {api_url}")
            res = requests.get(html.unescape(api_url), 
                              proxies={'http': None, 'https': None}, 
                              verify=False, headers=headers).json()
            
            # 解析创建时间
            dt_obj = datetime.strptime(res['created_at'], '%a %b %d %H:%M:%S %z %Y')
            
            # 创建保存目录
            image_dir = os.path.join(self.save_dir, 'image')
            video_dir = os.path.join(self.save_dir, 'video')
            
            for dir_path in [image_dir, video_dir]:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                    self.update_status.emit(f"创建目录: {dir_path}")
            
            # 下载图片 https://weibo.com/1660925262/Q5KRBjkKR
            total_items = 0
            completed_items = 0
            
            if 'pic_infos' in res:
                pic_infos = res['pic_infos']
                total_items += len(pic_infos)
                self.update_total_progress.emit(0)
                
                for i, (j, k) in enumerate(pic_infos.items()):
                    img_url = k['largest']['url'].replace('/large/', '/oslarge/')
                    self.update_status.emit(f"正在下载图片 {i+1}/{len(pic_infos)}: {k['largest']['url']}")
                    if k['type'] == 'livephoto':#https://weibo.com/6386087847/Q1uZVtDpf
                        try:
                            img_data = requests.get(k['video'], headers=headers, timeout=10)
                            img_path = os.path.join(video_dir, self.replace_invalid_chars(f"{dt_obj.strftime('%Y-%m-%d')}-{mid}-{k['fid']}.mp4"))
                            
                            with open(img_path, 'wb') as f:
                                f.write(img_data.content)
                                
                            completed_items += 1
                            progress = int(completed_items / total_items * 100)
                            self.update_total_progress.emit(progress)
                            self.update_status.emit(f"livephoto下载完成")
                            
                        except Exception as e:
                            self.update_status.emit(f"下载livephoto失败: {str(e)}")
                            traceback.print_exc()
                    ext='.jpg'
                    if k['type'] == 'gif':
                        ext='.gif'
                        try:
                            v_data = requests.get(k['video'], headers=headers, timeout=10)
                            v_path = os.path.join(video_dir, self.replace_invalid_chars(f"{dt_obj.strftime('%Y-%m-%d')}-{mid}-{k['video_object_id']}.mp4"))
                            self.update_status.emit(f"正在下载视频 {v_path}: {k['video']}")
                            with open(v_path, 'wb') as f:
                                f.write(v_data.content)
                                
                            completed_items += 1
                            progress = int(completed_items / total_items * 100)
                            self.update_total_progress.emit(progress)
                            self.update_status.emit(f"视频下载完成")
                            
                        except Exception as e:
                            self.update_status.emit(f"下载视频失败: {str(e)}")
                            traceback.print_exc()
                    try:
                        img_data = requests.get(img_url, headers=headers, timeout=10)
                        img_path = os.path.join(image_dir, f"{dt_obj.strftime('%Y-%m-%d')}-{mid}-{j}{ext}")
                        
                        with open(img_path, 'wb') as f:
                            f.write(img_data.content)
                            
                        completed_items += 1
                        progress = int(completed_items / total_items * 100)
                        self.update_total_progress.emit(progress)
                        self.update_status.emit(f"图片 {i+1}/{len(pic_infos)} 下载完成")
                        
                    except Exception as e:
                        self.update_status.emit(f"下载图片失败: {str(e)}")
                        traceback.print_exc()

            # 下载视频
            if 'page_info' in res and 'media_info' in res.get('page_info', {}) and \
               'playback_list' in res.get('page_info', {}).get('media_info', {}):
                
                media_info = res['page_info']['media_info']
                playback_list = media_info.get('playback_list', [])
                
                if playback_list:
                    total_items += 1
                    video_info = playback_list[0].get('play_info', {})
                    video_url = video_info.get('url')
                    
                    if video_url:
                        title = f"{media_info.get('name', 'video')}{res['page_info'].get('object_id')}"
                        title = self.replace_invalid_chars(title)
                        self.update_status.emit(f"正在下载视频: {video_url}")
                        
                        try:
                            video_path = os.path.join(video_dir, f"{dt_obj.strftime('%Y-%m-%d')}-{title}.mp4")
                            
                            # 流式下载视频
                            response = requests.get(video_url, headers=headers, verify=False, stream=True, timeout=30)
                            total_size = int(response.headers.get('content-length', 0))
                            block_size = 1024
                            self.update_progress.emit(0)
                            
                            with open(video_path, 'wb') as f:
                                for data in response.iter_content(block_size):
                                    if not self.isRunning():
                                        self.update_status.emit("下载已取消")
                                        return
                                        
                                    f.write(data)
                                    if total_size > 0:
                                        progress = int(len(data) / total_size * 100)
                                        self.update_progress.emit(progress)
                            
                            completed_items += 1
                            progress = int(completed_items / total_items * 100)
                            self.update_total_progress.emit(progress)
                            self.update_status.emit("视频下载完成")
                        except Exception as e:
                            self.update_status.emit(f"下载视频失败: {str(e)}")
                            traceback.print_exc()
            # 图片和视频 https://weibo.com/1742566624/Q6bhCD1mR https://weibo.com/1727858283/Q69VVw1hu
            if 'mix_media_info' in res and 'items' in res.get('mix_media_info', {}):
                items_info = res['mix_media_info']['items']
                for item in items_info:
                    total_items += 1
                    if item['type'] == 'pic':
                        img_url = item['data']['largest']['url'].replace('/large/', '/oslarge/')
                        self.update_status.emit(f"正在下载图片 : {item['data']['largest']['url']}")
                        ext='.jpg'
                        if item['data']['type'] == 'gif':#https://weibo.com/6554180184/Meqja1JiZ
                            ext='.gif'
                            try:
                                v_data = requests.get(item['data']['video'], headers=headers, timeout=10)
                                v_path = os.path.join(video_dir, self.replace_invalid_chars(f"{dt_obj.strftime('%Y-%m-%d')}-{mid}-{item['data']['video_object_id']}.mp4"))
                                
                                with open(v_data, 'wb') as f:
                                    f.write(v_path.content)
                                    
                                completed_items += 1
                                progress = int(completed_items / total_items * 100)
                                self.update_total_progress.emit(progress)
                                self.update_status.emit(f"视频下载完成")
                                
                            except Exception as e:
                                self.update_status.emit(f"下载视频失败: {str(e)}")
                                traceback.print_exc()
                        try:
                            img_data = requests.get(img_url, headers=headers, timeout=10)
                            img_path = os.path.join(image_dir, f"{dt_obj.strftime('%Y-%m-%d')}-{mid}-{item['id']}{ext}")
                            
                            with open(img_path, 'wb') as f:
                                f.write(img_data.content)
                                
                            completed_items += 1
                            progress = int(completed_items / total_items * 100)
                            self.update_total_progress.emit(progress)
                            self.update_status.emit(f"图片下载完成")
                            
                        except Exception as e:
                            self.update_status.emit(f"下载图片失败: {str(e)}")
                            traceback.print_exc()
                        if item['data']['type'] == 'livephoto':
                            try:
                                img_data = requests.get(item['data']['video'], headers=headers, timeout=10)
                                img_path = os.path.join(video_dir, self.replace_invalid_chars(f"{dt_obj.strftime('%Y-%m-%d')}-{mid}-{item['data']['fid']}.mp4"))
                                
                                with open(img_path, 'wb') as f:
                                    f.write(img_data.content)
                                    
                                completed_items += 1
                                progress = int(completed_items / total_items * 100)
                                self.update_total_progress.emit(progress)
                                self.update_status.emit(f"livephoto下载完成")
                                
                            except Exception as e:
                                self.update_status.emit(f"下载livephoto失败: {str(e)}")
                                traceback.print_exc()
                    if item['type'] == 'video':
                        media_info = item['data']['media_info']
                        playback_list = media_info.get('playback_list', [])
                        video_info = playback_list[0].get('play_info', {})
                        video_url = video_info.get('url')
                        
                        if video_url:
                            title = f"{media_info.get('name', 'video')}{item['data'].get('object_id')}"
                            title = self.replace_invalid_chars(title)
                            self.update_status.emit(f"正在下载视频: {video_url}")
                            
                            try:
                                video_path = os.path.join(video_dir, f"{dt_obj.strftime('%Y-%m-%d')}-{title}.mp4")
                                
                                # 流式下载视频
                                response = requests.get(video_url, headers=headers, verify=False, stream=True, timeout=30)
                                total_size = int(response.headers.get('content-length', 0))
                                block_size = 1024
                                self.update_progress.emit(0)
                                
                                with open(video_path, 'wb') as f:
                                    for data in response.iter_content(block_size):
                                        if not self.isRunning():
                                            self.update_status.emit("下载已取消")
                                            return
                                            
                                        f.write(data)
                                        if total_size > 0:
                                            progress = int(len(data) / total_size * 100)
                                            self.update_progress.emit(progress)
                                
                                completed_items += 1
                                progress = int(completed_items / total_items * 100)
                                self.update_total_progress.emit(progress)
                                self.update_status.emit("视频下载完成")
                            except Exception as e:
                                self.update_status.emit(f"下载视频失败: {str(e)}")
                                traceback.print_exc()
            if total_items == 0:
                self.update_status.emit("未找到可下载的内容")
            else:
                self.update_status.emit(f"下载完成! 共下载 {completed_items} 个文件")
            
            self.download_complete.emit("success")
            
        except Exception as e:
            error_msg = f"下载失败: {str(e)}"
            self.update_status.emit(error_msg)
            traceback.print_exc()
            self.download_complete.emit("failed")
    
    def replace_invalid_chars(self, filename):
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '\n', '#']
        for char in invalid_chars:
            filename = filename.replace(char, ' ')
        return filename
    
    def base62_encode(self, num, alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        num = int(num)
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            rem = num % base
            num = num // base
            arr.append(alphabet[rem])
        arr.reverse()
        return ''.join(arr)
    
    def base62_decode(self, string, alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        string = str(string)
        num = 0
        idx = 0
        for char in string:
            power = (len(string) - (idx + 1))
            num += alphabet.index(char) * (len(alphabet) ** power)
            idx += 1
        return num
    
    def reverse_cut_to_length(self, content, code_func, cut_num=4, fill_num=7):
        content = str(content)
        cut_list = [content[i - cut_num if i >= cut_num else 0:i] for i in range(len(content), 0, (-1 * cut_num))]
        cut_list.reverse()
        result = []
        for i, item in enumerate(cut_list):
            s = str(code_func(item))
            if i > 0 and len(s) < fill_num:
                s = (fill_num - len(s)) * '0' + s
            result.append(s)
        return ''.join(result)

class WeiboDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('微博无水印图片/视频下载器 by微信公众号 苏生不惑，获取所有微博数据微信联系sushengbuhuo')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # URL和Cookie输入部分
        input_layout = QVBoxLayout()
        
        # 微博链接输入
        url_layout = QHBoxLayout()
        url_label = QLabel('微博链接:')
        url_label.setFixedWidth(80)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('https://weibo.com/1744395855/OykWZj6Zt')
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        input_layout.addLayout(url_layout)
        
        # Cookie输入
        cookie_layout = QHBoxLayout()
        cookie_label = QLabel('微博Cookie:')
        cookie_label.setFixedWidth(80)
        self.cookie_input = QLineEdit()
        self.cookie_input.setPlaceholderText('请输入你的微博Cookie')
        cookie_layout.addWidget(cookie_label)
        cookie_layout.addWidget(self.cookie_input)
        input_layout.addLayout(cookie_layout)
        
        # 保存目录选择
        save_dir_layout = QHBoxLayout()
        save_dir_label = QLabel('保存目录:')
        save_dir_label.setFixedWidth(80)
        self.save_dir_input = QLineEdit()
        self.save_dir_input.setText(os.path.abspath(os.getcwd()))
        self.save_dir_input.setReadOnly(True)
        browse_btn = QPushButton('浏览...')
        browse_btn.clicked.connect(self.browse_save_dir)
        save_dir_layout.addWidget(save_dir_label)
        save_dir_layout.addWidget(self.save_dir_input)
        save_dir_layout.addWidget(browse_btn)
        input_layout.addLayout(save_dir_layout)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        self.download_btn = QPushButton('开始下载')
        self.download_btn.clicked.connect(self.start_download)
        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.download_btn)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addStretch(1)
        input_layout.addLayout(btn_layout)
        
        main_layout.addLayout(input_layout)
        
        # 进度条
        progress_layout = QVBoxLayout()
        progress_label = QLabel('下载进度:')
        self.total_progress = QProgressBar()
        self.total_progress.setRange(0, 100)
        self.total_progress.setValue(0)
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.total_progress)
        
        # 视频下载进度条（单独显示视频下载进度）
        video_progress_label = QLabel('视频下载进度:')
        self.video_progress = QProgressBar()
        self.video_progress.setRange(0, 100)
        self.video_progress.setValue(0)
        progress_layout.addWidget(video_progress_label)
        progress_layout.addWidget(self.video_progress)
        
        main_layout.addLayout(progress_layout)
        
        # 状态显示
        status_label = QLabel('状态:')
        main_layout.addWidget(status_label)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        main_layout.addWidget(self.status_text)
        
        # 设置布局比例
        main_layout.setStretch(0, 1)  # 输入部分
        main_layout.setStretch(1, 1)  # 进度条部分
        main_layout.setStretch(2, 6)  # 状态显示部分
        
        # 初始化状态
        self.update_status("请输入微博链接和Cookie，然后点击开始下载")
        
    def browse_save_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "选择保存目录", os.getcwd())
        if directory:
            self.save_dir_input.setText(directory)
            
    def update_status(self, message):
        self.status_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        self.status_text.verticalScrollBar().setValue(self.status_text.verticalScrollBar().maximum())
        
    def start_download(self):
        url = self.url_input.text().strip()
        cookie = self.cookie_input.text().strip()
        save_dir = self.save_dir_input.text().strip()
        
        if not url or not cookie:
            QMessageBox.warning(self, "警告", "微博链接和Cookie不能为空!")
            return
            
        if not os.path.exists(save_dir):
            try:
                os.makedirs(save_dir)
                self.update_status(f"创建保存目录: {save_dir}")
            except:
                QMessageBox.warning(self, "警告", f"无法创建保存目录: {save_dir}")
                return
                
        # 禁用下载按钮，启用取消按钮
        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        
        # 重置进度条
        self.total_progress.setValue(0)
        self.video_progress.setValue(0)
        
        # 清空状态
        self.status_text.clear()
        self.update_status("开始下载...")
        
        # 创建并启动下载线程
        self.download_thread = DownloadThread(url, cookie, save_dir)
        self.download_thread.update_status.connect(self.update_status)
        self.download_thread.update_progress.connect(self.update_video_progress)
        self.download_thread.update_total_progress.connect(self.update_total_progress)
        self.download_thread.download_complete.connect(self.download_finished)
        self.download_thread.start()
        
    def update_total_progress(self, value):
        self.total_progress.setValue(value)
        
    def update_video_progress(self, value):
        self.video_progress.setValue(value)
        
    def cancel_download(self):
        if self.download_thread and self.download_thread.isRunning():
            self.update_status("正在取消下载...")
            self.download_thread.terminate()
            self.download_thread.wait()
            self.update_status("下载已取消")
            
        self.download_finished("cancelled")
        
    def download_finished(self, status):
        # 恢复按钮状态
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        
        # 显示结果消息
        if status == "success":
            QMessageBox.information(self, "成功", "下载完成!")
        elif status == "failed":
            QMessageBox.critical(self, "失败", "下载过程中发生错误!")
        elif status == "cancelled":
            QMessageBox.information(self, "已取消", "下载已取消!")

def main():
    app = QApplication(sys.argv)
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    window = WeiboDownloader()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()    