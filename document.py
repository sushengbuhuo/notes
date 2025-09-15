import os
import shutil
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime, timedelta
import logging
from pathlib import Path
import threading
 
class DocumentOrganizer:
    def __init__(self):
        # 文件类型映射
        self.file_type_mapping = {
            '文档': ['doc', 'docx', 'odt', 'rtf'],
            '表格': ['xls', 'xlsx', 'csv', 'ods'],
            '演示': ['ppt', 'pptx', 'odp'],
            'PDF': ['pdf'],
            '图片': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
            '文本': ['txt', 'md', 'log'],
            '压缩包': ['zip', 'rar', '7z', 'tar', 'gz'],
            '音频': ['mp3', 'wav', 'flac', 'aac'],
            '视频': ['mp4', 'avi', 'mov', 'mkv'],
            '自定义': []  # 用于存储用户自定义的文件后缀
        }
         
        # 反向映射：扩展名到文件类型
        self.extension_to_type = {}
        for category, exts in self.file_type_mapping.items():
            for ext in exts:
                self.extension_to_type[ext.lower()] = category
 
    def get_file_age_days(self, file_path):
        """获取文件创建时间距今的天数（修复版）"""
        try:
            # 尝试获取创建时间
            if os.name == 'nt':  # Windows系统
                try:
                    create_time = os.path.getctime(file_path)
                except:
                    # 如果获取创建时间失败，使用修改时间作为备选
                    create_time = os.path.getmtime(file_path)
            else:  # Unix/Linux系统
                # Unix系统没有创建时间的统一接口，使用修改时间
                create_time = os.path.getmtime(file_path)
                 
            # 转换为datetime对象
            create_date = datetime.fromtimestamp(create_time)
            now = datetime.now()
             
            # 计算天数差
            days_diff = (now - create_date).days
            return max(0, days_diff)  # 确保不会返回负数
        except Exception as e:
            logging.warning(f"获取文件 {file_path} 时间信息失败: {str(e)}，将按最旧文件处理")
            return float('inf')  # 返回无穷大，确保会被筛选出来
 
    def filter_files(self, source_dir, days, file_types, file_name_condition=None, file_name_input=None, progress_callback=None):
        """筛选符合条件的文件（改为按天数筛选）"""
        filtered_files = []
         
        if not os.path.exists(source_dir):
            logging.error(f"源路径不存在: {source_dir}")
            return []
             
        # 获取所有文件总数用于进度计算
        total_files = 0
        for root, dirs, files in os.walk(source_dir):
            total_files += len(files)
             
        processed_files = 0
             
        # 递归遍历目录
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                processed_files += 1
                 
                # 每处理100个文件更新一次进度
                if processed_files % 100 == 0 and progress_callback:
                    progress = min(int((processed_files / total_files) * 100), 100)
                    progress_callback(progress, f"正在扫描: {file}")
                 
                # 检查文件年龄（按天数）
                file_age_days = self.get_file_age_days(file_path)
                if file_age_days < days:
                    continue
                     
                # 检查文件类型
                ext = file.split('.')[-1].lower() if '.' in file and len(file.split('.')) > 1 else ''
                valid_ext = False
                for ft in file_types:
                    if ext in ft.lower().split(','):
                        valid_ext = True
                        break
                if not valid_ext:
                    continue
                     
                # 检查文件名条件（如果提供）
                if file_name_input and file_name_condition:
                    file_name = os.path.splitext(file)[0]
                    if file_name_condition == 'contains' and file_name_input not in file_name:
                        continue
                    if file_name_condition == 'startsWith' and not file_name.startswith(file_name_input):
                        continue
                    if file_name_condition == 'endsWith' and not file_name.endswith(file_name_input):
                        continue
                         
                # 获取文件创建日期
                try:
                    if os.name == 'nt':
                        create_time = os.path.getctime(file_path)
                    else:
                        create_time = os.path.getmtime(file_path)
                    create_date = datetime.fromtimestamp(create_time)
                except:
                    create_date = datetime.now() - timedelta(days=file_age_days)
                     
                filtered_files.append({
                    'path': file_path,
                    'name': file,
                    'extension': ext,
                    'create_date': create_date,
                    'age_days': file_age_days
                })
                 
                # 每找到100个文件输出一次进度
                if len(filtered_files) % 100 == 0:
                    logging.info(f"已找到 {len(filtered_files)} 个符合条件的文件...")
         
        if progress_callback:
            progress_callback(100, "扫描完成")
             
        logging.info(f"筛选完成，共找到 {len(filtered_files)} 个符合条件的文件")
        return filtered_files
 
    def organize_files(self, files, dest_dir, move=False, overwrite=False, 
                      create_year_folders=True, create_month_folders=True, 
                      progress_callback=None):
        """整理文件到目标目录"""
        results = []
         
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
                logging.info(f"创建目标目录: {dest_dir}")
            except Exception as e:
                logging.error(f"创建目标目录失败: {str(e)}")
                return []
         
        total_files = len(files)
        for i, file_info in enumerate(files, 1):
            try:
                # 更新进度
                if progress_callback:
                    progress = min(int((i / total_files) * 100), 100)
                    progress_callback(progress, f"正在处理: {file_info['name']}")
                 
                # 构建目标路径
                file_path = file_info['path']
                file_name = file_info['name']
                create_date = file_info['create_date']
                 
                # 构建日期目录
                date_path = []
                if create_year_folders:
                    date_path.append(str(create_date.year))
                if create_month_folders:
                    date_path.append(f"{create_date.month:02d}")
                 
                # 获取文件类型目录
                ext = file_info['extension']
                type_dir = self.extension_to_type.get(ext, '其他')
                 
                # 完整目标目录
                target_dir = os.path.join(dest_dir, type_dir, *date_path)
                 
                # 创建目标目录
                Path(target_dir).mkdir(parents=True, exist_ok=True)
                 
                # 目标文件路径
                target_path = os.path.join(target_dir, file_name)
                 
                # 处理同名文件
                if os.path.exists(target_path) and not overwrite:
                    # 添加时间戳避免重名
                    name, ext = os.path.splitext(file_name)
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    target_path = os.path.join(target_dir, f"{name}_{timestamp}{ext}")
                    logging.warning(f"文件 {file_name} 已存在，将重命名为 {os.path.basename(target_path)}")
                 
                # 复制或移动文件
                if move:
                    shutil.move(file_path, target_path)
                    action = "移动"
                else:
                    shutil.copy2(file_path, target_path)
                    action = "复制"
                 
                logging.info(f"({i}/{total_files}) {action} 文件: {file_path} -> {target_path}")
                 
                results.append({
                    'original_path': file_path,
                    'target_path': target_path,
                    'name': file_name,
                    'success': True,
                    'error': ''
                })
                 
            except Exception as e:
                error_msg = f"处理文件 {file_info['name']} 失败: {str(e)}"
                logging.error(error_msg)
                results.append({
                    'original_path': file_path,
                    'target_path': '',
                    'name': file_name,
                    'success': False,
                    'error': str(e)
                })
         
        if progress_callback:
            progress_callback(100, "整理完成")
         
        return results
 
    def run(self, source_dir, dest_dir, days, file_types, 
            file_name_condition=None, file_name_input=None,
            move=False, overwrite=False, 
            create_year_folders=True, create_month_folders=True,
            progress_callback=None, status_callback=None):
        """运行整理流程"""
        if status_callback:
            status_callback("开始文件整理流程...")
        start_time = time.time()
        logging.info("开始文件整理流程...")
         
        # 筛选文件
        if status_callback:
            status_callback("开始筛选符合条件的文件...")
        logging.info("开始筛选符合条件的文件...")
         
        filtered_files = self.filter_files(
            source_dir, days, file_types,
            file_name_condition, file_name_input,
            progress_callback=lambda p, s: progress_callback(p, s) if progress_callback else None
        )
         
        if not filtered_files:
            if status_callback:
                status_callback("没有找到符合条件的文件，整理结束")
            logging.info("没有找到符合条件的文件，整理结束")
            return []
         
        # 整理文件
        if status_callback:
            status_callback("开始整理文件...")
        logging.info("开始整理文件...")
         
        results = self.organize_files(
            filtered_files, dest_dir, move, overwrite,
            create_year_folders, create_month_folders,
            progress_callback=lambda p, s: progress_callback(p, s) if progress_callback else None
        )
         
        # 统计结果
        success_count = sum(1 for r in results if r['success'])
        fail_count = len(results) - success_count
        elapsed_time = time.time() - start_time
         
        final_msg = (f"整理完成！共处理 {len(results)} 个文件，"
                    f"成功 {success_count} 个，失败 {fail_count} 个，"
                    f"总耗时: {elapsed_time:.2f} 秒")
         
        if status_callback:
            status_callback(final_msg)
        logging.info(final_msg)
         
        return results
 
 
class DocumentOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文档整理助手")
        self.root.geometry("850x700")
        self.root.minsize(750, 600)
         
        # 设置中文字体
        self.setup_fonts()
         
        # 创建整理器实例
        self.organizer = DocumentOrganizer()
         
        # 结果存储
        self.results = []
         
        # 创建界面
        self.create_widgets()
         
        # 配置日志
        self.setup_logging()
         
        # 防止多线程同时运行
        self.is_running = False
 
    def setup_fonts(self):
        """设置支持中文的字体"""
        default_font = ('SimHei', 10)
        self.root.option_add("*Font", default_font)
 
    def setup_logging(self):
        """配置日志系统"""
        # 创建日志文本框
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
         
        # 添加自定义日志处理器
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)
                self.text_widget = text_widget
                 
            def emit(self, record):
                msg = self.format(record) + "\n"
                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.insert(tk.END, msg)
                self.text_widget.see(tk.END)
                self.text_widget.config(state=tk.DISABLED)
         
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('organizer.log'),
                TextHandler(self.log_text)
            ]
        )
 
    def create_widgets(self):
        """创建GUI组件"""
        # 创建主框架
        main_notebook = ttk.Notebook(self.root)
        main_notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
         
        # 创建设置标签页
        settings_frame = ttk.Frame(main_notebook)
        main_notebook.add(settings_frame, text="设置")
         
        # 创建结果标签页
        results_frame = ttk.Frame(main_notebook)
        main_notebook.add(results_frame, text="结果")
         
        # 创建日志标签页
        self.log_frame = ttk.Frame(main_notebook)
        main_notebook.add(self.log_frame, text="日志")
         
        # 设置标签页内容
        self.create_settings_tab(settings_frame)
         
        # 结果标签页内容
        self.create_results_tab(results_frame)
         
        # 绑定标签页切换事件
        main_notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
 
    def create_settings_tab(self, parent):
        """创建设置标签页内容"""
        # 创建一个主画布和滚动条
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
         
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
         
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
         
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
         
        # 源目录选择
        ttk.Label(scrollable_frame, text="源目录:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.source_dir_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.source_dir_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(scrollable_frame, text="浏览...", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
         
        # 目标目录选择
        ttk.Label(scrollable_frame, text="目标目录:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.dest_dir_var = tk.StringVar()
        ttk.Entry(scrollable_frame, textvariable=self.dest_dir_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(scrollable_frame, text="浏览...", command=self.browse_dest).grid(row=1, column=2, padx=5, pady=5)
         
        # 时间条件（改为按天数，并增加自定义选项）
        ttk.Label(scrollable_frame, text="时间条件:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.time_condition_var = tk.StringVar(value="90")  # 90天约等于3个月
        time_frame = ttk.Frame(scrollable_frame)
        time_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
         
        # 预设时间选项（转换为天数）
        ttk.Radiobutton(time_frame, text="7天前", variable=self.time_condition_var, value="7").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(time_frame, text="30天前", variable=self.time_condition_var, value="30").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(time_frame, text="90天前", variable=self.time_condition_var, value="90").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(time_frame, text="自定义", variable=self.time_condition_var, value="custom").pack(side=tk.LEFT, padx=5)
         
        # 自定义天数输入框
        self.custom_days_var = tk.IntVar(value=180)
        self.custom_days_frame = ttk.Frame(scrollable_frame)
        self.custom_days_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(self.custom_days_frame, text="自定义天数:").pack(side=tk.LEFT)
        ttk.Entry(self.custom_days_frame, textvariable=self.custom_days_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(self.custom_days_frame, text="天前").pack(side=tk.LEFT)
        self.custom_days_frame.grid_remove()  # 初始隐藏
         
        # 绑定时间条件变化事件
        self.time_condition_var.trace_add("write", self.on_time_condition_changed)
         
        # 文件类型选择
        ttk.Label(scrollable_frame, text="文件类型:").grid(row=4, column=0, sticky=tk.NW, padx=5, pady=5)
         
        file_types_frame = ttk.LabelFrame(scrollable_frame, text="选择要整理的文件类型")
        file_types_frame.grid(row=4, column=1, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
         
        self.file_type_vars = {}
        row, col = 0, 0
        for file_type in self.organizer.file_type_mapping.keys():
            var = tk.BooleanVar(value=(file_type != '自定义'))  # 自定义类型默认不选
            self.file_type_vars[file_type] = var
            ttk.Checkbutton(file_types_frame, text=file_type, variable=var,
                           command=lambda ft=file_type: self.on_file_type_changed(ft)).grid(
                row=row, column=col, sticky=tk.W, padx=10, pady=2)
            col += 1
            if col > 1:  # 每行显示2个选项
                col = 0
                row += 1
         
        # 自定义文件后缀输入框
        self.custom_extensions_var = tk.StringVar()
        self.custom_extensions_frame = ttk.Frame(file_types_frame)
        self.custom_extensions_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
        ttk.Label(self.custom_extensions_frame, text="自定义后缀（用逗号分隔，如: json,xml）:").pack(side=tk.LEFT)
        ttk.Entry(self.custom_extensions_frame, textvariable=self.custom_extensions_var, width=30).pack(side=tk.LEFT, padx=5)
        self.custom_extensions_frame.grid_remove()  # 初始隐藏
         
        # 文件名筛选（可选）
        name_filter_frame = ttk.LabelFrame(scrollable_frame, text="文件名筛选（可选）")
        name_filter_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
         
        self.name_condition_var = tk.StringVar(value="contains")
        ttk.Radiobutton(name_filter_frame, text="包含", variable=self.name_condition_var, value="contains").grid(
            row=0, column=0, padx=10, pady=5)
        ttk.Radiobutton(name_filter_frame, text="开头为", variable=self.name_condition_var, value="startsWith").grid(
            row=0, column=1, padx=10, pady=5)
        ttk.Radiobutton(name_filter_frame, text="结尾为", variable=self.name_condition_var, value="endsWith").grid(
            row=0, column=2, padx=10, pady=5)
         
        ttk.Label(name_filter_frame, text="字符:").grid(row=0, column=3, padx=10, pady=5)
        self.name_input_var = tk.StringVar()
        ttk.Entry(name_filter_frame, textvariable=self.name_input_var, width=20).grid(
            row=0, column=4, padx=5, pady=5)
         
        # 高级选项
        advanced_frame = ttk.LabelFrame(scrollable_frame, text="高级选项")
        advanced_frame.grid(row=6, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
         
        self.move_files_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(advanced_frame, text="移动文件（默认是复制）", variable=self.move_files_var).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=2)
         
        self.overwrite_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="覆盖已存在的文件", variable=self.overwrite_var).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=2)
         
        self.create_year_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="按年份创建文件夹", variable=self.create_year_var).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=2)
         
        self.create_month_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="按月份创建文件夹", variable=self.create_month_var).grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=2)
         
        # 进度条
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(scrollable_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=7, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=10)
         
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(scrollable_frame, textvariable=self.status_var).grid(row=7, column=2, sticky=tk.W, padx=5, pady=10)
         
        # 开始按钮
        self.start_button = ttk.Button(scrollable_frame, text="开始整理", command=self.start_organizing)
        self.start_button.grid(row=8, column=0, columnspan=3, pady=20)
 
    def on_time_condition_changed(self, *args):
        """时间条件变化时显示/隐藏自定义天数输入框"""
        if self.time_condition_var.get() == "custom":
            self.custom_days_frame.grid()
        else:
            self.custom_days_frame.grid_remove()
     
    def on_file_type_changed(self, file_type):
        """文件类型变化时显示/隐藏自定义后缀输入框"""
        if file_type == "自定义":
            if self.file_type_vars[file_type].get():
                self.custom_extensions_frame.grid()
            else:
                self.custom_extensions_frame.grid_remove()
 
    def create_results_tab(self, parent):
        """创建结果标签页内容"""
        # 创建结果表格
        columns = ("文件名", "原路径", "目标路径", "状态", "天数")
        self.results_tree = ttk.Treeview(parent, columns=columns, show="headings")
         
        # 设置列标题
        for col in columns:
            self.results_tree.heading(col, text=col)
            width = 100 if col in ["状态", "天数"] else 250
            self.results_tree.column(col, width=width, anchor=tk.W)
         
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(parent, orient="vertical", command=self.results_tree.yview)
        scrollbar_x = ttk.Scrollbar(parent, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
         
        # 布局
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.results_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
         
        # 添加筛选按钮
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
         
        ttk.Button(filter_frame, text="全部", command=lambda: self.filter_results("all")).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="成功", command=lambda: self.filter_results("success")).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="失败", command=lambda: self.filter_results("failed")).pack(side=tk.LEFT, padx=5)
         
        # 结果统计
        self.results_stats = tk.StringVar(value="等待整理完成...")
        ttk.Label(filter_frame, textvariable=self.results_stats).pack(side=tk.RIGHT, padx=5)
 
    def browse_source(self):
        """浏览选择源目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir_var.set(directory)
 
    def browse_dest(self):
        """浏览选择目标目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.dest_dir_var.set(directory)
 
    def start_organizing(self):
        """开始整理文件（在新线程中运行）"""
        # 验证输入
        source_dir = self.source_dir_var.get()
        dest_dir = self.dest_dir_var.get()
         
        if not source_dir:
            messagebox.showerror("错误", "请选择源目录")
            return
             
        if not dest_dir:
            messagebox.showerror("错误", "请选择目标目录")
            return
             
        if source_dir == dest_dir:
            messagebox.showerror("错误", "源目录和目标目录不能相同")
            return
         
        # 获取时间条件
        try:
            if self.time_condition_var.get() == "custom":
                days = self.custom_days_var.get()
            else:
                days = int(self.time_condition_var.get())
             
            if days <= 0:
                raise ValueError("天数必须大于0")
        except ValueError as e:
            messagebox.showerror("错误", f"无效的时间设置: {str(e)}")
            return
         
        # 处理自定义文件类型
        custom_exts = []
        if self.file_type_vars.get('自定义', tk.BooleanVar(value=False)).get():
            ext_text = self.custom_extensions_var.get().strip()
            if ext_text:
                # 处理输入的自定义后缀，去除空格并转换为小写
                custom_exts = [ext.strip().lower() for ext in ext_text.split(',') if ext.strip()]
                if not custom_exts:
                    messagebox.showerror("错误", "请输入有效的自定义文件后缀")
                    return
                # 更新整理器中的自定义类型
                self.organizer.file_type_mapping['自定义'] = custom_exts
                # 更新反向映射
                for ext in custom_exts:
                    self.organizer.extension_to_type[ext] = '自定义'
            else:
                messagebox.showerror("错误", "请输入自定义文件后缀或取消选择自定义类型")
                return
         
        # 获取选中的文件类型
        selected_types = []
        for file_type, var in self.file_type_vars.items():
            if var.get():
                exts = self.organizer.file_type_mapping[file_type]
                selected_types.append(",".join(exts))
         
        if not selected_types:
            messagebox.showerror("错误", "请至少选择一种文件类型")
            return
         
        # 禁用开始按钮
        self.start_button.config(state=tk.DISABLED)
        self.is_running = True
         
        # 在新线程中执行整理操作，避免界面冻结
        threading.Thread(target=self.run_organizer, args=(
            source_dir, dest_dir, days, selected_types,
            self.name_condition_var.get(), self.name_input_var.get().strip(),
            self.move_files_var.get(), self.overwrite_var.get(),
            self.create_year_var.get(), self.create_month_var.get()
        ), daemon=True).start()
 
    def run_organizer(self, *args):
        """运行整理器（在后台线程中）"""
        try:
            # 调用整理器
            self.results = self.organizer.run(
                *args,
                progress_callback=self.update_progress,
                status_callback=self.update_status
            )
             
            # 更新结果表格
            self.root.after(0, self.update_results_table)
             
        except Exception as e:
            logging.error(f"整理过程出错: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"整理过程出错: {str(e)}"))
        finally:
            # 恢复界面状态
            self.is_running = False
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
 
    def update_progress(self, progress, status):
        """更新进度条（在主线程中）"""
        self.root.after(0, lambda: self.progress_var.set(progress))
        self.root.after(0, lambda: self.status_var.set(status))
 
    def update_status(self, status):
        """更新状态文本（在主线程中）"""
        self.root.after(0, lambda: self.status_var.set(status))
 
    def update_results_table(self):
        """更新结果表格"""
        # 清空现有内容
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
         
        # 添加新结果
        for result in self.results:
            # 查找对应的文件年龄（天数）
            age_days = "未知"
            for file_info in self.organizer.filtered_files:  # 需要在organizer中添加filtered_files属性存储
                if file_info['path'] == result['original_path']:
                    age_days = file_info['age_days']
                    break
                     
            status = "成功" if result['success'] else f"失败: {result['error']}"
            self.results_tree.insert("", tk.END, values=(
                result['name'],
                result['original_path'],
                result['target_path'],
                status,
                age_days
            ))
         
        # 更新统计信息
        if self.results:
            success_count = sum(1 for r in self.results if r['success'])
            fail_count = len(self.results) - success_count
            self.results_stats.set(f"共 {len(self.results)} 个文件，成功 {success_count} 个，失败 {fail_count} 个")
        else:
            self.results_stats.set("没有整理任何文件")
 
    def filter_results(self, filter_type):
        """筛选结果表格中的内容"""
        # 清空现有内容
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
         
        # 添加符合条件的结果
        for result in self.results:
            if (filter_type == "all" or
                (filter_type == "success" and result['success']) or
                (filter_type == "failed" and not result['success'])):
                 
                # 查找对应的文件年龄（天数）
                age_days = "未知"
                for file_info in getattr(self.organizer, 'filtered_files', []):
                    if file_info['path'] == result['original_path']:
                        age_days = file_info['age_days']
                        break
                 
                status = "成功" if result['success'] else f"失败: {result['error']}"
                self.results_tree.insert("", tk.END, values=(
                    result['name'],
                    result['original_path'],
                    result['target_path'],
                    status,
                    age_days
                ))
 
    def on_tab_changed(self, event):
        """处理标签页切换事件"""
        notebook = event.widget
        current_tab = notebook.select()
        tab_text = notebook.tab(current_tab, "text")
         
        # 如果切换到结果标签页且有结果，更新表格
        if tab_text == "结果" and self.results:
            self.update_results_table()
 
 
if __name__ == "__main__":
    # 在organizer类中添加filtered_files属性
    DocumentOrganizer.filtered_files = []
     
    root = tk.Tk()
    app = DocumentOrganizerGUI(root)
    root.mainloop()