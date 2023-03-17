from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import pdfkit
finished = pyqtSignal(bool)
class WorkThread(QThread):
    finished = pyqtSignal(bool)
    message = pyqtSignal(str)
    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent)
        self.parent = parent
        self.working = True

    def __del__(self):
        self.working = False
        self.wait()
    def run(self):
        pdf_files_path = self.parent.pdf_files_path.text().strip()
        pdf_tar_dir = self.parent.pdf_tar_dir.text().strip()
        file_list = pdf_files_path.split(',')
        num = 0
        for file in file_list:
            if file.endswith(".html"):
                print(file)
                try:
                    pdfkit.from_file(file, pdf_tar_dir+'/'+os.path.basename(file).replace('.html', '')+'.pdf')
                except Exception as e:
                    print('错误信息:',e)
        # QMessageBox().information(None, "html文件转pdf", "转换完成", QMessageBox.Yes)
        self.finished.emit(True)
class PDFMerge(QWidget):
    def __init__(self):
        super(PDFMerge, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('html文件转pdf @公众号苏生不惑')
        self.setWindowIcon(QIcon('pdf.ico'))
        self.setFixedWidth(500)
        self.setFixedHeight(120)

        grid = QGridLayout()

        self.pdf_files_path = QLineEdit()
        self.pdf_files_path.setReadOnly(True)

        self.pdf_files_btn = QPushButton()
        self.pdf_files_btn.setText('选择文件')
        self.pdf_files_btn.clicked.connect(self.pdf_files_btn_click)

        self.pdf_tar_dir = QLineEdit()
        self.pdf_tar_dir.setReadOnly(True)

        self.pdf_tar_btn = QPushButton()
        self.pdf_tar_btn.setText('保存路径')
        self.pdf_tar_btn.clicked.connect(self.pdf_tar_btn_click)

        self.start_btn = QPushButton()
        self.start_btn.setText('开始转换')
        self.start_btn.clicked.connect(self.start_btn_click)

        grid.addWidget(self.pdf_files_path, 0, 0, 1, 1)
        grid.addWidget(self.pdf_files_btn, 0, 1, 1, 1)

        grid.addWidget(self.pdf_tar_dir, 1, 0, 1, 1)
        grid.addWidget(self.pdf_tar_btn, 1, 1, 1, 1)

        grid.addWidget(self.start_btn, 2, 0, 1, 2)

        self.thread_ = WorkThread(self)
        self.thread_.finished.connect(self.finished)

        self.setLayout(grid)

    def pdf_files_btn_click(self):
        files = QFileDialog.getOpenFileNames(self, os.getcwd(), '选择文件', 'html Files(*.html)')
        file_list = files[0]
        self.pdf_files_path.setText(','.join(file_list))

    def pdf_tar_btn_click(self):
        dir = QFileDialog.getExistingDirectory(self, os.getcwd(), '保存目录')
        self.pdf_tar_dir.setText(dir)

    def start_btn_click(self):
        self.start_btn.setEnabled(False)
        self.thread_.start()

    def finished(self, finished):
        if finished is True:
            self.start_btn.setEnabled(True)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = PDFMerge()
    main.show()
    sys.exit(app.exec_())
