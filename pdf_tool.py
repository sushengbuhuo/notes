import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import fitz  # PyMuPDF
import os
from datetime import datetime
from PIL import Image, ImageTk
import threading
import io
#PDF工具箱-支持合并、分割、压缩、格式转化
class PDFProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF工具箱")
        self.root.geometry("750x540")
        self.root.configure(bg='#f0f0f0')
        font_style = ("宋体",11)
        self.root.option_add("*Font", font_style)
        self.style = ttk.Style()
        self.style.theme_use('clam')
         
        # 颜色定义
        self.primary_color = '#2c3e50'
        self.secondary_color = '#3498db'
        self.accent_color = '#e74c3c'
        self.light_color = '#ecf0f1'
        self.dark_color = '#34495e'
         
        # 配置样式
        self.style.configure('TNotebook', background=self.light_color)
        self.style.configure('TNotebook.Tab', 
                            background=self.dark_color, 
                            foreground='white',
                             width= 10,
                            padding=[10, 5])
        self.style.map('TNotebook.Tab', 
                      background=[('selected', self.secondary_color)],
                      expand=[('selected', [1, 1, 1, 0])])
         
        self.style.configure('TFrame', background=self.light_color)
        self.style.configure('TButton', 
                            background=self.secondary_color,
                            foreground='white',
                            font = font_style,
                            borderwidth=1,
                            width= 9,
                            focusthickness=3,
                            focuscolor=self.secondary_color)
        self.style.map('TButton', 
                      background=[('active', self.primary_color)])
         
        self.style.configure('Delete.TButton', 
                            background=self.accent_color)
        self.style.map('Delete.TButton', 
                      background=[('active', '#c0392b')])
         
        self.style.configure('Listbox', background='white', font = font_style, foreground=self.dark_color)
         
        # 初始化文件列表
        self.file_list = []
        self.preview_window = None
         
        self.create_widgets()
         
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
         
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
         
        # 标题
        title_label = tk.Label(main_frame, text="PDF工具箱", 
                              font=("黑体", 16, "bold"),
                              foreground=self.primary_color,
                              background=self.light_color)
        title_label.grid(row=0, column=0, pady=(0, 10))
         
        # 创建Notebook（选项卡控件）
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
         
        # 创建各个功能选项卡
        self.create_file_selection_tab()
        self.create_extract_tab()
        self.create_merge_tab()
        self.create_delete_tab()
        self.create_convert_tab()
        self.create_word_tab()
        self.create_compress_tab()
        self.create_rename_tab()
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W,
                             background=self.dark_color,
                             foreground='white')
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E))
         
    def create_file_selection_tab(self):
        # 文件选择选项卡
        file_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(file_frame, text="文件选择")
         
        # 配置网格
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(1, weight=1)
         
        # 按钮框架
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        # 添加文件按钮
        add_btn = ttk.Button(button_frame, text="添加文件", command=self.add_files)
        add_btn.grid(row=0, column=0, padx=(0, 5))
 
        # 添加文件夹按钮
        add_folder_btn = ttk.Button(button_frame, text="添加文件夹", command=self.add_folder)
        add_folder_btn.grid(row=0, column=1, padx=(0, 5))
 
        # 向上移动按钮
        up_btn = ttk.Button(button_frame, text="↑上移", command=self.move_up)
        up_btn.grid(row=0, column=2, padx=(0, 5))
 
        # 向下移动按钮
        down_btn = ttk.Button(button_frame, text="↓下移", command=self.move_down)
        down_btn.grid(row=0, column=3, padx=(0, 5))
 
        # 删除选中按钮
        delete_btn = ttk.Button(button_frame, text="删除选中", command=self.remove_selected,style='Delete.TButton')
        delete_btn.grid(row=0, column=5, padx=(0, 5))
 
        # 清空列表按钮
        clear_btn = ttk.Button(button_frame, text="清空列表", command=self.clear_list,style='Delete.TButton')
        clear_btn.grid(row=0, column=6, padx=(0, 5))
 
        # 预览按钮
        preview_btn = ttk.Button(button_frame, text="预览选中", command=self.preview_selected)
        preview_btn.grid(row=0, column=4, padx=(0, 5))
         
        # 文件列表框架
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
         
        # 创建带滚动条的列表框
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
         
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED,
                                      yscrollcommand=scrollbar.set,
                                      font=("Arial", 10),
                                      height=15)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.file_listbox.yview)
         
        # 绑定事件
        self.file_listbox.bind('<Delete>', lambda e: self.remove_selected())
        self.file_listbox.bind('<Double-Button-1>', lambda e: self.preview_selected())
         
    def move_up(self):
        """将选中的项目向上移动一位"""
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == 0:
            return
         
        index = selected[0]
        # 交换列表中的元素
        self.file_list[index], self.file_list[index-1] = self.file_list[index-1], self.file_list[index]
         
        # 更新列表框
        self.file_listbox.delete(index-1, index)
        self.file_listbox.insert(index, os.path.basename(self.file_list[index]))
        self.file_listbox.insert(index-1, os.path.basename(self.file_list[index-1]))
         
        # 重新选中移动后的项目
        self.file_listbox.selection_set(index-1)
        self.status_var.set(f"已向上移动选中的文件")
 
    def move_down(self):
        """将选中的项目向下移动一位"""
        selected = self.file_listbox.curselection()
        if not selected or selected[0] == len(self.file_list) - 1:
            return
         
        index = selected[0]
        # 交换列表中的元素
        self.file_list[index], self.file_list[index+1] = self.file_list[index+1], self.file_list[index]
         
        # 更新列表框
        self.file_listbox.delete(index, index+1)
        self.file_listbox.insert(index+1, os.path.basename(self.file_list[index+1]))
        self.file_listbox.insert(index, os.path.basename(self.file_list[index]))
         
        # 重新选中移动后的项目
        self.file_listbox.selection_set(index+1)
        self.status_var.set(f"已向下移动选中的文件")        
         
    def create_extract_tab(self):
        # 提取页面选项卡
        extract_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(extract_frame, text="提取页面")
         
        extract_frame.columnconfigure(1, weight=1)
         
        # 页面范围输入
        ttk.Label(extract_frame, text="页面范围:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.page_range = ttk.Entry(extract_frame, width=30)
        self.page_range.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        ttk.Label(extract_frame, text="示例: 1-3,5,7-9").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(5, 0))
         
        # 输出文件名
        ttk.Label(extract_frame, text="输出文件名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.extract_output = ttk.Entry(extract_frame, width=30)
        self.extract_output.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.extract_output.insert(0, "提取的页面.pdf")
         
        # 提取按钮
        extract_btn = ttk.Button(extract_frame, text="提取页面", 
                                command=self.extract_pages)
        extract_btn.grid(row=2, column=0, columnspan=3, pady=10)
         
    def create_merge_tab(self):
        # 合并文件选项卡
        merge_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(merge_frame, text="合并文件")
         
        merge_frame.columnconfigure(1, weight=1)
         
        # 输出文件名
        ttk.Label(merge_frame, text="输出文件名:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.merge_output = ttk.Entry(merge_frame, width=30)
        self.merge_output.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.merge_output.insert(0, "pdf合集.pdf")
         
        # 合并按钮
        merge_btn = ttk.Button(merge_frame, text="合并PDF文件", 
                              command=self.merge_pdfs)
        merge_btn.grid(row=1, column=0, columnspan=2, pady=10)
         
    def create_delete_tab(self):
        # 删除页面选项卡
        delete_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(delete_frame, text="删除页面")
         
        delete_frame.columnconfigure(1, weight=1)
         
        # 页面范围输入
        ttk.Label(delete_frame, text="要删除的页面范围:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.delete_range = ttk.Entry(delete_frame, width=30)
        self.delete_range.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        ttk.Label(delete_frame, text="示例: 1-3,5,7-9").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(5, 0))
         
        # 输出文件名
        ttk.Label(delete_frame, text="输出文件名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.delete_output = ttk.Entry(delete_frame, width=30)
        self.delete_output.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.delete_output.insert(0, "删除页面后的文档.pdf")
         
        # 删除按钮
        delete_btn = ttk.Button(delete_frame, text="删除页面", 
                               command=self.delete_pages)
        delete_btn.grid(row=2, column=0, columnspan=3, pady=10)
 
    def create_word_tab(self):
        # 转换为Word选项卡
        word_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(word_frame, text="转换为docx")
         
        word_frame.columnconfigure(1, weight=1)
         
        # 输出文件夹
        ttk.Label(word_frame, text="输出文件夹:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.word_output = ttk.Entry(word_frame, width=30)
        self.word_output.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.word_output.insert(0, "Word输出")
         
        word_browse_btn = ttk.Button(word_frame, text="浏览", command=self.browse_word_output_folder)
        word_browse_btn.grid(row=0, column=2, padx=(5, 0))
         
        # 转换按钮
        word_convert_btn = ttk.Button(word_frame, text="转换为Word", command=self.convert_to_word)
        word_convert_btn.grid(row=1, column=0, columnspan=3, pady=10)
         
    def create_convert_tab(self):
        # 转换为PNG选项卡
        convert_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(convert_frame, text="转换为PNG")
         
        convert_frame.columnconfigure(1, weight=1)
         
        # 输出文件夹
        ttk.Label(convert_frame, text="输出文件夹:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.png_output = ttk.Entry(convert_frame, width=30)
        self.png_output.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.png_output.insert(0, "PNG输出")
         
        browse_btn = ttk.Button(convert_frame, text="浏览", 
                               command=self.browse_output_folder)
        browse_btn.grid(row=0, column=2, padx=(5, 0))
         
        # 分辨率设置
        ttk.Label(convert_frame, text="分辨率 (DPI):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.png_dpi = ttk.Combobox(convert_frame, values=[72, 96, 150, 200, 300, 600], width=10)
        self.png_dpi.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        self.png_dpi.set("150")
         
        # 转换按钮
        convert_btn = ttk.Button(convert_frame, text="转换为PNG", 
                                command=self.convert_to_png)
        convert_btn.grid(row=2, column=0, columnspan=3, pady=10)
         
    def create_compress_tab(self):
        # PDF压缩选项卡
        compress_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(compress_frame, text="PDF压缩")
         
        compress_frame.columnconfigure(1, weight=1)
         
        # 压缩级别选择
        ttk.Label(compress_frame, text="压缩级别:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.compression_level = ttk.Combobox(compress_frame, 
                                            values=["高质量", "标准", "高压缩"], 
                                            width=15, state="readonly")
        self.compression_level.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        self.compression_level.set("标准")
         
        # 输出文件夹
        ttk.Label(compress_frame, text="输出文件夹:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.compress_output = ttk.Entry(compress_frame, width=30)
        self.compress_output.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.compress_output.insert(0, "压缩输出")
         
        compress_browse_btn = ttk.Button(compress_frame, text="浏览", 
                                       command=self.browse_compress_output_folder)
        compress_browse_btn.grid(row=1, column=2, padx=(5, 0))
         
        # 压缩按钮
        compress_btn = ttk.Button(compress_frame, text="压缩PDF文件", 
                                command=self.compress_pdfs)
        compress_btn.grid(row=2, column=0, columnspan=3, pady=10)
         
    def browse_compress_output_folder(self):
        folder = filedialog.askdirectory(title="选择压缩输出文件夹")
        if folder:
            self.compress_output.delete(0, tk.END)
            self.compress_output.insert(0, folder)
    def create_rename_tab(self):
        # 批量重命名选项卡
        rename_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(rename_frame, text="批量重命名")
         
        rename_frame.columnconfigure(1, weight=1)
         
        # 命名规则
        ttk.Label(rename_frame, text="命名规则:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.naming_pattern = ttk.Combobox(rename_frame, 
                                         values=["文档_001", "文件_001", "PDF_001", "自定义..."], 
                                         width=20, state="readonly")
        self.naming_pattern.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        self.naming_pattern.set("文档_001")
        self.naming_pattern.bind('<<ComboboxSelected>>', self.on_naming_pattern_change)
         
        # 自定义命名
        ttk.Label(rename_frame, text="自定义名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.custom_name = ttk.Entry(rename_frame, width=30, state="disabled")
        self.custom_name.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.custom_name.insert(0, "请输入名称模板（使用#作为数字占位符）")
         
        # 起始编号
        ttk.Label(rename_frame, text="起始编号:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.start_number = ttk.Spinbox(rename_frame, from_=1, to=9999, width=10)
        self.start_number.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        self.start_number.set("1")
         
        # 重命名按钮
        rename_btn = ttk.Button(rename_frame, text="执行重命名", 
                              command=self.batch_rename_files)
        rename_btn.grid(row=3, column=0, columnspan=2, pady=10)
         
    def on_naming_pattern_change(self, event):
        """当命名规则选择改变时启用/禁用自定义输入"""
        if self.naming_pattern.get() == "自定义...":
            self.custom_name.config(state="normal")
        else:
            self.custom_name.config(state="disabled")
 
    def batch_rename_files(self):
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
             
        pattern = self.naming_pattern.get()
        start_num = int(self.start_number.get())
         
        if pattern == "自定义...":
            custom_pattern = self.custom_name.get().strip()
            if not custom_pattern or "#" not in custom_pattern:
                messagebox.showwarning("警告", "请输入有效的自定义名称模板（必须包含#作为数字占位符）")
                return
            pattern = custom_pattern
         
        # 在后台线程中执行重命名
        def do_rename():
            try:
                self.status_var.set("正在重命名文件...")
                processed_count = 0
                current_num = start_num
                 
                for file_path in self.file_list:
                    try:
                        file_dir = os.path.dirname(file_path)
                        file_ext = os.path.splitext(file_path)[1]
                         
                        # 生成新文件名
                        if pattern == "文档_001":
                            new_name = f"文档_{current_num:03d}{file_ext}"
                        elif pattern == "文件_001":
                            new_name = f"文件_{current_num:03d}{file_ext}"
                        elif pattern == "PDF_001":
                            new_name = f"PDF_{current_num:03d}{file_ext}"
                        else:  # 自定义模式
                            new_name = pattern.replace("#", f"{current_num:03d}") + file_ext
                         
                        new_path = os.path.join(file_dir, new_name)
                         
                        # 重命名文件
                        os.rename(file_path, new_path)
                         
                        # 更新文件列表
                        self.file_list[processed_count] = new_path
                         
                        processed_count += 1
                        current_num += 1
                         
                        self.root.after(0, lambda f=os.path.basename(new_path): 
                            self.status_var.set(f"已重命名: {f}"))
                             
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "错误", f"重命名文件时出错: {str(e)}"))
                 
                # 更新列表框显示
                self.root.after(0, self.update_file_listbox)
                self.root.after(0, lambda: messagebox.showinfo(
                    "成功", f"成功重命名 {processed_count} 个文件"))
                self.root.after(0, lambda: self.status_var.set(
                    f"重命名完成: {processed_count} 个文件"))
                         
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"重命名时出错: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("重命名失败"))
                 
        threading.Thread(target=do_rename, daemon=True).start()
 
    def update_file_listbox(self):
        """更新文件列表框显示"""
        self.file_listbox.delete(0, tk.END)
        for file_path in self.file_list:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))
    def compress_pdfs(self):
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
             
        output_folder = self.compress_output.get().strip()
        compression_level = self.compression_level.get()
         
        if not output_folder:
            messagebox.showwarning("警告", "请选择输出文件夹")
            return
             
        # 在后台线程中执行压缩操作
        def do_compress():
            try:
                self.status_var.set("正在压缩PDF文件...")
                processed_count = 0
                 
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                 
                for file_path in self.file_list:
                    try:
                        # 设置压缩参数
                        if compression_level == "高质量":
                            zoom = 1.5
                        elif compression_level == "标准":
                            zoom = 1.2
                        else:  # 高压缩
                            zoom = 0.9
                         
                        doc = fitz.open(file_path)
                        output_doc = fitz.open()
                         
                        # 重新渲染页面以压缩
                        for page_num in range(len(doc)):
                            page = doc[page_num]
                            mat = fitz.Matrix(zoom, zoom)
                            pix = page.get_pixmap(matrix=mat)
                            img_bytes = pix.tobytes("png")
                             
                            # 创建新页面并插入图片
                            new_page = output_doc.new_page(width=pix.width, height=pix.height)
                            new_page.insert_image(new_page.rect, stream=img_bytes)
                         
                        # 保存压缩后的文件
                        base_name = os.path.splitext(os.path.basename(file_path))[0]
                        output_path = os.path.join(output_folder, f"{base_name}_压缩.pdf")
                        output_doc.save(output_path, garbage=4, deflate=True)
                         
                        doc.close()
                        output_doc.close()
                        processed_count += 1
                         
                        self.root.after(0, lambda f=os.path.basename(file_path): 
                            self.status_var.set(f"已压缩: {f}"))
                             
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "错误", f"处理文件 {os.path.basename(file_path)} 时出错: {str(e)}"))
                 
                self.root.after(0, lambda: messagebox.showinfo(
                    "成功", f"成功压缩 {processed_count} 个PDF文件\n输出文件夹: {output_folder}"))
                self.root.after(0, lambda: self.status_var.set(
                    f"压缩完成: {processed_count} 个文件"))
                         
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"压缩PDF时出错: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("压缩PDF失败"))
                 
        threading.Thread(target=do_compress, daemon=True).start()
     
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if files:
            for file in files:
                if file not in self.file_list:
                    self.file_list.append(file)
                    self.file_listbox.insert(tk.END, os.path.basename(file))
            self.status_var.set(f"添加了 {len(files)} 个文件")
         
    def add_folder(self):
        folder = filedialog.askdirectory(title="选择包含PDF文件的文件夹")
        if folder:
            pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) 
                        if f.lower().endswith('.pdf')]
            if pdf_files:
                for file in pdf_files:
                    if file not in self.file_list:
                        self.file_list.append(file)
                        self.file_listbox.insert(tk.END, os.path.basename(file))
                self.status_var.set(f"添加了 {len(pdf_files)} 个文件")
            else:
                messagebox.showwarning("警告", "选择的文件夹中没有PDF文件")
         
    def remove_selected(self):
        selected = self.file_listbox.curselection()
        if selected:
            # 从后往前删除，避免索引变化
            for i in selected[::-1]:
                self.file_list.pop(i)
                self.file_listbox.delete(i)
            self.status_var.set(f"删除了 {len(selected)} 个文件")
         
    def clear_list(self):
        if messagebox.askyesno("确认", "确定要清空文件列表吗？"):
            self.file_list.clear()
            self.file_listbox.delete(0, tk.END)
            self.status_var.set("已清空文件列表")
         
    def preview_selected(self):
        selected = self.file_listbox.curselection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一个PDF文件")
            return
             
        file_path = self.file_list[selected[0]]
        self.show_preview_window(file_path)
         
    def show_preview_window(self, file_path):
        """显示独立的预览窗口"""
        # 如果预览窗口已存在，先关闭它
        if self.preview_window and tk.Toplevel.winfo_exists(self.preview_window):
            self.preview_window.destroy()
         
        # 创建新预览窗口
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title(f"PDF预览 - {os.path.basename(file_path)}")
        self.preview_window.geometry("800x600")
        self.preview_window.configure(bg=self.light_color)
         
        # 主框架
        main_frame = ttk.Frame(self.preview_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
         
        # 控制框架
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
         
        # 页码控制
        ttk.Label(control_frame, text="页码:").pack(side=tk.LEFT)
         
        self.page_var = tk.StringVar()
        page_spinbox = ttk.Spinbox(control_frame, from_=1, to=100, 
                                  textvariable=self.page_var, width=5,
                                  command=lambda: self.update_preview(file_path))
        page_spinbox.pack(side=tk.LEFT, padx=(5, 10))
         
        # 缩放控制
        ttk.Label(control_frame, text="缩放:").pack(side=tk.LEFT)
        self.zoom_var = tk.StringVar(value="2.0")
        zoom_combo = ttk.Combobox(control_frame, textvariable=self.zoom_var,
                                 values=["0.5", "1.0", "1.5", "2.0", "2.5", "3.0"],
                                 width=5)
        zoom_combo.pack(side=tk.LEFT, padx=(5, 10))
        zoom_combo.bind('<<ComboboxSelected>>', lambda e: self.update_preview(file_path))
         
        # 关闭按钮
        close_btn = ttk.Button(control_frame, text="关闭", 
                              command=self.preview_window.destroy)
        close_btn.pack(side=tk.RIGHT)
         
        # 图片显示区域
        img_frame = ttk.Frame(main_frame)
        img_frame.pack(fill=tk.BOTH, expand=True)
         
        # 创建画布和滚动条
        v_scrollbar = ttk.Scrollbar(img_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(img_frame, orient=tk.HORIZONTAL)
         
        self.canvas = tk.Canvas(img_frame, bg='white',
                               yscrollcommand=v_scrollbar.set,
                               xscrollcommand=h_scrollbar.set)
         
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
         
        # 网格布局
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
         
        img_frame.columnconfigure(0, weight=1)
        img_frame.rowconfigure(0, weight=1)
         
        # 绑定鼠标滚轮事件
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)
        self.canvas.bind("<Button-5>", self.on_mousewheel)
         
        # 加载PDF信息
        try:
            self.preview_doc = fitz.open(file_path)
            total_pages = len(self.preview_doc)
             
            # 设置页码范围
            page_spinbox.config(to=total_pages)
            self.page_var.set("1")
             
            # 显示第一页
            self.update_preview(file_path)
             
        except Exception as e:
            messagebox.showerror("错误", f"打开PDF文件时出错: {str(e)}")
            self.preview_window.destroy()
             
    def on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
             
    def update_preview(self, file_path):
        """更新预览图像"""
        try:
            page_num = int(self.page_var.get()) - 1
            zoom = float(self.zoom_var.get())
             
            if page_num < 0 or page_num >= len(self.preview_doc):
                return
                 
            # 获取页面
            page = self.preview_doc[page_num]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
             
            # 转换为PIL图像
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
             
            # 转换为PhotoImage
            photo = ImageTk.PhotoImage(img)
             
            # 清除画布并显示新图像
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
             
            # 保持引用
            self.canvas.image = photo
             
            # 更新状态
            self.status_var.set(f"预览: {os.path.basename(file_path)} 第 {page_num + 1} 页")
             
        except Exception as e:
            messagebox.showerror("错误", f"更新预览时出错: {str(e)}")
     
    def parse_page_range(self, page_range, max_pages):
        """解析页面范围字符串，如 '1-3,5,7-9'"""
        pages = set()
        parts = page_range.split(',')
         
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                try:
                    start = int(start) - 1  # 转换为0-based
                    end = int(end) - 1
                    if start < 0:
                        start = 0
                    if end >= max_pages:
                        end = max_pages - 1
                    pages.update(range(start, end + 1))
                except ValueError:
                    raise ValueError(f"无效的页面范围: {part}")
            else:
                try:
                    page = int(part) - 1  # 转换为0-based
                    if page < 0:
                        page = 0
                    if page >= max_pages:
                        page = max_pages - 1
                    pages.add(page)
                except ValueError:
                    raise ValueError(f"无效的页码: {part}")
                     
        return sorted(pages)
         
    def extract_pages(self):
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
             
        page_range = self.page_range.get().strip()
        output_file = self.extract_output.get().strip()
         
        if not page_range:
            messagebox.showwarning("警告", "请输入页面范围")
            return
             
        if not output_file:
            messagebox.showwarning("警告", "请输入输出文件名")
            return
             
        # 确保输出文件有.pdf扩展名
        if not output_file.lower().endswith('.pdf'):
            output_file += '.pdf'
             
        # 选择输出位置
        output_path = filedialog.asksaveasfilename(
            title="保存提取的页面",
            defaultextension=".pdf",
            initialfile=output_file,
            filetypes=[("PDF文件", "*.pdf")]
        )
         
        if not output_path:
            return
             
        # 在后台线程中执行提取操作
        def do_extract():
            try:
                self.status_var.set("正在提取页面...")
                 
                merged_doc = fitz.open()
                processed_count = 0
                 
                for file_path in self.file_list:
                    try:
                        doc = fitz.open(file_path)
                        max_pages = len(doc)
                        pages_to_extract = self.parse_page_range(page_range, max_pages)
                         
                        if pages_to_extract:
                            merged_doc.insert_pdf(doc, from_page=min(pages_to_extract), 
                                                 to_page=max(pages_to_extract))
                            processed_count += len(pages_to_extract)
                             
                        doc.close()
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "错误", f"处理文件 {os.path.basename(file_path)} 时出错: {str(e)}"))
                 
                if processed_count > 0:
                    merged_doc.save(output_path)
                    merged_doc.close()
                    self.root.after(0, lambda: self.status_var.set(
                        f"成功提取 {processed_count} 个页面到 '{os.path.basename(output_path)}'"))
                    self.root.after(0, lambda: messagebox.showinfo(
                        "成功", f"成功提取 {processed_count} 个页面到\n{output_path}"))
                else:
                    merged_doc.close()
                    self.root.after(0, lambda: self.status_var.set("没有提取任何页面"))
                    self.root.after(0, lambda: messagebox.showwarning(
                        "警告", "没有提取任何页面，请检查页面范围"))
                         
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"提取页面时出错: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("提取页面失败"))
                 
        threading.Thread(target=do_extract, daemon=True).start()
         
    def merge_pdfs(self):
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
             
        output_file = self.merge_output.get().strip()
         
        if not output_file:
            messagebox.showwarning("警告", "请输入输出文件名")
            return
             
        # 确保输出文件有.pdf扩展名
        if not output_file.lower().endswith('.pdf'):
            output_file += '.pdf'
             
        # 选择输出位置
        output_path = filedialog.asksaveasfilename(
            title="保存合并的PDF",
            defaultextension=".pdf",
            initialfile=output_file,
            filetypes=[("PDF文件", "*.pdf")]
        )
         
        if not output_path:
            return
             
        # 在后台线程中执行合并操作
        def do_merge():
            try:
                self.status_var.set("正在合并PDF文件...")
                 
                merged_doc = fitz.open()
                processed_count = 0
                 
                for file_path in self.file_list:
                    try:
                        doc = fitz.open(file_path)
                        merged_doc.insert_pdf(doc)
                        doc.close()
                        processed_count += 1
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "错误", f"处理文件 {os.path.basename(file_path)} 时出错: {str(e)}"))
                 
                if processed_count > 0:
                    # 添加元数据
                    merged_doc.set_metadata({
                        "title": "合并的PDF文档",
                        "author": "PDF工具箱",
                        "creator": "PyMuPDF",
                        "creationDate": datetime.now().strftime("%Y%m%d%H%M%S"),
                        "subject": "多个PDF合并的文档"
                    })
                     
                    merged_doc.save(output_path)
                    merged_doc.close()
                    self.root.after(0, lambda: self.status_var.set(
                        f"成功合并 {processed_count} 个PDF文件到 '{os.path.basename(output_path)}'"))
                    self.root.after(0, lambda: messagebox.showinfo(
                        "成功", f"成功合并 {processed_count} 个PDF文件到\n{output_path}"))
                else:
                    merged_doc.close()
                    self.root.after(0, lambda: self.status_var.set("没有合并任何文件"))
                    self.root.after(0, lambda: messagebox.showwarning(
                        "警告", "没有合并任何文件"))
                         
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"合并PDF时出错: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("合并PDF失败"))
                 
        threading.Thread(target=do_merge, daemon=True).start()
         
    def delete_pages(self):
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
             
        page_range = self.delete_range.get().strip()
        output_file = self.delete_output.get().strip()
         
        if not page_range:
            messagebox.showwarning("警告", "请输入要删除的页面范围")
            return
             
        if not output_file:
            messagebox.showwarning("警告", "请输入输出文件名")
            return
             
        # 确保输出文件有.pdf扩展名
        if not output_file.lower().endswith('.pdf'):
            output_file += '.pdf'
             
        # 选择输出位置
        output_path = filedialog.asksaveasfilename(
            title="保存删除页面后的PDF",
            defaultextension=".pdf",
            initialfile=output_file,
            filetypes=[("PDF文件", "*.pdf")]
        )
         
        if not output_path:
            return
             
        # 在后台线程中执行删除操作
        def do_delete():
            try:
                self.status_var.set("正在删除页面...")
                 
                for file_path in self.file_list:
                    try:
                        doc = fitz.open(file_path)
                        max_pages = len(doc)
                        pages_to_delete = self.parse_page_range(page_range, max_pages)
                         
                        if pages_to_delete:
                            # 从后往前删除页面，避免索引变化
                            for page_num in sorted(pages_to_delete, reverse=True):
                                doc.delete_page(page_num)
                             
                            # 保存处理后的文件
                            base_name = os.path.splitext(os.path.basename(file_path))[0]
                            file_output_path = os.path.join(
                                os.path.dirname(output_path), 
                                f"{base_name}_{os.path.basename(output_path)}"
                            )
                             
                            doc.save(file_output_path)
                            doc.close()
                             
                            self.root.after(0, lambda: self.status_var.set(
                                f"成功处理 {os.path.basename(file_path)}"))
                        else:
                            doc.close()
                             
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "错误", f"处理文件 {os.path.basename(file_path)} 时出错: {str(e)}"))
                 
                self.root.after(0, lambda: messagebox.showinfo(
                    "成功", f"页面删除操作完成\n文件保存在: {os.path.dirname(output_path)}"))
                self.root.after(0, lambda: self.status_var.set("页面删除操作完成"))
                         
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"删除页面时出错: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("删除页面失败"))
                 
        threading.Thread(target=do_delete, daemon=True).start()
         
    def convert_to_word(self):
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
             
        output_folder = self.word_output.get().strip()
         
        if not output_folder:
            messagebox.showwarning("警告", "请选择输出文件夹")
            return
             
        # 在后台线程中执行转换操作
        def do_convert():
            try:
                self.status_var.set("正在转换为Word...")
                processed_count = 0
                 
                # 创建输出文件夹（如果不存在）
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                 
                for file_path in self.file_list:
                    try:
                        # 使用pdf2docx库进行转换:cite[2]:cite[4]
                        base_name = os.path.splitext(os.path.basename(file_path))[0]
                        output_path = os.path.join(output_folder, f"{base_name}.docx")
                         
                        # 转换PDF到Word
                        from pdf2docx import Converter
                        cv = Converter(file_path)
                        cv.convert(output_path)
                        cv.close()
                         
                        processed_count += 1
                        self.root.after(0, lambda f=os.path.basename(file_path): 
                            self.status_var.set(f"已转换: {f}"))
                             
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "错误", f"处理文件 {os.path.basename(file_path)} 时出错: {str(e)}"))
                 
                self.root.after(0, lambda: messagebox.showinfo(
                    "成功", f"成功转换 {processed_count} 个PDF到Word文档\n输出文件夹: {output_folder}"))
                self.root.after(0, lambda: self.status_var.set(
                    f"转换完成: {processed_count} 个文件"))
                         
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"转换为Word时出错: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("转换Word失败"))
                 
        threading.Thread(target=do_convert, daemon=True).start()
 
    def browse_word_output_folder(self):
        folder = filedialog.askdirectory(title="选择Word输出文件夹")
        if folder:
            self.word_output.delete(0, tk.END)
            self.word_output.insert(0, folder)
 
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="选择PNG输出文件夹")
        if folder:
            self.png_output.delete(0, tk.END)
            self.png_output.insert(0, folder)
         
    def convert_to_png(self):
        if not self.file_list:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
             
        output_folder = self.png_output.get().strip()
        dpi = self.png_dpi.get().strip()
         
        if not output_folder:
            messagebox.showwarning("警告", "请选择输出文件夹")
            return
             
        if not dpi.isdigit() or int(dpi) <= 0:
            messagebox.showwarning("警告", "请输入有效的DPI值")
            return
             
        dpi = int(dpi)
        zoom = dpi / 72  # 默认DPI是72
         
        # 在后台线程中执行转换操作
        def do_convert():
            try:
                self.status_var.set("正在转换为PNG...")
                total_pages = 0
                 
                # 创建输出文件夹（如果不存在）
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                 
                for file_path in self.file_list:
                    try:
                        doc = fitz.open(file_path)
                        base_name = os.path.splitext(os.path.basename(file_path))[0]
                         
                        for page_num in range(len(doc)):
                            page = doc[page_num]
                            mat = fitz.Matrix(zoom, zoom)
                            pix = page.get_pixmap(matrix=mat)
                             
                            output_path = os.path.join(
                                output_folder, 
                                f"{base_name}_{page_num + 1}.png"
                            )
                             
                            pix.save(output_path)
                            total_pages += 1
                             
                        doc.close()
                        self.root.after(0, lambda f=os.path.basename(file_path): 
                            self.status_var.set(f"已转换: {f}"))
                             
                    except Exception as e:
                        self.root.after(0, lambda: messagebox.showerror(
                            "错误", f"处理文件 {os.path.basename(file_path)} 时出错: {str(e)}"))
                 
                self.root.after(0, lambda: messagebox.showinfo(
                    "成功", f"成功转换 {total_pages} 个页面到PNG\n输出文件夹: {output_folder}"))
                self.root.after(0, lambda: self.status_var.set(
                    f"转换完成: {total_pages} 个页面"))
                         
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"转换为PNG时出错: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("转换PNG失败"))
                 
        threading.Thread(target=do_convert, daemon=True).start()
 
# 运行应用程序
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFProcessor(root)
    root.mainloop()