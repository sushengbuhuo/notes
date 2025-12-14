import sys
import csv
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import urllib.request
from io import BytesIO
from threading import Thread
from queue import Queue
import time
import os
from datetime import datetime
 
 
class ImageCarousel(QWidget):
    """图片轮播组件"""
 
    def __init__(self):
        super().__init__()
        self.images = []
        self.current_index = 0
        self.setFixedSize(500, 670)  # 减少高度
        self.setup_ui()
 
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
 
        # 图片显示区域
        self.image_label = QLabel()
        self.image_label.setFixedSize(480, 570)  # 减少图片显示区域高度
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.image_label)
 
        # 导航控制区域
        nav_widget = QWidget()
        nav_layout = QHBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
 
        # 上一张按钮
        self.prev_btn = QPushButton("&#9664; 上一张")
        self.prev_btn.setFixedHeight(45)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 15px;
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
        self.prev_btn.clicked.connect(self.show_prev)
        self.prev_btn.setEnabled(False)
 
        # 页码显示
        self.page_label = QLabel("0/0")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                padding: 5px 12px;
            }
        """)
 
        # 下一张按钮
        self.next_btn = QPushButton("下一张 &#9654;")
        self.next_btn.setFixedHeight(45)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                padding: 8px 15px;
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
        self.next_btn.clicked.connect(self.show_next)
        self.next_btn.setEnabled(False)
 
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.page_label)
        nav_layout.addWidget(self.next_btn)
 
        layout.addWidget(nav_widget)
 
    def set_images(self, image_urls):
        """设置图片列表"""
        self.images = []
        self.current_index = 0
 
        # 下载图片
        for url in image_urls:
            try:
                data = urllib.request.urlopen(url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
 
                # 缩放图片以适应显示区域
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        580, 500,  # 减少缩放尺寸
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    self.images.append(scaled_pixmap)
            except:
                continue
 
        # 更新显示
        self.update_display()
 
        # 更新导航按钮状态
        self.update_navigation()
 
    def update_display(self):
        """更新当前显示的图片"""
        if self.images:
            self.image_label.setPixmap(self.images[self.current_index])
            self.update_navigation()
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
 
    def update_navigation(self):
        """更新导航按钮状态"""
        total = len(self.images)
        if total > 0:
            self.page_label.setText(f"{self.current_index + 1}/{total}")
            self.prev_btn.setEnabled(self.current_index > 0)
            self.next_btn.setEnabled(self.current_index < total - 1)
        else:
            self.page_label.setText("0/0")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
 
    def show_prev(self):
        """显示上一张图片"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()
 
    def show_next(self):
        """显示下一张图片"""
        if self.current_index < len(self.images) - 1:
            self.current_index += 1
            self.update_display()
 
 
class ContentDisplay(QTextEdit):
    """内容显示组件，带滚动条"""
 
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
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
            title_tag = soup.find('meta', {'property': 'og:title'}) or soup.find('meta', {'name': 'og:title'})
            title = title_tag.get('content') if title_tag else ''
            if title and ' - 小红书' in title:
                title = title.replace(' - 小红书', '')
 
            # 提取内容
            content_tag = soup.find('meta', {'property': 'og:description'}) or soup.find('meta',
                                                                                         {'name': 'description'})
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
 
            return {
                '标题': title,
                '内容': content,
                '标签': tags,
                '图片链接': image_links,
                '图片数量': len(image_links),
                '状态': '成功'
            }
 
        except Exception as e:
            return {
                '标题': '',
                '内容': '',
                '标签': [],
                '图片链接': [],
                '图片数量': 0,
                '状态': f'错误: {str(e)}'
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
        self.setWindowTitle("无水印下载图文笔记工具 - 仅供学习交流 ")
        self.setGeometry(100, 100, 1200, 800)  # 减少窗口高度
 
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QWidget {
                font-family: 'Microsoft YaHei', Arial, sans-serif;
            }
        """)
 
        self.setup_ui()
        self.workers = []
 
    def setup_ui(self):
        """设置UI界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
 
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)  # 减少边距
        main_layout.setSpacing(15)  # 减少间距
 
        # 顶部控制区域
        top_card = self.create_top_card()
        main_layout.addWidget(top_card)
 
        # 内容显示区域
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(15)  # 减少间距
 
        # 左侧图片展示区
        self.image_carousel = ImageCarousel()
        content_layout.addWidget(self.image_carousel)
 
        # 右侧内容区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(12)  # 减少间距
 
        # 标题显示区域
        title_card = self.create_title_card()
        right_layout.addWidget(title_card)
 
        # 内容显示区域
        content_card = self.create_content_card()
        right_layout.addWidget(content_card, 1)  # 设置为可伸缩
 
        # 标签显示区域
        tags_card = self.create_tags_card()
        right_layout.addWidget(tags_card)
 
        content_layout.addWidget(right_widget, 1)  # 右侧区域可伸缩
        main_layout.addWidget(content_widget, 1)  # 内容区域可伸缩
 
    def create_top_card(self):
        """创建顶部控制卡片"""
        card = QWidget()
        card.setFixedHeight(70)  # 减少高度
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
        self.url_input.setMinimumHeight(35)  # 减少高度
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
 
        # 添加到布局
        layout.addWidget(url_label)
        layout.addWidget(self.url_input, 1)  # 输入框可伸缩
        layout.addWidget(self.parse_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.export_btn)
 
        return card
 
    def create_title_card(self):
        """创建标题显示卡片"""
        card = QWidget()
        card.setFixedHeight(90)  # 减少高度
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
 
        self.content_display = ContentDisplay()
 
        layout.addWidget(content_label)
        layout.addWidget(self.content_display)
 
        return card
 
    def create_tags_card(self):
        """创建标签显示卡片"""
        card = QWidget()
        card.setFixedHeight(130)  # 减少高度
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
        self.tags_display.setMaximumHeight(80)  # 减少高度
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
        self.export_btn.setEnabled(True)
 
        # 停止线程
        self.worker_thread.quit()
        self.worker_thread.wait()
 
        # 显示状态
        if result['状态'] == '成功':
            QMessageBox.information(self, "成功", "解析完成！")
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
 
    def export_data(self):
        """导出数据到文件夹（包含图片和文本）"""
        if not hasattr(self, 'current_result'):
            QMessageBox.warning(self, "警告", "没有可导出的数据！")
            return
 
        # 让用户选择保存目录
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择保存目录",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
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
 
            # 下载图片
            image_count = 0
            for i, img_url in enumerate(self.current_result['图片链接'], 1):
                try:
                    # 获取图片扩展名
                    ext = os.path.splitext(img_url)[1]
                    if not ext or len(ext) > 5:  # 如果没有扩展名或太长，使用jpg
                        ext = ".jpg"
 
                    # 下载图片
                    img_filename = os.path.join(save_dir, f"图片_{i:02d}{ext}")
                    urllib.request.urlretrieve(img_url, img_filename)
                    image_count += 1
 
                    # 更新进度
                    QApplication.processEvents()  # 确保UI更新
 
                except Exception as e:
                    print(f"下载图片失败 {img_url}: {str(e)}")
                    continue
 
            # 显示导出结果
            success_msg = f"数据导出成功！\n\n"
            success_msg += f"保存位置: {save_dir}\n"
            success_msg += f"文本文件: 内容.txt\n"
            success_msg += f"图片文件: {image_count}/{self.current_result['图片数量']} 张\n"
 
            if image_count < self.current_result['图片数量']:
                success_msg += f"\n注意: 部分图片下载失败"
 
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
 
 
def main():
    app = QApplication(sys.argv)
 
    # 设置应用程序样式
    app.setStyle('Fusion')
 
    window = MainWindow()
    window.show()
 
    sys.exit(app.exec_())
 
 
if __name__ == "__main__":
    main()