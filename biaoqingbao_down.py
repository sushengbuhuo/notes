from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
import requests
import re
from urllib.request import urlretrieve
from fake_useragent import UserAgent
class Emoji(QWidget):
    def __init__(self):
        super(Emoji, self).__init__()
        self.init_ui()

    def init_ui(self):
        '''
        初始化UI界面布局
        :return:
        '''
        self.setWindowTitle('表情包下载器')
        self.setWindowIcon(QIcon('表情包图标.png'))
        self.setFixedSize(500, 300)

        grid = QGridLayout()

        self.page_size = QLabel()
        self.page_size.setText('默认每页数量：')

        self.page_size_text = QLineEdit()
        self.page_size_text.setText('45')
        self.page_size_text.setReadOnly(True)

        self.page_num = QLabel()
        self.page_num.setText('设置下载页数：')

        self.page_num_text = QLineEdit()
        self.page_num_text.setPlaceholderText('请输入整数 1~200')
        self.page_num_text.setValidator(QIntValidator(1, 200))

        self.save_dir = QLineEdit()
        self.save_dir.setReadOnly(True)
        self.save_dir.setPlaceholderText('图片存储路径')

        self.save_dir_btn = QPushButton()
        self.save_dir_btn.setText('设置存储路径')
        self.save_dir_btn.clicked.connect(self.save_dir_btn_click)

        self.brower = QTextBrowser()
        self.brower.setPlaceholderText('下载进度结果展示区域...')

        self.start_btn = QPushButton()
        self.start_btn.setText('开始下载表情包')
        self.start_btn.clicked.connect(self.start_btn_click)

        grid.addWidget(self.page_size, 0, 0, 1, 1)
        grid.addWidget(self.page_size_text, 0, 1, 1, 1)
        grid.addWidget(self.page_num, 1, 0, 1, 1)
        grid.addWidget(self.page_num_text, 1, 1, 1, 1)
        grid.addWidget(self.save_dir, 2, 0, 1, 1)
        grid.addWidget(self.save_dir_btn, 2, 1, 1, 1)
        grid.addWidget(self.brower, 3, 0, 1, 2)
        grid.addWidget(self.start_btn, 4, 0, 1, 2)

        self.thread_ = DownloadThread(self)
        self.thread_.finished.connect(self.finished)
        self.thread_.log.connect(self.set_log)

        self.setLayout(grid)

    def save_dir_btn_click(self):
        '''
        设置存储文件路径
        :return:
        '''
        dir = QFileDialog.getExistingDirectory(self, "选择文件夹", os.getcwd())
        self.save_dir.setText(dir)

    def start_btn_click(self):
        '''
        启动子线程下载表情包
        :return:
        '''
        self.start_btn.setEnabled(False)
        self.thread_.start()
        self.set_log('下载线程已经启动...')

    def set_log(self, text):
        '''
        更新文本浏览器内日志信息
        :param text:
        :return:
        '''
        cursor = self.brower.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.brower.append(text)
        self.brower.setTextCursor(cursor)
        self.brower.ensureCursorVisible()

    def finished(self, finished):
        if finished is True:
            self.start_btn.setEnabled(True)
class DownloadThread(QThread):
    finished = pyqtSignal(bool)
    log = pyqtSignal(str)

    def __init__(self, parent=None):
        super(DownloadThread, self).__init__(parent)
        self.parent = parent
        self.working = True

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        self.download()

    def download(self):
        user_agent = UserAgent()
        page_num = int(self.parent.page_num_text.text())
        save_dir = self.parent.save_dir.text()
        for n in range(1, page_num):
            url = 'https://www.fabiaoqing.com/biaoqing/lists/page/{}.html'.format(n)
            headers = {
                'user-agent': user_agent.random
            }
            response = requests.get(url, headers=headers)
            repx = re.compile('data-original="(.*?)" title="(.*?)"', re.I)
            texts = repx.findall(response.text)
            for text in texts:
                emoji_url = text[0].split('" src="')[0]
                emoji_name = emoji_url.split('/')[-1]
                urlretrieve(emoji_url,
                            save_dir + '/' + emoji_name)
                self.log.emit(emoji_name + ' 下载完成！')
        self.log.emit('子线程下载完成！')
        self.finished.emit(True)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Emoji()
    main.show()
    sys.exit(app.exec_())
