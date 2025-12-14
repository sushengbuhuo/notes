import sys
import os
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
 
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit,
    QMessageBox, QFileDialog, QFrame, QProgressBar
)
from PyQt6.QtCore import (
    QObject, QSettings, QThread, pyqtSignal, Qt, pyqtSlot
)
from PyQt6.QtGui import QAction, QColor, QPalette, QPixmap, QMouseEvent
from bs4 import BeautifulSoup
 
 
class ImageCache:
    """图片缓存管理器"""
    _instance = None
     
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
        return cls._instance
     
    def get_key(self, url):
        """生成缓存键"""
        return hashlib.md5(url.encode()).hexdigest()
     
    def get(self, url):
        """获取缓存图片"""
        key = self.get_key(url)
        return self.cache.get(key)
     
    def put(self, url, data):
        """存储图片到缓存"""
        key = self.get_key(url)
        self.cache[key] = data
         
    def clear(self):
        """清空缓存"""
        self.cache.clear()
 
class DownloadWorker(QObject):
    """图片下载工作线程"""
    progress = pyqtSignal(int, int)  # current, total
    image_downloaded = pyqtSignal(int, bytes, str)  # index, data, url
    finished = pyqtSignal(list)  # 所有图片下载完成
    error = pyqtSignal(str, str)  # url, error message
     
    def __init__(self, image_urls):
        super().__init__()
        self.image_urls = image_urls
        self.should_stop = False
        self.cache = ImageCache()
         
    def run(self):
        """执行下载任务"""
        try:
            total = len(self.image_urls)
            downloaded = 0
             
            # 使用线程池并发下载
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for i, url in enumerate(self.image_urls):
                    if self.should_stop:
                        break
                     
                    # 检查缓存
                    cached_data = self.cache.get(url)
                    if cached_data:
                        self.image_downloaded.emit(i, cached_data, url)
                        downloaded += 1
                        self.progress.emit(downloaded, total)
                        continue
                     
                    # 提交下载任务
                    future = executor.submit(self.download_single_image, i, url)
                    futures.append(future)
                 
                # 处理下载结果
                for future in as_completed(futures):
                    if self.should_stop:
                        break
                     
                    try:
                        result = future.result()
                        if result:
                            i, data, url = result
                            self.cache.put(url, data)
                            downloaded += 1
                            self.progress.emit(downloaded, total)
                    except Exception as e:
                        # 错误已由下载函数处理并发射信号
                        pass
             
            if not self.should_stop:
                self.finished.emit(self.image_urls)
                 
        except Exception as e:
            self.error.emit("下载失败", str(e))
     
    def download_single_image(self, index, url):
        """下载单张图片"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.xiaohongshu.com/'
            }
             
            # 使用urllib3或requests下载
            response = requests.get(url, headers=headers, timeout=10, stream=True)
            response.raise_for_status()
             
            # 读取图片数据
            data = response.content
             
            if data and len(data) > 0:
                # 验证是否为有效图片
                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    self.image_downloaded.emit(index, data, url)
                    return (index, data, url)
                else:
                    self.error.emit(url, "无效的图片数据")
            else:
                self.error.emit(url, "空图片数据")
                 
        except Exception as e:
            self.error.emit(url, str(e))
         
        return None
     
    def stop(self):
        """停止下载"""
        self.should_stop = True
 
class ThumbnailWidget(QLabel):
    """缩略图控件"""
     
    def __init__(self, index, parent=None, meta_parent=None):
        super().__init__(parent)
        self.parent_widget = meta_parent
        self.index = index
        self.is_selected = False
        self.setFixedSize(50, 70)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            ThumbnailWidget {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                padding: 2px;
            }
            ThumbnailWidget:hover {
                border-color: #3498db;
                background-color: #e3f2fd;
            }
        """)
         
    def set_selected(self, selected):
        """设置选中状态"""
        self.is_selected = selected
        if selected:
            self.setStyleSheet("""
                ThumbnailWidget {
                    background-color: #3498db;
                    border: 2px solid #2980b9;
                    border-radius: 5px;
                    padding: 2px;
                }
                ThumbnailWidget:hover {
                    border-color: #21618c;
                    background-color: #2980b9;
                }
            """)
        else:
            self.setStyleSheet("""
                ThumbnailWidget {
                    background-color: #f8f9fa;
                    border: 2px solid #dee2e6;
                    border-radius: 5px;
                    padding: 2px;
                }
                ThumbnailWidget:hover {
                    border-color: #3498db;
                    background-color: #e3f2fd;
                }
            """)
     
    def mousePressEvent(self, event: QMouseEvent):
        """点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_widget.thumbnail_clicked(self.index)
        super().mousePressEvent(event)
 
class ImageCarousel(QWidget):
    """图片轮播组件 - 带缩略图导航和异步下载"""
     
    # 自定义信号
    download_started = pyqtSignal()
    download_finished = pyqtSignal(list)
    download_error = pyqtSignal(str)
 
    def __init__(self):
        super().__init__()
        self.images = []
        self.thumbnails = []
        self.image_data = []  # 存储图片原始数据
        self.current_index = 0
        self.thumbnail_start = 0
        self.download_worker = None
        self.download_thread = None
        self.downloading = False
         
        self.setFixedSize(500, 730)  # 增加高度以容纳进度条
        self.setup_ui()
 
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
 
        # 图片显示区域
        self.image_label = QLabel()
        self.image_label.setFixedSize(480, 570)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.image_label)
 
        # 页码显示
        self.page_label = QLabel("0/0")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px 12px;
            }
        """)
        layout.addWidget(self.page_label)
 
        # 下载进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 5px;
                text-align: center;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
 
        # 缩略图导航区域
        self.setup_thumbnail_nav()
         
        layout.addStretch()
 
    def setup_thumbnail_nav(self):
        """设置缩略图导航"""
        nav_frame = QFrame()
        nav_frame.setFixedHeight(100)
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 5px;
            }
        """)
         
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(5)
         
        # 左侧滚动按钮
        self.scroll_left_btn = QPushButton("\u25C0")
        self.scroll_left_btn.setFixedSize(30, 70)
        self.scroll_left_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                color: #495057;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
            QPushButton:disabled {
                background-color: #f8f9fa;
                color: #adb5bd;
                border-color: #e9ecef;
            }
        """)
        self.scroll_left_btn.clicked.connect(self.scroll_thumbnails_left)
        self.scroll_left_btn.setEnabled(False)
        nav_layout.addWidget(self.scroll_left_btn)
         
        # 缩略图容器
        self.thumbnail_container = QWidget()
        self.thumbnail_layout = QHBoxLayout(self.thumbnail_container)
        self.thumbnail_layout.setContentsMargins(0, 0, 0, 0)
        self.thumbnail_layout.setSpacing(5)
         
        # 创建6个缩略图占位符
        self.thumbnail_widgets = []
        for i in range(6):
            thumbnail = ThumbnailWidget(i, self.thumbnail_container, self)
            self.thumbnail_widgets.append(thumbnail)
            self.thumbnail_layout.addWidget(thumbnail)
         
        nav_layout.addWidget(self.thumbnail_container, 1)
         
        # 右侧滚动按钮
        self.scroll_right_btn = QPushButton("\u25B6")
        self.scroll_right_btn.setFixedSize(30, 70)
        self.scroll_right_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                color: #495057;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
            QPushButton:disabled {
                background-color: #f8f9fa;
                color: #adb5bd;
                border-color: #e9ecef;
            }
        """)
        self.scroll_right_btn.clicked.connect(self.scroll_thumbnails_right)
        self.scroll_right_btn.setEnabled(False)
        nav_layout.addWidget(self.scroll_right_btn)
         
        self.layout().addWidget(nav_frame)
 
    def set_images(self, image_urls):
        """设置图片列表（异步下载）"""
        # 停止当前的下载任务
        self.stop_download()
         
        # 重置状态
        self.images = []
        self.thumbnails = []
        self.image_data = []
        self.current_index = 0
        self.thumbnail_start = 0
         
        # 初始化列表
        for _ in image_urls:
            self.images.append(None)
            self.thumbnails.append(None)
            self.image_data.append(None)
         
        # 更新显示占位符
        self.update_display()
        self.update_thumbnails()
         
        if image_urls:
            self.download_started.emit()
            self.start_image_download(image_urls)
        else:
            self.update_display()
 
    def start_image_download(self, image_urls):
        """启动图片下载线程"""
        self.downloading = True
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(image_urls))
         
        # 创建下载线程
        self.download_thread = QThread()
        self.download_worker = DownloadWorker(image_urls)
        self.download_worker.moveToThread(self.download_thread)
         
        # 连接信号
        self.download_worker.progress.connect(self.on_download_progress)
        self.download_worker.image_downloaded.connect(self.on_image_downloaded)
        self.download_worker.finished.connect(self.on_download_finished)
        self.download_worker.error.connect(self.on_download_error)
         
        # 启动线程
        self.download_thread.started.connect(self.download_worker.run)
        self.download_thread.start()
 
    @pyqtSlot(int, bytes, str)
    def on_image_downloaded(self, index, data, url):
        """单张图片下载完成"""
        if index < len(self.image_data):
            # 保存原始数据
            self.image_data[index] = data
             
            # 创建QPixmap
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                # 主显示图片
                scaled_pixmap = pixmap.scaled(
                    580, 500,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.images[index] = scaled_pixmap
                 
                # 缩略图
                thumbnail_pixmap = pixmap.scaled(
                    46, 66,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.thumbnails[index] = thumbnail_pixmap
                 
                # 如果这是第一张图片或当前索引的图片，更新显示
                if index == 0 or index == self.current_index:
                    self.update_display()
                 
                # 更新缩略图
                if self.thumbnail_start <= index < self.thumbnail_start + 6:
                    self.update_thumbnails()
 
    @pyqtSlot(int, int)
    def on_download_progress(self, current, total):
        """下载进度更新"""
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"下载中: {current}/{total}")
 
    @pyqtSlot(list)
    def on_download_finished(self, image_urls):
        """所有图片下载完成"""
        self.downloading = False
        self.progress_bar.hide()
         
        # 清理线程
        if self.download_thread:
            self.download_thread.quit()
            self.download_thread.wait()
            self.download_thread = None
            self.download_worker = None
         
        self.download_finished.emit(image_urls)
         
        # 确保显示当前图片
        self.update_display()
        self.update_thumbnails()
 
    @pyqtSlot(str, str)
    def on_download_error(self, url, error_msg):
        """下载错误"""
        self.download_error.emit(f"下载失败 ({url}): {error_msg}")
 
    def stop_download(self):
        """停止下载"""
        if self.download_worker:
            self.download_worker.stop()
         
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.quit()
            self.download_thread.wait()
         
        self.downloading = False
        self.progress_bar.hide()
 
    def update_display(self):
        """更新当前显示的图片"""
        if self.images and self.images[self.current_index] is not None:
            self.image_label.setPixmap(self.images[self.current_index])
            self.page_label.setText(f"{self.current_index + 1}/{len(self.images)}")
        else:
            if self.downloading and self.current_index < len(self.images):
                self.image_label.setText(f"下载中... ({self.current_index + 1}/{len(self.images)})")
            else:
                self.image_label.setText("暂无图片")
             
            self.image_label.setStyleSheet("""
                QLabel {
                    background-color: #f8f9fa;
                    border: 2px solid #dee2e6;
                    border-radius: 15px;
                    padding: 10px;
                    color: #6c757d;
                    font-size: 16px;
                }
            """)
             
            if len(self.images) > 0:
                self.page_label.setText(f"{self.current_index + 1}/{len(self.images)}")
            else:
                self.page_label.setText("0/0")
 
    def update_thumbnails(self):
        """更新缩略图显示"""
        total = len(self.thumbnails)
         
        # 更新滚动按钮状态
        self.scroll_left_btn.setEnabled(self.thumbnail_start > 0)
        self.scroll_right_btn.setEnabled(self.thumbnail_start + 6 < total)
         
        # 更新每个缩略图
        for i in range(6):
            widget = self.thumbnail_widgets[i]
            thumbnail_index = self.thumbnail_start + i
             
            if thumbnail_index < total:
                pixmap = self.thumbnails[thumbnail_index]
                if pixmap is not None:
                    widget.setPixmap(pixmap)
                else:
                    widget.setText(f"{thumbnail_index + 1}")
                    widget.setStyleSheet("""
                        ThumbnailWidget {
                            background-color: #e9ecef;
                            border: 2px solid #ced4da;
                            border-radius: 5px;
                            padding: 2px;
                            color: #6c757d;
                            font-size: 10px;
                        }
                    """)
                 
                widget.set_selected(thumbnail_index == self.current_index)
                widget.setVisible(True)
            else:
                widget.setVisible(False)
                widget.set_selected(False)
 
    def scroll_thumbnails_left(self):
        """向左滚动缩略图"""
        if self.thumbnail_start > 0:
            self.thumbnail_start = max(0, self.thumbnail_start - 6)
            self.update_thumbnails()
 
    def scroll_thumbnails_right(self):
        """向右滚动缩略图"""
        total = len(self.thumbnails)
        if self.thumbnail_start + 6 < total:
            self.thumbnail_start = min(self.thumbnail_start + 6, total - 6)
            self.update_thumbnails()
 
    def thumbnail_clicked(self, widget_index):
        """缩略图被点击"""
        actual_index = self.thumbnail_start + widget_index
        if actual_index < len(self.images):
            self.current_index = actual_index
            self.update_display()
            self.update_thumbnails()
 
    def show_prev(self):
        """显示上一张图片"""
        if self.current_index > 0:
            self.current_index -= 1
             
            if self.current_index < self.thumbnail_start:
                self.thumbnail_start = max(0, self.current_index)
             
            self.update_display()
            self.update_thumbnails()
 
    def show_next(self):
        """显示下一张图片"""
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
             
            if self.current_index >= self.thumbnail_start + 6:
                self.thumbnail_start = min(self.current_index - 5, len(self.thumbnails) - 6)
             
            self.update_display()
            self.update_thumbnails()
     
    def get_image_data(self, index):
        """获取指定索引的图片原始数据"""
        if 0 <= index < len(self.image_data):
            return self.image_data[index]
        return None
 
class Worker(QObject):
    """工作线程"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
 
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.is_paused = False
        self.should_stop = False
 
    def get_xiaohongshu_content(self, url):
        """获取小红书内容"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
 
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
 
            # 提取标题
            title_tag = soup.find('meta',{'name': 'og:title'}) or soup.find('meta', {'property': 'og:title'})
            title = title_tag.get('content') if title_tag else ''
            if title and ' - 小红书' in title:
                title = title.replace(' - 小红书', '')
 
            # 提取内容
            content_tag = soup.find('meta', {'name': 'description'}) or soup.find('meta',{'property': 'og:description'})
            content = content_tag.get('content') if content_tag else ''
 
            # 提取标签
            keywords_tag = soup.find('meta', {'name': 'keywords'})
            tags = []
            if keywords_tag and keywords_tag.get('content'):
                tags = [tag.strip() for tag in keywords_tag['content'].split(',')]
 
            # 提取图片链接
            image_links = []
            image_tags = soup.find_all('meta', {'property': 'og:image'})
            if not image_tags:
                image_tags = soup.find_all('meta', {'name': 'og:image'})
 
            for img_tag in image_tags:
                if img_tag.get('content'):
                    image_links.append(img_tag['content'])
             
            # url
            url_tag = soup.find('meta', {'name': 'og:url'}) or soup.find('meta',{'property': 'og:url'} )
            url_original = url_tag.get('content') if url_tag else ''
            # comment
            note_comment_tag = soup.find('meta',  {'name': 'og:xhs:note_comment'}) or soup.find('meta',{'property': 'og:xhs:note_comment'})
            note_comment_count = note_comment_tag.get('content') if note_comment_tag else ''
            # note_like
            note_like_tag = soup.find('meta',  {'name': 'og:xhs:note_like'}) or soup.find('meta',{'property': 'og:xhs:note_like'})
            note_like_count = note_like_tag.get('content') if note_like_tag else ''
            # collect
            note_collect_tag = soup.find('meta',  {'name': 'og:xhs:note_collect'}) or soup.find('meta',{'property': 'og:xhs:note_collect'})
            note_collect_count = note_collect_tag.get('content') if note_collect_tag else ''
 
            #原帖信息，url-点赞-收藏-评论
            original_post_info =(url_original,note_like_count,note_collect_count,note_comment_count)
 
            return {
                '标题': title,
                '内容': content,
                '标签': tags,
                '图片链接': image_links,
                '图片数量': len(image_links),
                '状态': '成功',
                'original_post_info':original_post_info
            }
 
        except Exception as e:
            return {
                '标题': '',
                '内容': '',
                '标签': [],
                '图片链接': [],
                '图片数量': 0,
                '状态': f'错误: {str(e)}',
                'original_post_info':()
            }
 
    def run(self):
        """运行解析任务"""
        if self.should_stop:
            return
 
        result = self.get_xiaohongshu_content(self.url)
        self.finished.emit(result)
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("无水印下载图文笔记工具 - 仅供学习交流")
        self.setGeometry(100, 100, 1200, 800)
 
        # 初始化 QSettings
        self.settings = QSettings("MyCompany", "My App")
 
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QWidget {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
            }
        """)
 
        # 设置上下文菜单策略
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
 
        self.setup_ui()
        self.workers = []
        self.current_result = None
 
    def show_context_menu(self, position):
        """显示右键上下文菜单"""
        menu = QMenu(self)
         
        # 1. 当前设置信息（不可点击）
        current_folder = self.settings.value("default_xhs_download_folder", "")
        if current_folder:
            display_text = f"当前文件夹: ./{os.path.basename(current_folder)}"
            if len(display_text) > 40:
                display_text = display_text[:37] + "..."
        else:
            display_text = "当前文件夹: 未设置"
         
        info_action = QAction(display_text, self)
        info_action.setEnabled(False)
        menu.addAction(info_action)
         
        # 添加分隔符
        menu.addSeparator()
         
        # 2. 设置默认下载文件夹按钮
        set_action = QAction("&#128193; 设置默认下载文件夹", self)
        set_action.triggered.connect(self.set_default_download_folder)
        menu.addAction(set_action)
         
        # 3. 清除默认文件夹按钮
        clear_action = QAction("&#128465;&#65039; 清除默认文件夹", self)
        clear_action.triggered.connect(self.clear_default_download_folder)
        menu.addAction(clear_action)
         
        # 显示菜单
        menu.exec(self.mapToGlobal(position))
 
    def set_default_download_folder(self):
        """设置默认下载文件夹"""
        # 使用当前设置的值作为初始目录（如果存在）
        current_folder = self.settings.value("default_xhs_download_folder", "")
         
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择默认下载文件夹",
            current_folder if current_folder else "",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
         
        if directory:
            self.settings.setValue("default_xhs_download_folder", directory)
            QMessageBox.information(
                self,
                "设置成功",
                f"已设置默认下载文件夹为:\n{directory}"
            )
 
    def clear_default_download_folder(self):
        """清除默认下载文件夹设置"""
        reply = QMessageBox.question(
            self,
            "确认清除",
            "确定要清除默认下载文件夹设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
         
        if reply == QMessageBox.StandardButton.Yes:
            self.settings.remove("default_xhs_download_folder")
            QMessageBox.information(self, "清除成功", "已清除默认下载文件夹设置")
 
    def get_default_download_folder(self):
        """获取默认下载文件夹路径"""
        return self.settings.value("default_xhs_download_folder", "")
 
    def setup_ui(self):
        """设置UI界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
 
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
 
        # 顶部控制区域
        top_card = self.create_top_card()
        main_layout.addWidget(top_card)
 
        # 内容显示区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(15)
 
        # 左侧图片展示区
        self.image_carousel = ImageCarousel()
        self.image_carousel.download_started.connect(self.on_download_started)
        self.image_carousel.download_finished.connect(self.on_download_finished)
        self.image_carousel.download_error.connect(self.on_download_error)
        content_layout.addWidget(self.image_carousel)
 
        # 右侧内容区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(12)
 
        # 标题显示区域
        title_card = self.create_title_card()
        right_layout.addWidget(title_card)
 
        # 内容显示区域
        content_card = self.create_content_card()
        right_layout.addWidget(content_card, 1)
 
        # 标签显示区域
        tags_card = self.create_tags_card()
        right_layout.addWidget(tags_card)
 
        content_layout.addWidget(right_widget, 1)
        main_layout.addWidget(content_widget, 1)
 
    def create_top_card(self):
        """创建顶部控制卡片"""
        card = QWidget()
        card.setFixedHeight(70)
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                padding: 12px;
            }
        """)
 
        layout = QHBoxLayout(card)
        layout.setSpacing(15)
 
        # 笔记链接输入框
        url_label = QLabel("笔记链接:")
        url_label.setStyleSheet("font-weight: bold; color: #495057; font-size: 13px;")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入小红书笔记链接...")
        self.url_input.setClearButtonEnabled(True)
        self.url_input.setMinimumHeight(35)
        self.url_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
 
        # 开始解析按钮
        self.parse_btn = QPushButton("开始解析")
        self.parse_btn.setMinimumHeight(35)
        self.parse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                padding: 6px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.parse_btn.clicked.connect(self.start_parsing)
         
        # 暂停解析按钮 
        self.pause_btn = QPushButton("暂停解析")
        self.pause_btn.setMinimumHeight(35)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                padding: 6px 15px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
 
        # 导出数据按钮
        self.export_btn = QPushButton("下载数据")
        self.export_btn.setMinimumHeight(35)
        self.export_btn.setEnabled(False)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                padding: 6px 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.export_btn.clicked.connect(self.export_data)
 
        layout.addWidget(url_label)
        layout.addWidget(self.url_input, 1)
        layout.addWidget(self.parse_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.export_btn)
 
        return card
 
    def create_title_card(self):
        """创建标题显示卡片"""
        card = QWidget()
        card.setFixedHeight(90)
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                padding: 4px;
            }
        """)
 
        layout = QVBoxLayout(card)
        layout.setSpacing(1)
 
        title_label = QLabel("标题")
        title_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        """)
 
        self.title_display = QLabel("等待解析...")
        self.title_display.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #343a40;
                padding: 3px;
            }
        """)
        self.title_display.setWordWrap(True)
 
        layout.addWidget(title_label)
        layout.addWidget(self.title_display)
 
        return card
 
    def create_content_card(self):
        """创建内容显示卡片"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                padding: 4px;
            }
        """)
 
        layout = QVBoxLayout(card)
        layout.setSpacing(1)
 
        content_label = QLabel("内容")
        content_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        """)
 
        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        self.content_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 12px;
                font-size: 13px;
                line-height: 1.6;
                color: #343a40;
                min-height: 160px;
            }
            QScrollBar:vertical {
                background-color: #f1f3f5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #adb5bd;
                border-radius: 5px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #6c757d;
            }
        """)
        palette = self.content_display.palette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor(200, 220, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(20, 20, 20))
        self.content_display.setPalette(palette)
 
        layout.addWidget(content_label)
        layout.addWidget(self.content_display)
 
        return card
 
    def create_tags_card(self):
        """创建标签显示卡片"""
        card = QWidget()
        card.setFixedHeight(130)
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                padding: 4px;
            }
        """)
 
        layout = QVBoxLayout(card)
        layout.setSpacing(1)
 
        tags_label = QLabel("标签")
        tags_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        """)
 
        self.tags_display = QTextEdit()
        self.tags_display.setReadOnly(True)
        self.tags_display.setMaximumHeight(80)
        self.tags_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 2px;
                font-size: 13px;
                color: #495057;
            }
        """)
 
        palette = self.tags_display.palette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor(200, 220, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(20, 20, 20))
        self.tags_display.setPalette(palette)
 
        layout.addWidget(tags_label)
        layout.addWidget(self.tags_display)
 
        return card
 
    def start_parsing(self):
        """开始解析"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "警告", "请输入小红书笔记链接！")
            return
 
        # 禁用按钮
        self.parse_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.export_btn.setEnabled(False)
 
        # 清除之前的结果
        self.title_display.setText("解析中...")
        self.content_display.clear()
        self.tags_display.clear()
        self.image_carousel.set_images([])
 
        # 创建工作线程
        self.worker = Worker(url)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
 
        # 连接信号
        self.worker.finished.connect(self.on_parsing_finished)
        self.worker.error.connect(self.on_parsing_error)
        self.worker_thread.started.connect(self.worker.run)
 
        # 启动线程
        self.worker_thread.start()
 
    def on_parsing_finished(self, result):
        """解析完成处理"""
        # 更新UI
        self.title_display.setText(result['标题'] or "未获取到标题")
        self.content_display.setText(result['内容'] or "未获取到内容")
 
        # 更新标签
        if result['标签']:
            tags_text = ", ".join(result['标签'])
            self.tags_display.setText(tags_text)
        else:
            self.tags_display.setText("未获取到标签")
 
        # 更新图片
        if result['图片链接']:
            self.image_carousel.set_images(result['图片链接'])
        else:
            self.image_carousel.set_images([])
 
        # 保存结果
        self.current_result = result
 
        # 更新按钮状态
        self.parse_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.export_btn.setEnabled(len(result['图片链接']) > 0)
 
        # 停止线程
        self.worker_thread.quit()
        self.worker_thread.wait()
 
        # 显示状态
        if result['状态'] == '成功':
            pass
            # QMessageBox.information(self, "成功", f"解析完成！找到 {result['图片数量']} 张图片")
        else:
            QMessageBox.warning(self, "警告", result['状态'])
 
    def on_parsing_error(self, error_msg):
        """解析错误处理"""
        self.title_display.setText("解析失败")
        self.content_display.setText(f"错误信息: {error_msg}")
 
        # 更新按钮状态
        self.parse_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
 
        # 停止线程
        self.worker_thread.quit()
        self.worker_thread.wait()
 
        QMessageBox.critical(self, "错误", f"解析失败: {error_msg}")
 
    def on_download_started(self):
        """图片下载开始"""
        self.export_btn.setEnabled(False)
 
    def on_download_finished(self, image_urls):
        """图片下载完成"""
        self.export_btn.setEnabled(len(image_urls) > 0)
        # QMessageBox.information(self, "完成", f"图片下载完成！共 {len(image_urls)} 张图片")
 
    def on_download_error(self, error_msg):
        """图片下载错误"""
        QMessageBox.warning(self, "下载错误", error_msg)
 
    def export_data(self):
        """导出数据到文件夹（包含图片和文本）"""
        if not hasattr(self, 'current_result'):
            QMessageBox.warning(self, "警告", "没有可导出的数据！")
            return
         
        # 获取默认下载文件夹
        default_folder = self.get_default_download_folder()
        directory = default_folder
        if not default_folder:
            # 让用户选择保存目录
            directory = QFileDialog.getExistingDirectory(
                self,
                "选择保存目录",
                "",
                QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
            )
 
            if not directory:
                return
 
        try:
            # 创建以时间戳命名的子文件夹
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_dir = os.path.join(directory, f"小红书笔记_{timestamp}")
            os.makedirs(save_dir, exist_ok=True)
 
            # 创建文本文件
            text_filename = os.path.join(save_dir, "内容.txt")
            with open(text_filename, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("小红书笔记内容\n")
                f.write("=" * 50 + "\n\n")
 
                # 写入标题
                f.write("【标题】\n")
                f.write(f"{self.current_result['标题'] or '无标题'}\n\n")
 
                # 写入内容
                f.write("【内容】\n")
                f.write(f"{self.current_result['内容'] or '无内容'}\n\n")
 
                # 写入标签
                f.write("【标签】\n")
                if self.current_result['标签']:
                    tags_text = ", ".join(self.current_result['标签'])
                    f.write(f"{tags_text}\n\n")
                else:
                    f.write("无标签\n\n")
 
                # 写入统计信息
                f.write("=" * 50 + "\n")
                f.write("统计信息\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"图片数量: {self.current_result['图片数量']}\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"导出状态: {self.current_result['状态']}\n")
 
                # 原帖信息
                if self.current_result['original_post_info']:
                    f.write("\n\n")
                    f.write("=" * 50 + "\n")
                    f.write("原帖信息\n")
                    f.write("=" * 50 + "\n\n")
 
                    url,note_like_count,note_collect_count,note_comment_count = self.current_result['original_post_info'] 
                    f.write(f"{url}\n\n")
                    # 点赞收藏数量 不给（仅显示10+）
                    # f.write(f"点赞: {note_like_count}\n")
                    # f.write(f"收藏: {note_collect_count}\n")
                    # f.write(f"评论: {note_comment_count}\n")
 
 
            # 下载图片 - 从内存中直接保存，无需重新下载
            image_count = 0
            total_images = min(self.current_result['图片数量'], len(self.image_carousel.image_data))
             
            for i in range(total_images):
                try:
                    # 从内存缓存中获取图片数据
                    image_data = self.image_carousel.get_image_data(i)
                     
                    if image_data:
                        # 尝试从URL获取扩展名
                        img_url = self.current_result['图片链接'][i] if i < len(self.current_result['图片链接']) else ""
                        ext = ".jpg"  # 默认扩展名
                         
                        if img_url:
                            url_ext = os.path.splitext(img_url)[1]
                            if url_ext and len(url_ext) <= 5:  # 合理的扩展名长度
                                ext = url_ext.split('?')[0]  # 去除查询参数
                         
                        # 保存图片
                        img_filename = os.path.join(save_dir, f"图片_{i+1:02d}{ext}")
                        with open(img_filename, 'wb') as img_file:
                            img_file.write(image_data)
                        image_count += 1
                    else:
                        print(f"图片 {i+1} 数据不存在")
 
                    # 更新进度
                    QApplication.processEvents()
 
                except Exception as e:
                    print(f"保存图片失败 {i+1}: {str(e)}")
                    continue
 
            # 显示导出结果
            success_msg = f"数据导出成功！\n\n"
            success_msg += f"保存位置: {save_dir}\n"
            success_msg += f"文本文件: 内容.txt\n"
            success_msg += f"图片文件: {image_count}/{total_images} 张\n"
 
            if image_count < total_images:
                success_msg += f"\n注意: 部分图片保存失败"
 
            QMessageBox.information(self, "导出成功", success_msg)
 
            # 打开保存的文件夹
            if sys.platform == "win32":
                os.startfile(save_dir)
            elif sys.platform == "darwin":
                import subprocess
                subprocess.run(["open", save_dir])
            else:
                import subprocess
                subprocess.run(["xdg-open", save_dir])
 
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出过程中发生错误:\n{str(e)}")
 
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止所有下载线程
        self.image_carousel.stop_download()
        event.accept()
 
def main():
    app = QApplication(sys.argv)
 
    # 设置应用程序样式
    app.setStyle('Fusion')
 
    window = MainWindow()
    window.show()
 
    sys.exit(app.exec())
 
if __name__ == "__main__":
    main()