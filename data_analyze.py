"""
Python数据分析平台
基于PyQt6框架开发的桌面应用程序，提供数据导入/导出、清洗转换、分析计算和可视化功能
"""
 
# 导入模块https://www.52pojie.cn/thread-2066170-1-1.html
import sys  # 系统相关功能
from PyQt6.QtWidgets import (  # PyQt6 GUI组件
    QApplication, QMainWindow, QLabel, QStatusBar, 
    QToolBar, QTableWidget, QTableWidgetItem, QMenu, QFileDialog,
    QInputDialog, QMessageBox
)
from PyQt6.QtGui import QAction  # 动作类
from PyQt6.QtCore import Qt  # Qt核心功能
import pandas as pd  # 数据处理库，用于CSV/Excel文件读取
import json  # JSON处理模块，用于JSON文件读取
import numpy as np  # 数值计算库
import matplotlib.pyplot as plt  # 数据可视化库，用于创建静态图表
import seaborn as sns  # 基于matplotlib的高级可视化库，提供更美观的统计图表
from sklearn import linear_model, preprocessing  # 机器学习库
import statsmodels.api as sm  # 统计分析库
import sqlite3  # SQLite数据库支持
import pymysql  # 添加MySQL支持库
import pymongo  # 添加MongoDB支持库
 
 
class DataAnalysisPlatform(QMainWindow):
    """
    数据分析平台主窗口类
     
    属性:
        table_widget: QTableWidget - 中央数据表格显示区
        status_bar: QStatusBar - 底部状态栏
        toolbar: QToolBar - 主工具栏
        current_file_path: str - 当前打开的文件路径
    """
     
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
         
        # 设置窗口标题和尺寸
        self.setWindowTitle("Python数据分析平台2.0")
        self.setGeometry(100, 100, 1200, 800)  # x, y, width, height
         
        # 存储当前打开的文件路径
        self.current_file_path = None
 
        # 添加MySQL连接信息的存储属性
        self.mysql_connection_info = None
        self.current_mysql_table = None
 
        # 添加MongoDB连接信息的存储属性
        self.mongo_connection_info = None
        self.current_mongo_database = None
        self.current_mongo_collection = None
         
        # 初始化UI组件
        self._init_ui()
         
    def _init_ui(self):
        """初始化用户界面"""
        # 创建中央表格部件
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)
         
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
         
        # 创建菜单栏
        self._create_menus()
         
        # 创建工具栏
        self._create_toolbar()
         
        # 设置表格右键菜单
        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self._show_context_menu)
         
    def _create_menus(self):
        """创建菜单栏"""
        # 文件菜单
        file_menu = self.menuBar().addMenu("文件")
         
        # 打开动作
        open_action = QAction("打开", self)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
 
        # 添加MySQL连接动作
        mysql_action = QAction("连接MySQL数据库", self)
        mysql_action.triggered.connect(self._connect_mysql)
        file_menu.addAction(mysql_action)
 
        # 添加MongoDB连接动作
        mongo_action = QAction("连接MongoDB数据库", self)
        mongo_action.triggered.connect(self._connect_mongo)
        file_menu.addAction(mongo_action)
         
        # 保存动作
        save_action = QAction("保存", self)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
         
        # 编辑菜单
        edit_menu = self.menuBar().addMenu("编辑")
         
        # 排序动作
        sort_action = QAction("排序", self)
        sort_action.triggered.connect(self._sort_data)
        edit_menu.addAction(sort_action)
         
        # 筛选动作
        filter_action = QAction("筛选", self)
        filter_action.triggered.connect(self._filter_data)
        edit_menu.addAction(filter_action)
         
        # 帮助菜单
        help_menu = self.menuBar().addMenu("帮助")
         
        # 关于动作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
         
     
    def _connect_mongo(self):
        """
        连接MongoDB数据库并加载数据
         
        功能: 弹出对话框让用户输入MongoDB连接信息，连接并显示数据库中的集合数据
        """
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QListWidget, QMessageBox
         
        # 创建MongoDB连接对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("连接MongoDB数据库")
        layout = QVBoxLayout()
         
        # 主机名输入
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("主机名:"))
        host_edit = QLineEdit("localhost")
        host_layout.addWidget(host_edit)
        layout.addLayout(host_layout)
         
        # 端口输入
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("端口:"))
        port_edit = QLineEdit("27017")
        port_layout.addWidget(port_edit)
        layout.addLayout(port_layout)
         
        # 用户名输入（可选）
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名:"))
        user_edit = QLineEdit()
        user_layout.addWidget(user_edit)
        layout.addLayout(user_layout)
         
        # 密码输入（可选）
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("密码:"))
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_edit)
        layout.addLayout(password_layout)
         
        # 数据库名称输入
        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("数据库名:"))
        db_edit = QLineEdit()
        db_layout.addWidget(db_edit)
        layout.addLayout(db_layout)
         
        # 按钮布局
        button_layout = QHBoxLayout()
         
        # 测试连接按钮
        test_button = QPushButton("测试连接")
        test_button.clicked.connect(lambda: self._test_mongo_connection(
            host_edit.text(), int(port_edit.text()), user_edit.text(), 
            password_edit.text(), db_edit.text()))
        button_layout.addWidget(test_button)
         
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_button)
         
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
         
        layout.addLayout(button_layout)
         
        dialog.setLayout(layout)
         
        # 显示对话框
        if dialog.exec():
            try:
                # 显示连接中消息
                self.status_bar.showMessage("正在连接MongoDB数据库...")
                 
                # 构建连接字符串
                host = host_edit.text()
                port = int(port_edit.text())
                username = user_edit.text()
                password = password_edit.text()
                database = db_edit.text()
                 
                # 保存连接信息
                self.mongo_connection_info = {
                    'host': host,
                    'port': port,
                    'username': username,
                    'password': password,
                    'database': database
                }
                 
                # 连接MongoDB
                if username and password:
                    # 有认证的连接
                    client = pymongo.MongoClient(
                        host=host,
                        port=port,
                        username=username,
                        password=password,
                        authSource=database
                    )
                else:
                    # 无认证的连接
                    client = pymongo.MongoClient(host=host, port=port)
                 
                # 获取数据库
                db = client[database]
                 
                # 获取数据库中的所有集合
                collections = db.list_collection_names()
                 
                if not collections:
                    raise ValueError("数据库中没有找到集合")
                 
                # 让用户选择要读取的集合
                collection_name, ok = QInputDialog.getItem(
                    self,
                    "选择数据集合",
                    "请选择要读取的数据集合:",
                    collections,
                    0,
                    False
                )
                 
                if not ok or not collection_name:
                    client.close()
                    self.status_bar.showMessage("连接已取消")
                    return
                 
                # 保存当前数据库和集合名
                self.current_mongo_database = database
                self.current_mongo_collection = collection_name
                 
                # 读取集合数据
                collection = db[collection_name]
                data = list(collection.find())
                 
                # 转换为DataFrame
                if data:
                    # 处理MongoDB的_id字段
                    for item in data:
                        if '_id' in item:
                            item['_id'] = str(item['_id'])
                     
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame()  # 空数据框
                 
                # 清空现有表格
                self.table_widget.clear()
                 
                if not df.empty:
                    # 设置表格行列数
                    self.table_widget.setRowCount(df.shape[0])
                    self.table_widget.setColumnCount(df.shape[1])
                     
                    # 设置表头
                    self.table_widget.setHorizontalHeaderLabels(df.columns.tolist())
                     
                    # 填充表格数据
                    for i in range(df.shape[0]):
                        for j in range(df.shape[1]):
                            value = str(df.iloc[i, j]) if pd.notna(df.iloc[i, j]) else ""
                            item = QTableWidgetItem(value)
                            self.table_widget.setItem(i, j, item)
                 
                # 关闭连接
                client.close()
                 
                # 清除其他连接信息
                self.current_file_path = None
                self.mysql_connection_info = None
                self.current_mysql_table = None
                 
                # 显示成功消息
                self.status_bar.showMessage(f"已连接MongoDB数据库: {database}, 集合: {collection_name}")
                 
            except Exception as e:
                # 显示错误消息
                self.status_bar.showMessage(f"连接MongoDB数据库失败: {str(e)}")
                QMessageBox.critical(self, "连接失败", f"无法连接MongoDB数据库: {str(e)}")
 
    def _test_mongo_connection(self, host, port, username, password, database):
        """
        测试MongoDB连接
         
        参数:
            host: str - 主机名
            port: int - 端口号
            username: str - 用户名
            password: str - 密码
            database: str - 数据库名
        """
        try:
            # 显示测试中消息
            self.status_bar.showMessage("正在测试MongoDB连接...")
             
            # 连接MongoDB
            if username and password:
                # 有认证的连接
                client = pymongo.MongoClient(
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    authSource=database,
                    serverSelectionTimeoutMS=2000  # 2秒超时
                )
            else:
                # 无认证的连接
                client = pymongo.MongoClient(
                    host=host, 
                    port=port,
                    serverSelectionTimeoutMS=2000  # 2秒超时
                )
             
            # 尝试获取数据库信息
            client.server_info()
             
            # 关闭连接
            client.close()
             
            # 显示成功消息
            self.status_bar.showMessage("MongoDB连接测试成功")
            QMessageBox.information(self, "连接成功", "MongoDB连接测试成功！")
             
        except Exception as e:
            # 显示错误消息
            self.status_bar.showMessage(f"MongoDB连接测试失败: {str(e)}")
            QMessageBox.critical(self, "连接失败", f"MongoDB连接测试失败: {str(e)}")
 
 
 
    def _connect_mysql(self):
        """
        连接MySQL数据库并加载数据
         
        功能: 弹出对话框让用户输入MySQL连接信息，连接并显示数据库中的表数据
        """
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
         
        # 创建MySQL连接对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("连接MySQL数据库")
        layout = QVBoxLayout()
         
        # 主机名输入
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("主机名:"))
        host_edit = QLineEdit("localhost")
        host_layout.addWidget(host_edit)
        layout.addLayout(host_layout)
         
        # 端口输入
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("端口:"))
        port_edit = QLineEdit("3306")
        port_layout.addWidget(port_edit)
        layout.addLayout(port_layout)
         
        # 用户名输入
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("用户名:"))
        user_edit = QLineEdit()
        user_layout.addWidget(user_edit)
        layout.addLayout(user_layout)
         
        # 密码输入
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("密码:"))
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_edit)
        layout.addLayout(password_layout)
         
        # 数据库名输入
        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("数据库名:"))
        db_edit = QLineEdit()
        db_layout.addWidget(db_edit)
        layout.addLayout(db_layout)
         
        # 测试连接按钮
        test_btn = QPushButton("测试连接")
        layout.addWidget(test_btn)
         
        # 连接状态标签
        status_label = QLabel("")
        layout.addWidget(status_label)
         
        # 确定/取消按钮
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
         
        dialog.setLayout(layout)
         
        # 测试连接功能
        def test_connection():
            try:
                conn = pymysql.connect(
                    host=host_edit.text(),
                    port=int(port_edit.text()),
                    user=user_edit.text(),
                    password=password_edit.text(),
                    db=db_edit.text() if db_edit.text() else None
                )
                conn.close()
                status_label.setText("连接成功!")
                status_label.setStyleSheet("color: green;")
            except Exception as e:
                status_label.setText(f"连接失败: {str(e)}")
                status_label.setStyleSheet("color: red;")
         
        test_btn.clicked.connect(test_connection)
         
        # 确定按钮功能
        def on_accept():
            try:
                # 获取连接信息
                host = host_edit.text()
                port = int(port_edit.text())
                user = user_edit.text()
                password = password_edit.text()
                database = db_edit.text()
                 
                # 连接MySQL数据库
                conn = pymysql.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    db=database
                )
                 
                # 获取数据库中的所有表
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                cursor.close()
                 
                if not tables:
                    conn.close()
                    raise ValueError("数据库中没有找到表")
                 
                # 如果只有一个表，直接读取；如果有多个表，让用户选择
                if len(tables) == 1:
                    table_name = tables[0]
                else:
                    # 显示表选择对话框
                    table_name, ok = QInputDialog.getItem(
                        self,
                        "选择数据表",
                        "请选择要读取的数据表:",
                        tables,
                        0,
                        False
                    )
                     
                    if not ok or not table_name:
                        conn.close()
                        dialog.reject()
                        return
                 
                # 读取选定表的数据
                data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                conn.close()
                 
                # 清空现有表格
                self.table_widget.clear()
                 
                # 设置表格行列数
                self.table_widget.setRowCount(data.shape[0])  # 行数为数据行数
                self.table_widget.setColumnCount(data.shape[1])  # 列数为数据列数
                 
                # 设置表头
                self.table_widget.setHorizontalHeaderLabels(data.columns.tolist())
                 
                # 填充表格数据
                for i in range(data.shape[0]):  # 遍历每一行
                    for j in range(data.shape[1]):  # 遍历每一列
                        # 获取单元格值，处理NaN值为空字符串
                        value = str(data.iloc[i, j]) if not pd.isna(data.iloc[i, j]) else ""
                        # 创建表格项并设置值
                        item = QTableWidgetItem(value)
                        self.table_widget.setItem(i, j, item)
                 
                # 保存MySQL连接信息，以便刷新功能使用
                self.mysql_connection_info = {
                    'host': host,
                    'port': port,
                    'user': user,
                    'password': password,
                    'database': database
                }
                self.current_mysql_table = table_name
                self.current_file_path = None  # 清除文件路径，以便刷新时使用MySQL连接
                 
                # 显示成功消息
                self.status_bar.showMessage(f"成功从MySQL数据库加载表: {table_name}")
                 
                dialog.accept()
            except Exception as e:
                # 显示错误消息
                self.status_bar.showMessage(f"连接MySQL失败: {str(e)}")
                QMessageBox.critical(self, "连接失败", f"无法连接到MySQL数据库: {str(e)}")
         
        ok_btn.clicked.connect(on_accept)
        cancel_btn.clicked.connect(dialog.reject)
         
        # 显示对话框
        dialog.exec()
 
         
    def _create_toolbar(self):
        """创建工具栏"""
        self.toolbar = QToolBar("主工具栏")
        self.addToolBar(self.toolbar)
         
        # 添加工具按钮
        open_action = QAction("打开", self)
        open_action.triggered.connect(self._open_file)
        self.toolbar.addAction(open_action)
         
        save_action = QAction("保存", self)
        save_action.triggered.connect(self._save_file)
        self.toolbar.addAction(save_action)
         
        # 添加刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self._refresh_data)
        self.toolbar.addAction(refresh_action)
         
        self.toolbar.addSeparator()
         
        sort_action = QAction("排序", self)
        sort_action.triggered.connect(self._sort_data)
        self.toolbar.addAction(sort_action)
         
        filter_action = QAction("筛选", self)
        filter_action.triggered.connect(self._filter_data)
        self.toolbar.addAction(filter_action)
         
        self.toolbar.addSeparator()
         
        analyze_action = QAction("分析", self)
        analyze_action.triggered.connect(self._data_analysis)
        self.toolbar.addAction(analyze_action)
         
        # 可视化按钮并连接信号槽
        visualize_action = QAction("可视化", self)
        visualize_action.triggered.connect(self._visualize_data)
        self.toolbar.addAction(visualize_action)
 
 
 
    def _copy_data(self):
        """复制选中单元格数据到剪贴板"""
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            self.status_bar.showMessage("没有选中要复制的数据")
            return
             
        # 获取选中单元格的文本内容
        data = []
        current_row = -1
         
        for item in selected_items:
            if item.row() != current_row:
                data.append([])
                current_row = item.row()
            data[-1].append(item.text())
         
        # 将数据转换为制表符分隔的字符串
        text = "\n".join("\t".join(row) for row in data)
         
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.status_bar.showMessage(f"已复制 {len(selected_items)} 个单元格数据")
         
    def _paste_data(self):
        """从剪贴板粘贴数据到表格"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
         
        if not text:
            self.status_bar.showMessage("剪贴板中没有数据")
            return
             
        try:
            # 解析剪贴板数据（制表符分隔的行，换行符分隔的列）
            data = [row.split("\t") for row in text.split("\n") if row]
             
            # 获取当前选中单元格位置
            selected_items = self.table_widget.selectedItems()
            start_row = selected_items[0].row() if selected_items else 0
            start_col = selected_items[0].column() if selected_items else 0
             
            # 将数据粘贴到表格中
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    target_row = start_row + row_idx
                    target_col = start_col + col_idx
                     
                    # 确保表格有足够的行和列
                    if target_row >= self.table_widget.rowCount():
                        self.table_widget.insertRow(target_row)
                    if target_col >= self.table_widget.columnCount():
                        self.table_widget.insertColumn(target_col)
                     
                    # 设置单元格数据
                    item = QTableWidgetItem(cell_data)
                    self.table_widget.setItem(target_row, target_col, item)
             
            self.status_bar.showMessage(f"已粘贴 {len(data)} 行数据")
        except Exception as e:
            self.status_bar.showMessage(f"粘贴失败: {str(e)}")
         
    def _show_context_menu(self, position):
        """显示表格右键菜单"""
        menu = QMenu()
         
        # 获取当前点击的行
        row = self.table_widget.rowAt(position.y())
        col = self.table_widget.columnAt(position.x())
         
        # 添加菜单项并连接功能
        copy_action = menu.addAction("复制")
        copy_action.triggered.connect(self._copy_data)
         
        paste_action = menu.addAction("粘贴")
        paste_action.triggered.connect(self._paste_data)
         
        menu.addSeparator()
         
        delete_action = menu.addAction("删除行")
        delete_action.triggered.connect(lambda: self._delete_row(row))
         
        insert_action = menu.addAction("插入行")
        insert_action.triggered.connect(lambda: self._insert_row(row))
         
        menu.addSeparator()
         
        add_col_action = menu.addAction("添加列")
        add_col_action.triggered.connect(self._add_column)
         
        remove_col_action = menu.addAction("删除列")
        remove_col_action.triggered.connect(self._remove_column)
         
        # 新增编辑列名功能
        if col >= 0:  # 确保点击的是有效的列
            edit_col_action = menu.addAction("编辑列名")
            edit_col_action.triggered.connect(lambda: self._edit_column_name(col))
         
        # 显示菜单
        menu.exec(self.table_widget.viewport().mapToGlobal(position))
         
    def _edit_column_name(self, col):
        """编辑指定列的列名"""
        from PyQt6.QtWidgets import QInputDialog
         
        # 获取当前列名
        current_name = self.table_widget.horizontalHeaderItem(col).text()
         
        # 弹出输入对话框
        new_name, ok = QInputDialog.getText(
            self,
            "编辑列名",
            "请输入新的列名:",
            text=current_name
        )
         
        if ok and new_name:
            # 更新列名
            self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(new_name))
            self.status_bar.showMessage(f"已更新列名: {current_name} -> {new_name}")
 
    def _add_column(self):
        """在表格末尾添加新列"""
        col = self.table_widget.columnCount()
        self.table_widget.insertColumn(col)
        self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(f"列{col+1}"))
        self.status_bar.showMessage(f"已添加第{col+1}列")
         
    def _remove_column(self):
        """删除当前选中列"""
        col = self.table_widget.currentColumn()
        if col >= 0:
            self.table_widget.removeColumn(col)
            self.status_bar.showMessage(f"已删除第{col+1}列")
        else:
            self.status_bar.showMessage("请先选择要删除的列")
         
    def _insert_row(self, row):
        """在指定位置插入新行"""
        self.table_widget.insertRow(row)
        # 初始化新行的单元格
        for col in range(self.table_widget.columnCount()):
            self.table_widget.setItem(row, col, QTableWidgetItem(""))
         
    def _delete_row(self, row):
        """删除指定行"""
        if row >= 0:
            self.table_widget.removeRow(row)
         
 
    # def _open_file(self):
    #     """
    #     打开数据文件并加载到表格中
         
    #     支持格式: CSV/Excel/JSON/SQLite
    #     功能: 通过文件对话框选择文件，读取数据并显示在表格中
    #     """
    #     from PyQt6.QtWidgets import QFileDialog  # 文件对话框组件
    #     import pandas as pd  # 数据处理库
    #     import json  # JSON处理模块
    #     import sqlite3  # SQLite数据库支持
         
    #     # 设置文件过滤器，支持多种格式（新增SQLite格式）
    #     file_filter = "数据文件 (*.csv *.xlsx *.json *.db *.sqlite);;CSV文件 (*.csv);;Excel文件 (*.xlsx);;JSON文件 (*.json);;SQLite数据库 (*.db *.sqlite)"
         
    #     # 弹出文件选择对话框
    #     file_path, _ = QFileDialog.getOpenFileName(
    #         self, 
    #         "打开数据文件",  # 对话框标题
    #         "",  # 初始目录
    #         file_filter  # 文件过滤器
    #     )
         
    #     # 如果用户选择了文件
    #     if file_path:
    #         try:
    #             # 根据文件扩展名选择不同的读取方式
    #             if file_path.endswith('.csv'):
    #                 # 读取CSV文件
    #                 data = pd.read_csv(file_path)  # 使用pandas读取CSV
    #             elif file_path.endswith('.xlsx'):
    #                 # 读取Excel文件
    #                 data = pd.read_excel(file_path)  # 使用pandas读取Excel
    #             elif file_path.endswith('.json'):
    #                 # 读取JSON文件
    #                 with open(file_path, 'r', encoding='utf-8') as f:
    #                     json_data = json.load(f)  # 加载JSON数据
    #                 data = pd.DataFrame(json_data)  # 转换为DataFrame
    #             elif file_path.endswith(('.db', '.sqlite')):
    #                 # 读取SQLite数据库文件
    #                 conn = sqlite3.connect(file_path)
                     
    #                 # 获取数据库中的所有表
    #                 cursor = conn.cursor()
    #                 cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #                 tables = [table[0] for table in cursor.fetchall()]
    #                 cursor.close()
                     
    #                 if not tables:
    #                     raise ValueError("数据库中没有找到表")
                     
    #                 # 如果只有一个表，直接读取；如果有多个表，让用户选择
    #                 if len(tables) == 1:
    #                     table_name = tables[0]
    #                 else:
    #                     # 显示表选择对话框
    #                     table_name, ok = QInputDialog.getItem(
    #                         self,
    #                         "选择数据表",
    #                         "请选择要读取的数据表:",
    #                         tables,
    #                         0,
    #                         False
    #                     )
                         
    #                     if not ok or not table_name:
    #                         conn.close()
    #                         return
                     
    #                 # 读取选定表的数据
    #                 data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    #                 conn.close()
    #             else:
    #                 raise ValueError("不支持的文件格式")
                 
    #             # 清空现有表格
    #             self.table_widget.clear()
                 
    #             # 设置表格行列数
    #             self.table_widget.setRowCount(data.shape[0])  # 行数为数据行数
    #             self.table_widget.setColumnCount(data.shape[1])  # 列数为数据列数
                 
    #             # 设置表头
    #             self.table_widget.setHorizontalHeaderLabels(data.columns.tolist())
                 
    #             # 填充表格数据
    #             for i in range(data.shape[0]):  # 遍历每一行
    #                 for j in range(data.shape[1]):  # 遍历每一列
    #                     # 获取单元格值，处理NaN值为空字符串
    #                     value = str(data.iloc[i, j]) if not pd.isna(data.iloc[i, j]) else ""
    #                     # 创建表格项并设置值
    #                     item = QTableWidgetItem(value)
    #                     self.table_widget.setItem(i, j, item)
                 
    #             # 显示成功消息
    #             self.status_bar.showMessage(f"成功加载文件: {file_path}")
                 
    #         except Exception as e:
    #             # 显示错误消息
    #             self.status_bar.showMessage(f"加载文件失败: {str(e)}")
 
    def _open_file(self):
        """
        打开数据文件并加载到表格中
         
        支持格式: CSV/Excel/JSON/SQLite
        功能: 通过文件对话框选择文件，读取数据并显示在表格中
        """
        from PyQt6.QtWidgets import QFileDialog  # 文件对话框组件
        import pandas as pd  # 数据处理库
        import json  # JSON处理模块
        import sqlite3  # SQLite数据库支持
         
        # 设置文件过滤器，支持多种格式（新增SQLite格式）
        file_filter = "数据文件 (*.csv *.xlsx *.json *.db *.sqlite);;CSV文件 (*.csv);;Excel文件 (*.xlsx);;JSON文件 (*.json);;SQLite数据库 (*.db *.sqlite)"
         
        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "打开数据文件",  # 对话框标题
            "",  # 初始目录
            file_filter  # 文件过滤器
        )
         
        # 如果用户选择了文件
        if file_path:
            try:
                # 保存当前文件路径
                self.current_file_path = file_path
                 
                # 根据文件扩展名选择不同的读取方式
                if file_path.endswith('.csv'):
                    # 读取CSV文件
                    data = pd.read_csv(file_path)  # 使用pandas读取CSV
                elif file_path.endswith('.xlsx'):
                    # 读取Excel文件
                    data = pd.read_excel(file_path)  # 使用pandas读取Excel
                elif file_path.endswith('.json'):
                    # 读取JSON文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)  # 加载JSON数据
                    data = pd.DataFrame(json_data)  # 转换为DataFrame
                elif file_path.endswith(('.db', '.sqlite')):
                    # 读取SQLite数据库文件
                    conn = sqlite3.connect(file_path)
                     
                    # 获取数据库中的所有表
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [table[0] for table in cursor.fetchall()]
                    cursor.close()
                     
                    if not tables:
                        raise ValueError("数据库中没有找到表")
                     
                    # 如果只有一个表，直接读取；如果有多个表，让用户选择
                    if len(tables) == 1:
                        table_name = tables[0]
                    else:
                        # 显示表选择对话框
                        table_name, ok = QInputDialog.getItem(
                            self,
                            "选择数据表",
                            "请选择要读取的数据表:",
                            tables,
                            0,
                            False
                        )
                         
                        if not ok or not table_name:
                            conn.close()
                            return
                     
                    # 读取选定表的数据
                    data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    conn.close()
                else:
                    raise ValueError("不支持的文件格式")
                 
                # 清空现有表格
                self.table_widget.clear()
                 
                # 设置表格行列数
                self.table_widget.setRowCount(data.shape[0])  # 行数为数据行数
                self.table_widget.setColumnCount(data.shape[1])  # 列数为数据列数
                 
                # 设置表头
                self.table_widget.setHorizontalHeaderLabels(data.columns.tolist())
                 
                # 填充表格数据
                for i in range(data.shape[0]):  # 遍历每一行
                    for j in range(data.shape[1]):  # 遍历每一列
                        # 获取单元格值，处理NaN值为空字符串
                        value = str(data.iloc[i, j]) if not pd.isna(data.iloc[i, j]) else ""
                        # 创建表格项并设置值
                        item = QTableWidgetItem(value)
                        self.table_widget.setItem(i, j, item)
                 
                # 显示成功消息
                self.status_bar.showMessage(f"成功加载文件: {file_path}")
                 
            except Exception as e:
                # 显示错误消息
                self.status_bar.showMessage(f"加载文件失败: {str(e)}")
 
 
    def _refresh_data(self):
        """
        刷新表格数据
         
        功能: 重新加载当前打开的文件或MySQL数据库，更新表格数据
        """
        if self.current_file_path:
            try:
                # 显示刷新中消息
                self.status_bar.showMessage("正在刷新数据...")
                 
                # 重新打开文件（复用_open_file方法的逻辑）
                # 这里我们通过临时变量来存储和恢复文件路径，避免在_open_file中覆盖
                temp_file_path = self.current_file_path
                self.current_file_path = None
                 
                # 创建一个模拟的QFileDialog结果
                from PyQt6.QtWidgets import QFileDialog
                 
                file_path = temp_file_path
                 
                # 根据文件扩展名选择不同的读取方式
                if file_path.endswith('.csv'):
                    # 读取CSV文件
                    data = pd.read_csv(file_path)  # 使用pandas读取CSV
                elif file_path.endswith('.xlsx'):
                    # 读取Excel文件
                    data = pd.read_excel(file_path)  # 使用pandas读取Excel
                elif file_path.endswith('.json'):
                    # 读取JSON文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)  # 加载JSON数据
                    data = pd.DataFrame(json_data)  # 转换为DataFrame
                elif file_path.endswith(('.db', '.sqlite')):
                    # 读取SQLite数据库文件
                    conn = sqlite3.connect(file_path)
                     
                    # 获取数据库中的所有表
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [table[0] for table in cursor.fetchall()]
                    cursor.close()
                     
                    if not tables:
                        raise ValueError("数据库中没有找到表")
                     
                    # 如果只有一个表，直接读取；如果有多个表，让用户选择
                    if len(tables) == 1:
                        table_name = tables[0]
                    else:
                        # 显示表选择对话框
                        table_name, ok = QInputDialog.getItem(
                            self,
                            "选择数据表",
                            "请选择要读取的数据表:",
                            tables,
                            0,
                            False
                        )
                         
                        if not ok or not table_name:
                            conn.close()
                            self.current_file_path = temp_file_path
                            return
                     
                    # 读取选定表的数据
                    data = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    conn.close()
                else:
                    raise ValueError("不支持的文件格式")
                 
                # 清空现有表格
                self.table_widget.clear()
                 
                # 设置表格行列数
                self.table_widget.setRowCount(data.shape[0])  # 行数为数据行数
                self.table_widget.setColumnCount(data.shape[1])  # 列数为数据列数
                 
                # 设置表头
                self.table_widget.setHorizontalHeaderLabels(data.columns.tolist())
                 
                # 填充表格数据
                for i in range(data.shape[0]):  # 遍历每一行
                    for j in range(data.shape[1]):  # 遍历每一列
                        # 获取单元格值，处理NaN值为空字符串
                        value = str(data.iloc[i, j]) if not pd.isna(data.iloc[i, j]) else ""
                        # 创建表格项并设置值
                        item = QTableWidgetItem(value)
                        self.table_widget.setItem(i, j, item)
                 
                # 恢复当前文件路径
                self.current_file_path = temp_file_path
                 
                # 显示成功消息
                self.status_bar.showMessage(f"数据已刷新: {file_path}")
                 
            except Exception as e:
                # 恢复当前文件路径
                self.current_file_path = temp_file_path
                # 显示错误消息
                self.status_bar.showMessage(f"刷新数据失败: {str(e)}")
        elif self.mysql_connection_info and self.current_mysql_table:
            # 处理MySQL数据库刷新
            try:
                # 显示刷新中消息
                self.status_bar.showMessage("正在刷新MySQL数据...")
                 
                # 使用保存的连接信息连接MySQL数据库
                conn = pymysql.connect(
                    host=self.mysql_connection_info['host'],
                    port=self.mysql_connection_info['port'],
                    user=self.mysql_connection_info['user'],
                    password=self.mysql_connection_info['password'],
                    db=self.mysql_connection_info['database']
                )
                 
                # 读取选定表的数据
                data = pd.read_sql_query(f"SELECT * FROM {self.current_mysql_table}", conn)
                conn.close()
                 
                # 清空现有表格
                self.table_widget.clear()
                 
                # 设置表格行列数
                self.table_widget.setRowCount(data.shape[0])  # 行数为数据行数
                self.table_widget.setColumnCount(data.shape[1])  # 列数为数据列数
                 
                # 设置表头
                self.table_widget.setHorizontalHeaderLabels(data.columns.tolist())
                 
                # 填充表格数据
                for i in range(data.shape[0]):  # 遍历每一行
                    for j in range(data.shape[1]):  # 遍历每一列
                        # 获取单元格值，处理NaN值为空字符串
                        value = str(data.iloc[i, j]) if not pd.isna(data.iloc[i, j]) else ""
                        # 创建表格项并设置值
                        item = QTableWidgetItem(value)
                        self.table_widget.setItem(i, j, item)
                 
                # 显示成功消息
                self.status_bar.showMessage(f"已刷新MySQL数据库表: {self.current_mysql_table}")
                 
            except Exception as e:
                # 显示错误消息
                self.status_bar.showMessage(f"刷新MySQL数据失败: {str(e)}")
         
        elif self.mongo_connection_info and self.current_mongo_database and self.current_mongo_collection:
            # 处理MongoDB数据库刷新
            try:
                # 显示刷新中消息
                self.status_bar.showMessage("正在刷新MongoDB数据...")
                 
                # 获取连接信息
                host = self.mongo_connection_info['host']
                port = self.mongo_connection_info['port']
                username = self.mongo_connection_info['username']
                password = self.mongo_connection_info['password']
                database = self.mongo_connection_info['database']
                collection_name = self.current_mongo_collection
                 
                # 连接MongoDB
                if username and password:
                    # 有认证的连接
                    client = pymongo.MongoClient(
                        host=host,
                        port=port,
                        username=username,
                        password=password,
                        authSource=database
                    )
                else:
                    # 无认证的连接
                    client = pymongo.MongoClient(host=host, port=port)
                 
                # 获取数据库和集合
                db = client[database]
                collection = db[collection_name]
                 
                # 读取集合数据
                data = list(collection.find())
                 
                # 转换为DataFrame
                if data:
                    # 处理MongoDB的_id字段
                    for item in data:
                        if '_id' in item:
                            item['_id'] = str(item['_id'])
                     
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame()  # 空数据框
                 
                # 清空现有表格
                self.table_widget.clear()
                 
                if not df.empty:
                    # 设置表格行列数
                    self.table_widget.setRowCount(df.shape[0])
                    self.table_widget.setColumnCount(df.shape[1])
                     
                    # 设置表头
                    self.table_widget.setHorizontalHeaderLabels(df.columns.tolist())
                     
                    # 填充表格数据
                    for i in range(df.shape[0]):
                        for j in range(df.shape[1]):
                            value = str(df.iloc[i, j]) if pd.notna(df.iloc[i, j]) else ""
                            item = QTableWidgetItem(value)
                            self.table_widget.setItem(i, j, item)
                 
                # 关闭连接
                client.close()
                 
                # 显示成功消息
                self.status_bar.showMessage(f"已刷新MongoDB数据库: {database}, 集合: {collection_name}")
                 
            except Exception as e:
                # 显示错误消息
                self.status_bar.showMessage(f"刷新MongoDB数据失败: {str(e)}")
        else:
            # 更新提示消息，包含MongoDB
            self.status_bar.showMessage("没有打开的文件或数据库连接可供刷新")
 
 
         
    #########################
 
    def _save_file(self):
        """
        保存表格数据到文件
         
        支持格式: CSV/Excel/JSON/SQLite/MySQL/MongoDB
        功能: 通过文件对话框选择保存路径和格式，将表格数据保存到指定文件或数据库
        """
        from PyQt6.QtWidgets import QFileDialog, QInputDialog, QMessageBox  # 文件对话框组件
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
        from PyQt6.QtCore import Qt
        import sqlite3  # SQLite数据库支持
        import pymysql  # MySQL数据库支持
        import pymongo  # MongoDB数据库支持
        from sqlalchemy import create_engine  # 添加SQLAlchemy支持，用于处理MySQL连接
        from pymongo import MongoClient
        import json
         
        # 检查表格是否有数据
        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            self.status_bar.showMessage("表格中没有数据可保存")
            return
         
        # 创建保存选项对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("选择保存方式")
        dialog.resize(300, 250)
         
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("请选择要将数据保存到哪种格式:"))
         
        # 创建选项按钮组
        btn_layout = QVBoxLayout()
         
        # 创建按钮
        csv_btn = QPushButton("CSV文件 (*.csv)")
        excel_btn = QPushButton("Excel文件 (*.xlsx)")
        json_btn = QPushButton("JSON文件 (*.json)")
        sqlite_btn = QPushButton("SQLite数据库 (*.db)")
        mysql_btn = QPushButton("MySQL数据库")
        mongo_btn = QPushButton("MongoDB数据库")  # 添加MongoDB按钮
         
        # 添加按钮到布局
        btn_layout.addWidget(csv_btn)
        btn_layout.addWidget(excel_btn)
        btn_layout.addWidget(json_btn)
        btn_layout.addWidget(sqlite_btn)
        btn_layout.addWidget(mysql_btn)
        btn_layout.addWidget(mongo_btn)  # 添加MongoDB按钮
         
        layout.addLayout(btn_layout)
         
        # 从表格中提取数据
        data = []
        headers = []
         
        # 获取表头
        for col in range(self.table_widget.columnCount()):
            header = self.table_widget.horizontalHeaderItem(col)
            headers.append(header.text() if header else f"Column{col+1}")
         
        # 获取表格数据
        for row in range(self.table_widget.rowCount()):
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
         
        # 创建DataFrame
        df = pd.DataFrame(data, columns=headers)
         
        # 定义保存函数 - 保留原有功能
        def save_to_csv():
            try:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "保存为CSV文件", "", "CSV文件 (*.csv)"
                )
                if file_path:
                    if not file_path.endswith('.csv'):
                        file_path += '.csv'
                    df.to_csv(file_path, index=False, encoding='utf-8-sig')
                    self.status_bar.showMessage(f"数据已成功保存到CSV文件: {file_path}")
                dialog.close()
            except Exception as e:
                self.status_bar.showMessage(f"保存CSV文件失败: {str(e)}")
                dialog.close()
         
        def save_to_excel():
            try:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "保存为Excel文件", "", "Excel文件 (*.xlsx)"
                )
                if file_path:
                    if not file_path.endswith('.xlsx'):
                        file_path += '.xlsx'
                    df.to_excel(file_path, index=False)
                    self.status_bar.showMessage(f"数据已成功保存到Excel文件: {file_path}")
                dialog.close()
            except Exception as e:
                self.status_bar.showMessage(f"保存Excel文件失败: {str(e)}")
                dialog.close()
         
        def save_to_json():
            try:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "保存为JSON文件", "", "JSON文件 (*.json)"
                )
                if file_path:
                    if not file_path.endswith('.json'):
                        file_path += '.json'
                    df.to_json(file_path, orient='records', force_ascii=False, indent=4)
                    self.status_bar.showMessage(f"数据已成功保存到JSON文件: {file_path}")
                dialog.close()
            except Exception as e:
                self.status_bar.showMessage(f"保存JSON文件失败: {str(e)}")
                dialog.close()
         
        def save_to_sqlite():
            try:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "保存到SQLite数据库", "", "SQLite数据库 (*.db *.sqlite)"
                )
                if file_path:
                    # 确保文件扩展名正确
                    if not (file_path.endswith('.db') or file_path.endswith('.sqlite')):
                        file_path += '.db'
                     
                    # 让用户输入表名
                    table_name, ok = QInputDialog.getText(
                        self,
                        "输入表名",
                        "请输入要保存的表名:",
                        text="data_table"
                    )
                     
                    if ok and table_name.strip():
                        # 连接到SQLite数据库
                        conn = sqlite3.connect(file_path)
                         
                        # 检查表是否已存在
                        cursor = conn.cursor()
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                        table_exists = cursor.fetchone() is not None
                        cursor.close()
                         
                        # 如果表已存在，询问用户是否覆盖
                        if table_exists:
                            reply = QMessageBox.question(
                                self,
                                "表已存在",
                                f"表 '{table_name}' 已存在，是否覆盖？",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                             
                            if reply == QMessageBox.StandardButton.No:
                                conn.close()
                                self.status_bar.showMessage("取消保存到SQLite数据库")
                                dialog.close()
                                return
                         
                        # 将数据写入SQLite表
                        df.to_sql(table_name, conn, if_exists='replace', index=False)
                         
                        # 关闭连接
                        conn.close()
                        self.status_bar.showMessage(f"数据已成功保存到SQLite数据库: {file_path} 表: {table_name}")
                dialog.close()
            except Exception as e:
                self.status_bar.showMessage(f"保存到SQLite数据库失败: {str(e)}")
                dialog.close()
         
        def save_to_mysql():
            try:
                # 如果之前有MySQL连接信息，可以直接使用
                if hasattr(self, 'mysql_connection_info') and self.mysql_connection_info:
                    use_last_conn = QMessageBox.question(
                        self,
                        "使用上次连接",
                        "是否使用上次的MySQL连接信息？",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                     
                    if use_last_conn == QMessageBox.StandardButton.Yes:
                        # 直接使用上次的连接信息
                        host, port, user, password, db = self.mysql_connection_info
                         
                        # 让用户输入表名
                        table_name, ok = QInputDialog.getText(
                            self,
                            "输入表名",
                            "请输入要保存的表名:",
                            text="data_table"
                        )
                         
                        if ok and table_name.strip():
                            try:
                                # 创建SQLAlchemy引擎用于MySQL连接
                                engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4")
                                 
                                # 连接MySQL数据库
                                conn = engine.connect()
                                 
                                # 检查表是否已存在（使用SQLAlchemy Core）
                                from sqlalchemy import inspect
                                inspector = inspect(engine)
                                table_exists = table_name in inspector.get_table_names()
                                 
                                # 如果表已存在，询问用户是否覆盖
                                if table_exists:
                                    reply = QMessageBox.question(
                                        self,
                                        "表已存在",
                                        f"表 '{table_name}' 已存在，是否覆盖？",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                    )
                                     
                                    if reply == QMessageBox.StandardButton.No:
                                        conn.close()
                                        self.status_bar.showMessage("取消保存到MySQL数据库")
                                        dialog.close()
                                        return
                                 
                                # 将数据写入MySQL表
                                df.to_sql(table_name, engine, if_exists='replace', index=False)
                                 
                                # 关闭连接
                                conn.close()
                                self.status_bar.showMessage(f"数据已成功保存到MySQL数据库: {db} 表: {table_name}")
                            except Exception as e:
                                self.status_bar.showMessage(f"保存到MySQL数据库失败: {str(e)}")
                        dialog.close()
                        return
                 
                # 创建MySQL连接对话框
                mysql_dialog = QDialog(self)
                mysql_dialog.setWindowTitle("连接MySQL数据库")
                mysql_dialog.resize(400, 300)
                 
                mysql_layout = QVBoxLayout(mysql_dialog)
                 
                # 主机名/IP地址
                host_layout = QHBoxLayout()
                host_layout.addWidget(QLabel("主机名/IP地址:"))
                host_input = QLineEdit("localhost")
                host_layout.addWidget(host_input)
                mysql_layout.addLayout(host_layout)
                 
                # 端口号
                port_layout = QHBoxLayout()
                port_layout.addWidget(QLabel("端口号:"))
                port_input = QLineEdit("3306")
                port_layout.addWidget(port_input)
                mysql_layout.addLayout(port_layout)
                 
                # 用户名
                user_layout = QHBoxLayout()
                user_layout.addWidget(QLabel("用户名:"))
                user_input = QLineEdit()
                user_layout.addWidget(user_input)
                mysql_layout.addLayout(user_layout)
                 
                # 密码
                pwd_layout = QHBoxLayout()
                pwd_layout.addWidget(QLabel("密码:"))
                pwd_input = QLineEdit()
                pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
                pwd_layout.addWidget(pwd_input)
                mysql_layout.addLayout(pwd_layout)
                 
                # 数据库名
                db_layout = QHBoxLayout()
                db_layout.addWidget(QLabel("数据库名:"))
                db_input = QLineEdit()
                db_layout.addWidget(db_input)
                mysql_layout.addLayout(db_layout)
                 
                # 表名
                table_layout = QHBoxLayout()
                table_layout.addWidget(QLabel("表名:"))
                table_input = QLineEdit("data_table")
                table_layout.addWidget(table_input)
                mysql_layout.addLayout(table_layout)
                 
                # 按钮布局
                btn_layout = QHBoxLayout()
                 
                # 测试连接按钮
                test_btn = QPushButton("测试连接")
                btn_layout.addWidget(test_btn)
                 
                # 确定/取消按钮
                ok_btn = QPushButton("确定")
                cancel_btn = QPushButton("取消")
                btn_layout.addWidget(ok_btn)
                btn_layout.addWidget(cancel_btn)
                 
                mysql_layout.addLayout(btn_layout)
                 
                # 测试连接功能
                def _test_connection():
                    try:
                        host = host_input.text()
                        port = int(port_input.text())
                        user = user_input.text()
                        password = pwd_input.text()
                        db = db_input.text()
                         
                        if not user or not db:
                            QMessageBox.warning(self, "输入错误", "用户名和数据库名不能为空")
                            return
                         
                        # 连接到MySQL数据库
                        conn = pymysql.connect(
                            host=host,
                            port=port,
                            user=user,
                            password=password,
                            database=db,
                            charset='utf8mb4'
                        )
                        conn.close()
                        QMessageBox.information(self, "连接成功", "MySQL数据库连接成功！")
                    except Exception as e:
                        QMessageBox.critical(self, "连接失败", f"MySQL数据库连接失败: {str(e)}")
                 
                test_btn.clicked.connect(_test_connection)
                 
                # 确定按钮功能
                def _save_to_mysql_db():
                    try:
                        host = host_input.text()
                        port = int(port_input.text())
                        user = user_input.text()
                        password = pwd_input.text()
                        db = db_input.text()
                        table_name = table_input.text()
                         
                        if not user or not db or not table_name:
                            QMessageBox.warning(self, "输入错误", "用户名、数据库名和表名不能为空")
                            return
                         
                        # 创建SQLAlchemy引擎用于MySQL连接
                        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4")
                         
                        # 连接MySQL数据库
                        conn = engine.connect()
                         
                        # 检查表是否已存在（使用SQLAlchemy Core）
                        from sqlalchemy import inspect
                        inspector = inspect(engine)
                        table_exists = table_name in inspector.get_table_names()
                         
                        # 如果表已存在，询问用户是否覆盖
                        if table_exists:
                            reply = QMessageBox.question(
                                self,
                                "表已存在",
                                f"表 '{table_name}' 已存在，是否覆盖？",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                             
                            if reply == QMessageBox.StandardButton.No:
                                conn.close()
                                mysql_dialog.close()
                                self.status_bar.showMessage("取消保存到MySQL数据库")
                                return
                         
                        # 将数据写入MySQL表
                        df.to_sql(table_name, engine, if_exists='replace', index=False)
                         
                        # 保存连接信息
                        self.mysql_connection_info = (host, port, user, password, db)
                         
                        # 关闭连接
                        conn.close()
                        mysql_dialog.close()
                        dialog.close()
                        self.status_bar.showMessage(f"数据已成功保存到MySQL数据库: {db} 表: {table_name}")
                    except Exception as e:
                        QMessageBox.critical(self, "保存失败", f"保存到MySQL数据库失败: {str(e)}")
                        self.status_bar.showMessage(f"保存到MySQL数据库失败: {str(e)}")
                 
                ok_btn.clicked.connect(_save_to_mysql_db)
                cancel_btn.clicked.connect(mysql_dialog.close)
                 
                mysql_dialog.exec()
            except Exception as e:
                self.status_bar.showMessage(f"保存到MySQL数据库失败: {str(e)}")
                dialog.close()
         
        # 新增MongoDB保存功能
        def save_to_mongo():
            try:
                # 如果之前有MongoDB连接信息，可以直接使用
                if hasattr(self, 'mongo_connection_info') and self.mongo_connection_info:
                    use_last_conn = QMessageBox.question(
                        self,
                        "使用上次连接",
                        "是否使用上次的MongoDB连接信息？",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                     
                    if use_last_conn == QMessageBox.StandardButton.Yes:
                        # 直接使用上次的连接信息
                        host, port, db_name, collection_name = self.mongo_connection_info
                         
                        # 让用户确认或修改集合名
                        collection_name, ok = QInputDialog.getText(
                            self,
                            "输入集合名",
                            "请输入要保存的集合名:",
                            text=collection_name
                        )
                         
                        if ok and collection_name.strip():
                            try:
                                # 连接MongoDB数据库
                                client = MongoClient(host, port)
                                db = client[db_name]
                                collection = db[collection_name]
                                 
                                # 检查集合是否已存在数据
                                collection_exists = collection.count_documents({}) > 0
                                 
                                # 如果集合已存在数据，询问用户是否覆盖
                                if collection_exists:
                                    reply = QMessageBox.question(
                                        self,
                                        "集合已存在数据",
                                        f"集合 '{collection_name}' 已存在数据，是否清空并覆盖？",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                    )
                                     
                                    if reply == QMessageBox.StandardButton.No:
                                        client.close()
                                        self.status_bar.showMessage("取消保存到MongoDB数据库")
                                        dialog.close()
                                        return
                                 
                                # 清空集合（如果选择覆盖）
                                collection.delete_many({})
                                 
                                # 将DataFrame转换为字典列表
                                data_dict = df.to_dict('records')
                                 
                                # 保存数据到MongoDB
                                if data_dict:
                                    collection.insert_many(data_dict)
                                 
                                # 关闭连接
                                client.close()
                                self.status_bar.showMessage(f"数据已成功保存到MongoDB数据库: {db_name} 集合: {collection_name}")
                            except Exception as e:
                                self.status_bar.showMessage(f"保存到MongoDB数据库失败: {str(e)}")
                        dialog.close()
                        return
                 
                # 创建MongoDB连接对话框
                mongo_dialog = QDialog(self)
                mongo_dialog.setWindowTitle("连接MongoDB数据库")
                mongo_dialog.resize(400, 250)
                 
                mongo_layout = QVBoxLayout(mongo_dialog)
                 
                # 主机名/IP地址
                host_layout = QHBoxLayout()
                host_layout.addWidget(QLabel("主机名/IP地址:"))
                host_input = QLineEdit("localhost")
                host_layout.addWidget(host_input)
                mongo_layout.addLayout(host_layout)
                 
                # 端口号
                port_layout = QHBoxLayout()
                port_layout.addWidget(QLabel("端口号:"))
                port_input = QLineEdit("27017")
                port_layout.addWidget(port_input)
                mongo_layout.addLayout(port_layout)
                 
                # 数据库名
                db_layout = QHBoxLayout()
                db_layout.addWidget(QLabel("数据库名:"))
                db_input = QLineEdit("data_analysis")
                db_layout.addWidget(db_input)
                mongo_layout.addLayout(db_layout)
                 
                # 集合名
                collection_layout = QHBoxLayout()
                collection_layout.addWidget(QLabel("集合名:"))
                collection_input = QLineEdit("data_table")
                collection_layout.addWidget(collection_input)
                mongo_layout.addLayout(collection_layout)
                 
                # 按钮布局
                btn_layout = QHBoxLayout()
                 
                # 测试连接按钮
                test_btn = QPushButton("测试连接")
                btn_layout.addWidget(test_btn)
                 
                # 确定/取消按钮
                ok_btn = QPushButton("确定")
                cancel_btn = QPushButton("取消")
                btn_layout.addWidget(ok_btn)
                btn_layout.addWidget(cancel_btn)
                 
                mongo_layout.addLayout(btn_layout)
                 
                # 测试连接功能
                def _test_connection():
                    try:
                        host = host_input.text()
                        port = int(port_input.text())
                        db_name = db_input.text()
                         
                        if not db_name:
                            QMessageBox.warning(self, "输入错误", "数据库名不能为空")
                            return
                         
                        # 连接到MongoDB数据库
                        client = MongoClient(host, port)
                        # 尝试访问数据库以测试连接
                        db = client[db_name]
                        # 列出数据库集合以确认连接正常
                        collections = db.list_collection_names()
                        client.close()
                        QMessageBox.information(self, "连接成功", "MongoDB数据库连接成功！")
                    except Exception as e:
                        QMessageBox.critical(self, "连接失败", f"MongoDB数据库连接失败: {str(e)}")
                 
                test_btn.clicked.connect(_test_connection)
                 
                # 确定按钮功能
                def _save_to_mongo_db():
                    try:
                        host = host_input.text()
                        port = int(port_input.text())
                        db_name = db_input.text()
                        collection_name = collection_input.text()
                         
                        if not db_name or not collection_name:
                            QMessageBox.warning(self, "输入错误", "数据库名和集合名不能为空")
                            return
                         
                        # 连接MongoDB数据库
                        client = MongoClient(host, port)
                        db = client[db_name]
                        collection = db[collection_name]
                         
                        # 检查集合是否已存在数据
                        collection_exists = collection.count_documents({}) > 0
                         
                        # 如果集合已存在数据，询问用户是否覆盖
                        if collection_exists:
                            reply = QMessageBox.question(
                                self,
                                "集合已存在数据",
                                f"集合 '{collection_name}' 已存在数据，是否清空并覆盖？",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                             
                            if reply == QMessageBox.StandardButton.No:
                                client.close()
                                mongo_dialog.close()
                                self.status_bar.showMessage("取消保存到MongoDB数据库")
                                return
                         
                        # 清空集合（如果选择覆盖）
                        collection.delete_many({})
                         
                        # 将DataFrame转换为字典列表
                        data_dict = df.to_dict('records')
                         
                        # 保存数据到MongoDB
                        if data_dict:
                            collection.insert_many(data_dict)
                         
                        # 保存连接信息
                        self.mongo_connection_info = (host, port, db_name, collection_name)
                         
                        # 关闭连接
                        client.close()
                        mongo_dialog.close()
                        dialog.close()
                        self.status_bar.showMessage(f"数据已成功保存到MongoDB数据库: {db_name} 集合: {collection_name}")
                    except Exception as e:
                        QMessageBox.critical(self, "保存失败", f"保存到MongoDB数据库失败: {str(e)}")
                        self.status_bar.showMessage(f"保存到MongoDB数据库失败: {str(e)}")
                 
                ok_btn.clicked.connect(_save_to_mongo_db)
                cancel_btn.clicked.connect(mongo_dialog.close)
                 
                mongo_dialog.exec()
            except Exception as e:
                self.status_bar.showMessage(f"保存到MongoDB数据库失败: {str(e)}")
                dialog.close()
         
        # 连接按钮信号
        csv_btn.clicked.connect(save_to_csv)
        excel_btn.clicked.connect(save_to_excel)
        json_btn.clicked.connect(save_to_json)
        sqlite_btn.clicked.connect(save_to_sqlite)
        mysql_btn.clicked.connect(save_to_mysql)
        mongo_btn.clicked.connect(save_to_mongo)  # 连接MongoDB按钮信号
         
        # 显示对话框
        dialog.exec()
 
 
    #########################
 
 
 
    def _sort_data(self):
        """
        对表格数据进行多列排序
         
        功能: 弹出对话框让用户选择最多3列进行组合排序，支持升序/降序
        """
        from PyQt6.QtWidgets import (QInputDialog, QDialog, QVBoxLayout, 
                                  QLabel, QComboBox, QDialogButtonBox, QHBoxLayout)
         
        # 检查表格是否有数据
        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            self.status_bar.showMessage("表格中没有数据可排序")
            return
             
        # 创建排序对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("多列排序")
        layout = QVBoxLayout()
         
        # 添加最多3个排序条件
        for i in range(3):
            row_layout = QHBoxLayout()
            row_layout.addWidget(QLabel(f"排序条件 {i+1}:"))
             
            # 列选择下拉框
            col_combo = QComboBox()
            col_combo.setObjectName(f"col_combo_{i}")
            col_combo.addItems([self.table_widget.horizontalHeaderItem(j).text() 
                              for j in range(self.table_widget.columnCount())])
            row_layout.addWidget(col_combo)
             
            # 排序方式下拉框
            order_combo = QComboBox()
            order_combo.setObjectName(f"order_combo_{i}")
            order_combo.addItems(["升序", "降序"])
            row_layout.addWidget(order_combo)
             
            layout.addLayout(row_layout)
         
        # 添加确定/取消按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
         
        dialog.setLayout(layout)
         
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 获取排序条件并执行排序
            self.status_bar.showMessage("正在排序数据...")
             
            # 获取当前表格数据
            data = []
            for row in range(self.table_widget.rowCount()):
                row_data = []
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
             
            # 转换为DataFrame以便排序
            headers = [self.table_widget.horizontalHeaderItem(col).text() 
                      for col in range(self.table_widget.columnCount())]
            df = pd.DataFrame(data, columns=headers)
             
            # 获取排序条件
            sort_conditions = []
            for i in range(3):
                col_combo = dialog.findChild(QComboBox, f"col_combo_{i}")
                order_combo = dialog.findChild(QComboBox, f"order_combo_{i}")
                 
                if col_combo and col_combo.currentText():
                    ascending = order_combo.currentText() == "升序"
                    sort_conditions.append((col_combo.currentText(), ascending))
             
            # 执行多列排序
            if sort_conditions:
                df = df.sort_values(
                    by=[col for col, _ in sort_conditions],
                    ascending=[asc for _, asc in sort_conditions]
                )
                 
                # 更新表格数据
                self.table_widget.setRowCount(len(df))
                for row in range(len(df)):
                    for col in range(len(df.columns)):
                        self.table_widget.setItem(row, col, 
                            QTableWidgetItem(str(df.iloc[row, col])))
                 
            self.status_bar.showMessage(f"已按{len(sort_conditions)}列排序完成")
        else:
            self.status_bar.showMessage("排序已取消")
         
 
         
    def _clean_data(self):
        """
        数据清洗功能
         
        功能: 对表格数据进行清洗处理，包括空值处理和数据整理
        参数: 无
        返回值: 无
        """
        from PyQt6.QtWidgets import QInputDialog, QMessageBox  # 输入对话框和消息框组件
         
        # 检查表格是否有数据
        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            self.status_bar.showMessage("表格中没有数据可清洗")
            return
             
        # 弹出对话框让用户选择清洗选项
        options = ["删除空行", "填充空值", "删除重复行", "数据类型转换"]
        option, ok = QInputDialog.getItem(
            self,
            "选择清洗选项",  # 对话框标题
            "请选择要执行的清洗操作:",  # 提示文本
            options,  # 选项列表
            0,  # 默认选中第一项
            False  # 不允许编辑
        )
         
        # 如果用户取消了选择
        if not ok:
            return
             
        # 根据用户选择执行不同的清洗操作
        try:
            if option == "删除空行":
                # 删除所有空行
                rows_to_remove = []
                for row in range(self.table_widget.rowCount()):
                    is_empty = True
                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(row, col)
                        if item and item.text().strip():
                            is_empty = False
                            break
                    if is_empty:
                        rows_to_remove.append(row)
                 
                # 从后往前删除行，避免索引错乱
                for row in sorted(rows_to_remove, reverse=True):
                    self.table_widget.removeRow(row)
                 
                self.status_bar.showMessage(f"已删除 {len(rows_to_remove)} 个空行")
                 
            elif option == "填充空值":
                # 填充空值
                col, ok = QInputDialog.getInt(
                    self,
                    "选择列",
                    "请输入要填充空值的列号(从1开始):",
                    1,  # 默认值
                    1,  # 最小值
                    self.table_widget.columnCount(),  # 最大值
                    1  # 步长
                )
                 
                if not ok:
                    return
                     
                # 获取填充值
                value, ok = QInputDialog.getText(
                    self,
                    "输入填充值",
                    "请输入要填充的值:"
                )
                 
                if not ok:
                    return
                     
                # 填充空值
                col_index = col - 1
                filled_count = 0
                for row in range(self.table_widget.rowCount()):
                    item = self.table_widget.item(row, col_index)
                    if not item or not item.text().strip():
                        self.table_widget.setItem(row, col_index, QTableWidgetItem(value))
                        filled_count += 1
                 
                self.status_bar.showMessage(f"已填充 {filled_count} 个空值")
                 
            elif option == "删除重复行":
                # 删除重复行
                rows_to_remove = []
                seen_rows = set()
                 
                for row in range(self.table_widget.rowCount()):
                    row_data = []
                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(row, col)
                        row_data.append(item.text() if item else "")
                     
                    row_tuple = tuple(row_data)
                    if row_tuple in seen_rows:
                        rows_to_remove.append(row)
                    else:
                        seen_rows.add(row_tuple)
                 
                # 从后往前删除行
                for row in sorted(rows_to_remove, reverse=True):
                    self.table_widget.removeRow(row)
                 
                self.status_bar.showMessage(f"已删除 {len(rows_to_remove)} 个重复行")
                 
            elif option == "数据类型转换":
                # 数据类型转换
                col, ok = QInputDialog.getInt(
                    self,
                    "选择列",
                    "请输入要转换数据类型的列号(从1开始):",
                    1,
                    1,
                    self.table_widget.columnCount(),
                    1
                )
                 
                if not ok:
                    return
                     
                # 选择目标类型
                types = ["整数", "浮点数", "字符串", "布尔值"]
                target_type, ok = QInputDialog.getItem(
                    self,
                    "选择目标类型",
                    "请选择要转换的数据类型:",
                    types,
                    0,
                    False
                )
                 
                if not ok:
                    return
                     
                # 执行转换
                col_index = col - 1
                converted_count = 0
                for row in range(self.table_widget.rowCount()):
                    item = self.table_widget.item(row, col_index)
                    if item and item.text().strip():
                        try:
                            text = item.text()
                            if target_type == "整数":
                                value = int(text)
                            elif target_type == "浮点数":
                                value = float(text)
                            elif target_type == "布尔值":
                                value = True if text.lower() in ["true", "1", "yes"] else False
                            else:  # 字符串
                                value = str(text)
                             
                            self.table_widget.setItem(row, col_index, QTableWidgetItem(str(value)))
                            converted_count += 1
                        except ValueError:
                            pass
                 
                self.status_bar.showMessage(f"已转换 {converted_count} 个值为 {target_type}")
                 
        except Exception as e:
            self.status_bar.showMessage(f"数据清洗失败: {str(e)}")
             
    def _filter_data(self):
        """
        对表格数据进行高级筛选
         
        功能: 弹出对话框让用户设置多条件筛选，支持运算符(=,>,<等)和逻辑组合(AND/OR)
        改进: 支持多条件组合筛选，简化操作流程
        """
        from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                  QComboBox, QLineEdit, QDialogButtonBox, QPushButton,
                                  QScrollArea, QWidget, QGroupBox)
        from PyQt6.QtCore import Qt
         
        # 检查表格是否有数据
        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            self.status_bar.showMessage("表格中没有数据可筛选")
            return
             
        # 创建筛选对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("高级筛选")
        dialog.resize(500, 400)
        layout = QVBoxLayout()
         
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
         
        # 添加条件组
        condition_group = QGroupBox("筛选条件")
        condition_group_layout = QVBoxLayout()
         
        # 初始条件
        condition_widgets = []
         
        def add_condition():
            condition_widget = QWidget()
            condition_layout = QHBoxLayout()
             
            # 列选择下拉框
            col_combo = QComboBox()
            col_combo.addItems([self.table_widget.horizontalHeaderItem(j).text() 
                              for j in range(self.table_widget.columnCount())])
            condition_layout.addWidget(col_combo)
             
            # 运算符下拉框
            operator_combo = QComboBox()
            operator_combo.addItems(["=", ">", "<", "<=", ">=", "!=", "包含", "不包含", "开头为", "结尾为", "为空", "不为空"])
            condition_layout.addWidget(operator_combo)
             
            # 值输入框
            value_edit = QLineEdit()
            condition_layout.addWidget(value_edit)
             
            # 删除按钮
            delete_btn = QPushButton("删除")
            delete_btn.clicked.connect(lambda: remove_condition(condition_widget))
            condition_layout.addWidget(delete_btn)
             
            condition_widget.setLayout(condition_layout)
            condition_group_layout.addWidget(condition_widget)
            condition_widgets.append({
                "widget": condition_widget,
                "col_combo": col_combo,
                "operator_combo": operator_combo,
                "value_edit": value_edit
            })
         
        def remove_condition(widget):
            condition_group_layout.removeWidget(widget)
            widget.deleteLater()
            condition_widgets[:] = [cw for cw in condition_widgets if cw["widget"] != widget]
         
        # 添加初始条件
        add_condition()
         
        # 添加条件按钮
        add_btn = QPushButton("添加条件")
        add_btn.clicked.connect(add_condition)
        condition_group_layout.addWidget(add_btn)
         
        condition_group.setLayout(condition_group_layout)
        scroll_layout.addWidget(condition_group)
         
        # 添加逻辑组合选项
        logic_group = QGroupBox("逻辑组合")
        logic_layout = QVBoxLayout()
        logic_combo = QComboBox()
        logic_combo.addItems(["AND", "OR"])
        logic_layout.addWidget(logic_combo)
        logic_group.setLayout(logic_layout)
        scroll_layout.addWidget(logic_group)
         
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
         
        # 添加确定/取消按钮
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
         
        dialog.setLayout(layout)
         
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 获取筛选条件并执行筛选
            self.status_bar.showMessage("正在筛选数据...")
             
            # 获取当前表格数据
            data = []
            for row in range(self.table_widget.rowCount()):
                row_data = []
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
             
            # 转换为DataFrame以便筛选
            headers = [self.table_widget.horizontalHeaderItem(col).text() 
                      for col in range(self.table_widget.columnCount())]
            df = pd.DataFrame(data, columns=headers)
             
            # 获取筛选条件
            masks = []
            logic = logic_combo.currentText()
             
            for condition in condition_widgets:
                col_name = condition["col_combo"].currentText()
                operator = condition["operator_combo"].currentText()
                value = condition["value_edit"].text()
                 
                # 构建筛选条件
                if operator == "=":
                    mask = df[col_name] == value
                elif operator == ">":
                    mask = df[col_name] > value
                elif operator == "<":
                    mask = df[col_name] < value
                elif operator == "<=":
                    mask = df[col_name] <= value
                elif operator == ">=":
                    mask = df[col_name] >= value
                elif operator == "!=":
                    mask = df[col_name] != value
                elif operator == "包含":
                    mask = df[col_name].str.contains(value, na=False)
                elif operator == "不包含":
                    mask = ~df[col_name].str.contains(value, na=False)
                elif operator == "开头为":
                    mask = df[col_name].str.startswith(value, na=False)
                elif operator == "结尾为":
                    mask = df[col_name].str.endswith(value, na=False)
                elif operator == "为空":
                    mask = df[col_name].isna() | (df[col_name] == "")
                elif operator == "不为空":
                    mask = ~df[col_name].isna() & (df[col_name] != "")
                 
                masks.append(mask)
             
            # 组合筛选条件
            if masks:
                combined_mask = masks[0]
                for mask in masks[1:]:
                    if logic == "AND":
                        combined_mask &= mask
                    else:
                        combined_mask |= mask
                 
                filtered_df = df[combined_mask]
            else:
                filtered_df = df.copy()
             
            # 更新表格显示
            self.table_widget.setRowCount(len(filtered_df))
            for row in range(len(filtered_df)):
                for col in range(len(filtered_df.columns)):
                    self.table_widget.setItem(row, col, 
                        QTableWidgetItem(str(filtered_df.iloc[row, col])))
             
            self.status_bar.showMessage(
                f"已筛选出{len(filtered_df)}条记录 (共{len(df)}条)" +
                f" | 使用{len(condition_widgets)}个条件{logic}组合"
            )
        else:
            self.status_bar.showMessage("筛选已取消")
         
 
         
    def _data_cleaning(self):
        """
        数据清洗功能
         
        功能: 对表格数据进行清洗处理，包括空值处理和数据整理
        参数: 无
        返回值: 无
        """
        from PyQt6.QtWidgets import QInputDialog  # 输入对话框组件
         
        # 检查表格是否有数据
        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            self.status_bar.showMessage("表格中没有数据可清洗")
            return
             
        # 获取所有列名作为选项
        columns = []
        for col in range(self.table_widget.columnCount()):
            header = self.table_widget.horizontalHeaderItem(col)
            columns.append(header.text() if header else f"Column{col+1}")
             
        # 弹出对话框让用户选择清洗列
        column, ok = QInputDialog.getItem(
            self,
            "选择清洗列",  # 对话框标题
            "请选择要清洗的列:",  # 提示文本
            columns,  # 选项列表
            0,  # 默认选中第一项
            False  # 不允许编辑
        )
         
        # 如果用户取消了选择
        if not ok:
            return
             
        # 获取列索引
        col_index = columns.index(column)
         
        # 弹出对话框让用户选择清洗方式
        methods = ["删除空值行", "填充默认值", "删除重复行"]
        method, ok = QInputDialog.getItem(
            self,
            "选择清洗方式",
            "请选择清洗方式:",
            methods,
            0,
            False
        )
         
        # 如果用户取消了选择
        if not ok:
            return
             
        # 执行数据清洗
        try:
            if method == "删除空值行":
                # 删除空值行逻辑
                rows_to_keep = []
                for row in range(self.table_widget.rowCount()):
                    item = self.table_widget.item(row, col_index)
                    if item and item.text().strip():  # 检查单元格是否有值
                        rows_to_keep.append(row)
                 
                # 创建新表格数据
                new_data = []
                for row in rows_to_keep:
                    row_data = []
                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(row, col)
                        row_data.append(item.text() if item else "")
                    new_data.append(row_data)
                 
                # 更新表格
                self._update_table_with_data(new_data)
                 
                self.status_bar.showMessage(f"已删除{self.table_widget.rowCount() - len(rows_to_keep)}条空值行")
                 
            elif method == "填充默认值":
                # 填充默认值逻辑
                default_value, ok = QInputDialog.getText(
                    self,
                    "输入默认值",
                    f"请输入{column}列的默认值:"
                )
                 
                if ok:
                    for row in range(self.table_widget.rowCount()):
                        item = self.table_widget.item(row, col_index)
                        if not item or not item.text().strip():
                            self.table_widget.setItem(row, col_index, QTableWidgetItem(default_value))
                     
                    self.status_bar.showMessage(f"已将{column}列的空值填充为: {default_value}")
                 
            elif method == "删除重复行":
                # 删除重复行逻辑
                unique_values = set()
                rows_to_keep = []
                 
                for row in range(self.table_widget.rowCount()):
                    item = self.table_widget.item(row, col_index)
                    value = item.text() if item else ""
                    if value not in unique_values:
                        unique_values.add(value)
                        rows_to_keep.append(row)
                 
                # 创建新表格数据
                new_data = []
                for row in rows_to_keep:
                    row_data = []
                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(row, col)
                        row_data.append(item.text() if item else "")
                    new_data.append(row_data)
                 
                # 更新表格
                self._update_table_with_data(new_data)
                 
                self.status_bar.showMessage(f"已删除{self.table_widget.rowCount() - len(rows_to_keep)}条重复行")
                 
        except Exception as e:
            self.status_bar.showMessage(f"数据清洗失败: {str(e)}")
             
    def _update_table_with_data(self, data):
        """
        用新数据更新表格
         
        参数:
            data: list - 二维列表，包含表格数据
        返回值: 无
        """
        # 清空表格内容
        self.table_widget.clearContents()
         
        # 设置新行数
        self.table_widget.setRowCount(len(data))
         
        # 填充新数据
        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QTableWidgetItem(data[row][col])
                self.table_widget.setItem(row, col, item)
                 
    def _visualize_data(self):
        """
        数据可视化功能
         
        功能: 对表格数据进行可视化展示，支持多种图表类型
        参数: 无
        返回值: 无
        """
        from PyQt6.QtWidgets import QInputDialog, QMessageBox  # 输入对话框和消息框组件
         
        # 检查表格是否有数据
        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            self.status_bar.showMessage("表格中没有数据可可视化")
            return
             
        # 获取所有列名作为选项
        columns = []
        for col in range(self.table_widget.columnCount()):
            header = self.table_widget.horizontalHeaderItem(col)
            columns.append(header.text() if header else f"Column{col+1}")
             
        # 弹出对话框让用户选择可视化列
        column, ok = QInputDialog.getItem(
            self,
            "选择可视化列",  # 对话框标题
            "请选择要可视化的列:",  # 提示文本
            columns,  # 选项列表
            0,  # 默认选中第一项
            False  # 不允许编辑
        )
         
        # 如果用户取消了选择
        if not ok:
            return
             
        # 获取列索引
        col_index = columns.index(column)
         
        # 弹出对话框让用户选择图表类型
        chart_types = ["柱状图", "折线图", "饼图", "箱线图", "散点图"]
        chart_type, ok = QInputDialog.getItem(
            self,
            "选择图表类型",
            "请选择图表类型:",
            chart_types,
            0,
            False
        )
         
        # 如果用户取消了选择
        if not ok:
            return
             
        # 收集列数据
        numeric_data = []
        labels = []
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, col_index)
            if item and item.text().strip():  # 只处理有值的单元格
                try:
                    # 尝试转换为数值
                    value = float(item.text())
                    numeric_data.append(value)
                    labels.append(str(row+1))  # 使用行号作为标签
                except ValueError:
                    # 非数值数据跳过
                    pass
         
        # 如果没有有效数据
        if not numeric_data:
            self.status_bar.showMessage(f"{column}列没有可可视化的数值数据")
            return
             
        # 执行可视化
        try:
             # 设置matplotlib支持中文显示
            plt.rcParams["font.family"] = ["SimHei", "SimSun"]
            plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
                 
            plt.figure(figsize=(8, 6))  # 设置图表大小
             
            if chart_type == "柱状图":
                # 创建柱状图
                plt.bar(labels, numeric_data)
                plt.title(f"{column}列柱状图")  # 设置标题
                plt.xlabel("行号")  # X轴标签
                plt.ylabel("数值")  # Y轴标签
                 
            elif chart_type == "折线图":
                # 创建折线图
                plt.plot(labels, numeric_data, marker='o')
                plt.title(f"{column}列折线图")
                plt.xlabel("行号")
                plt.ylabel("数值")
                 
            elif chart_type == "饼图":
                # 创建饼图
                plt.pie(numeric_data, labels=labels, autopct='%1.1f%%')
                plt.title(f"{column}列饼图")
                 
            elif chart_type == "箱线图":
                # 创建箱线图
                sns.boxplot(data=numeric_data)
                plt.title(f"{column}列箱线图")
                plt.ylabel("数值")
                 
            elif chart_type == "散点图":
                # 创建散点图
                plt.scatter(range(len(numeric_data)), numeric_data)
                plt.title(f"{column}列散点图")
                plt.xlabel("索引")
                plt.ylabel("数值")
                 
            plt.tight_layout()  # 自动调整子图参数
            plt.show()  # 显示图表
             
            self.status_bar.showMessage(f"已生成{column}列的{chart_type}")
             
        except Exception as e:
            self.status_bar.showMessage(f"数据可视化失败: {str(e)}")
 
             
    def _data_analysis(self):
        """
        数据分析功能
         
        功能: 对表格数据进行基础统计分析
        参数: 无
        返回值: 无
        """
        from PyQt6.QtWidgets import QMessageBox  # 消息框组件
        import numpy as np  # 数值计算库
         
        # 检查表格是否有数据
        if self.table_widget.rowCount() == 0 or self.table_widget.columnCount() == 0:
            self.status_bar.showMessage("表格中没有数据可分析")
            return
             
        # 基础统计分析
        try:
            stats = []
            for col in range(self.table_widget.columnCount()):
                data = []
                for row in range(self.table_widget.rowCount()):
                    item = self.table_widget.item(row, col)
                    if item and item.text().strip():  # 只处理有值的单元格
                        try:
                            value = float(item.text())
                            data.append(value)
                        except ValueError:
                            pass
                 
                if data:
                    header = self.table_widget.horizontalHeaderItem(col)
                    col_name = header.text() if header else f"Column{col+1}"
                     
                    # 计算统计量
                    stats.append(f"{col_name}列统计结果:")
                    stats.append(f"-----------------")
                    stats.append(f"数据个数: {len(data)}")
                    stats.append(f"平均值: {np.mean(data):.2f}")
                    stats.append(f"标准差: {np.std(data):.2f}")
                    stats.append(f"最小值: {min(data):.2f}")
                    stats.append(f"25%分位数: {np.percentile(data, 25):.2f}")
                    stats.append(f"中位数: {np.median(data):.2f}")
                    stats.append(f"75%分位数: {np.percentile(data, 75):.2f}")
                    stats.append(f"最大值: {max(data):.2f}")
                    stats.append("")
             
            # 显示统计结果
            if stats:
                QMessageBox.information(
                    self,
                    "基础统计结果",
                    "\n".join(stats)
                )
                self.status_bar.showMessage("已完成基础统计分析")
            else:
                self.status_bar.showMessage("没有找到可分析的数值数据")
                 
        except Exception as e:
            self.status_bar.showMessage(f"数据分析失败: {str(e)}")
         
    # except Exception as e:
    #     self.status_bar.showMessage(f"数据分析失败: {str(e)}")
     
    def _show_about(self):
        """显示关于信息"""
        self.status_bar.showMessage("关于功能待实现")
 
 
if __name__ == "__main__":
    """程序入口"""
    app = QApplication(sys.argv)
     
    # 创建主窗口
    window = DataAnalysisPlatform()
    window.show()
     
    # 运行应用
    sys.exit(app.exec())