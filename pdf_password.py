import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading


class PDFEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF加密解密工具")
        # --- 设置窗口尺寸为 800x600 ---
        self.root.minsize(800, 600)
        self.root.geometry("800x600")

        # --- 设置全局字体 ---
        self.default_font = ("Arial", 10)
        self.root.option_add("*Font", self.default_font)

        # 存储文件路径 (使用 Path 对象)
        self.file_paths = []
        self.output_path = Path("")
        self.is_encrypt_mode = True  # True为加密，False为解密

        self.setup_ui()

    def setup_ui(self):
        # 创建主框架并配置 grid 权重
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        main_frame.grid_rowconfigure(1, weight=0) # 中间设置行不扩展
        main_frame.grid_rowconfigure(2, weight=1) # 文件列表区域可扩展
        main_frame.grid_columnconfigure(0, weight=1) # 主内容区可扩展

        # --- 文件选择框架 ---
        file_frame = tk.LabelFrame(main_frame, text="文件选择")
        file_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=(0, 10))
        file_frame.grid_rowconfigure(0, weight=1) # Treeview 区域可扩展
        file_frame.grid_columnconfigure(0, weight=1) # Treeview 区域可扩展

        # 使用 Treeview 替代 Listbox
        tree_frame = tk.Frame(file_frame)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # 定义列
        columns = ("directory", "filename")
        self.file_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode="extended")

        # 定义列标题
        self.file_tree.heading("directory", text="目录")
        self.file_tree.heading("filename", text="文件名")

        # --- 调整列宽：目录列 250px，文件名列 300px ---
        self.file_tree.column("directory", width=250, minwidth=150, stretch=tk.YES)
        self.file_tree.column("filename", width=300, minwidth=150, stretch=tk.YES)

        # 添加滚动条
        v_scrollbar_files = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        h_scrollbar_files = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.file_tree.xview)
        self.file_tree.configure(yscrollcommand=v_scrollbar_files.set, xscrollcommand=h_scrollbar_files.set)

        # 布局 Treeview 和滚动条
        self.file_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar_files.grid(row=0, column=1, sticky='ns')
        h_scrollbar_files.grid(row=1, column=0, sticky='ew')


        # --- 文件操作按钮 (横向分布) ---
        file_buttons_frame = tk.Frame(file_frame)
        file_buttons_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        # 配置列权重以控制布局
        file_buttons_frame.grid_columnconfigure(0, weight=0) # 版权文本不扩展
        file_buttons_frame.grid_columnconfigure(1, weight=1) # 添加文件按钮左侧的弹性空间
        file_buttons_frame.grid_columnconfigure(2, weight=0) # 添加文件按钮不扩展
        file_buttons_frame.grid_columnconfigure(3, weight=0) # 删除文件按钮不扩展
        file_buttons_frame.grid_columnconfigure(4, weight=0) # 清空列表按钮不扩展

        # --- 添加版权说明文本 ---
        copyright_label = tk.Label(file_buttons_frame, text="", fg="gray")
        copyright_label.grid(row=0, column=0, padx=(0, 10))

        button_width = 12
        add_files_button = tk.Button(file_buttons_frame, text="添加PDF文件", command=self.add_files, width=button_width)
        remove_file_button = tk.Button(file_buttons_frame, text="删除选中文件", command=self.remove_selected_file, width=button_width)
        self.clear_button = tk.Button(file_buttons_frame, text="清空列表", command=self.clear_list, width=button_width)

        add_files_button.grid(row=0, column=2, padx=(0, 5))
        remove_file_button.grid(row=0, column=3, padx=5)
        self.clear_button.grid(row=0, column=4, padx=(5, 0))


        # --- 中间行：设置、操作模式、执行按钮 ---
        middle_container_frame = tk.Frame(main_frame)
        middle_container_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 10))
        middle_container_frame.grid_columnconfigure(0, weight=1) # 设置区可扩展
        middle_container_frame.grid_columnconfigure(1, weight=0) # 操作区不扩展
        middle_container_frame.grid_columnconfigure(2, weight=0) # 执行按钮区不扩展

        # --- 设置框架 ---
        settings_frame = tk.LabelFrame(middle_container_frame, text="设置", padx=10, pady=10)
        settings_frame.grid(row=0, column=0, sticky="nsew")
        settings_frame.grid_columnconfigure(0, weight=0)
        settings_frame.grid_columnconfigure(1, weight=1)
        settings_frame.grid_columnconfigure(2, weight=0)

        output_label = tk.Label(settings_frame, text="输出目录 (可选):")
        output_label.grid(row=0, column=0, sticky="w", padx=(0, 5))

        self.output_entry = tk.Entry(settings_frame)
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))

        self.output_button = tk.Button(settings_frame, text="浏览...", command=self.select_output_path)
        self.output_button.grid(row=0, column=2, padx=(0, 0))

        self.password_label = tk.Label(settings_frame, text="设置密码:")
        self.password_label.grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(10, 0))

        self.password_entry = tk.Entry(settings_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(10, 0))

        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(settings_frame, text="显示密码", variable=self.show_password_var,
                                             command=self.toggle_password_visibility)
        show_password_check.grid(row=1, column=2, sticky="w", pady=(10, 0))


        # --- 操作模式框架 ---
        mode_frame = tk.LabelFrame(middle_container_frame, text="操作模式", padx=15, pady=10)
        mode_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        self.mode_var = tk.StringVar(value="encrypt")
        encrypt_radio = tk.Radiobutton(mode_frame, text="加密PDF", variable=self.mode_var, value="encrypt",
                                       command=self.toggle_mode, anchor='w')
        decrypt_radio = tk.Radiobutton(mode_frame, text="解密PDF", variable=self.mode_var, value="decrypt",
                                       command=self.toggle_mode, anchor='w')
        encrypt_radio.pack(fill=tk.X, pady=3)
        decrypt_radio.pack(fill=tk.X, pady=3)


        # --- 执行按钮 ---
        self.execute_button = tk.Button(middle_container_frame, text="执行", command=self.execute_operation,
                                       bg='lightblue', font=('Arial', 12, 'bold'),
                                       width=6, height=2)
        self.execute_button.grid(row=0, column=2, sticky="w", padx=(15, 0))


        # --- 日志区域框架 ---
        log_frame = tk.LabelFrame(main_frame, text="操作日志")
        log_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0, 5))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, state=tk.DISABLED, wrap=tk.WORD)
        scrollbar_log = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar_log.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar_log.grid(row=0, column=1, sticky='ns')

        # 初始化界面状态
        self.toggle_mode()

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "encrypt":
            self.is_encrypt_mode = True
            self.password_label.config(text="设置密码:")
        else: # decrypt
            self.is_encrypt_mode = False
            self.password_label.config(text="输入密码:")

    def add_files(self):
        file_paths = filedialog.askopenfilenames(title="选择PDF文件", filetypes=[("PDF Files", "*.pdf")])
        for file_path in file_paths:
            p_file_path = Path(file_path)
            if p_file_path not in self.file_paths and p_file_path.is_file():
                self.file_paths.append(p_file_path)
                self.file_tree.insert("", tk.END, values=(str(p_file_path.parent), p_file_path.name))

    def remove_selected_file(self):
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的文件。")
            return
        
        indices_to_remove = []
        for item_id in selected_items:
            idx = self.file_tree.index(item_id)
            indices_to_remove.append(idx)
            self.file_tree.delete(item_id)
        
        for idx in sorted(indices_to_remove, reverse=True):
            del self.file_paths[idx]

    def select_output_path(self):
        folder_path = filedialog.askdirectory(title="选择输出目录")
        if folder_path:
            p_folder_path = Path(folder_path)
            if p_folder_path.is_dir():
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, str(p_folder_path))
            else:
                # 如果选择的路径不是有效目录，清空输入框或提示
                self.output_entry.delete(0, tk.END)
                messagebox.showwarning("警告", "选择的路径不是有效目录，将使用源文件目录。")

    def clear_list(self):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.file_paths.clear()

    def execute_operation(self):
        if not self.file_paths:
            messagebox.showerror("错误", "请先添加PDF文件。")
            return

        password = self.password_entry.get()
        if self.is_encrypt_mode:
            if not password:
                messagebox.showerror("错误", "加密模式下必须设置密码。")
                return
        else: # 解密
            if not password:
                messagebox.showerror("错误", "解密模式下必须输入密码。")
                return

        try:
            output_dir_str = self.output_entry.get().strip()
            # --- 更新逻辑：如果输出目录为空或无效，则 output_dir 为 None ---
            output_dir = Path(output_dir_str) if output_dir_str and Path(output_dir_str).is_dir() else None
        except Exception as e:
            messagebox.showerror("错误", f"输出路径无效: {e}")
            return

        # 禁用按钮，防止重复点击
        self.execute_button.config(state=tk.DISABLED, text="执行中...", bg='lightgray')
        self.clear_button.config(state=tk.DISABLED)

        # 在后台线程中执行操作
        thread = threading.Thread(target=self._perform_operation, args=(password, output_dir))
        thread.daemon = True
        thread.start()

    def _perform_operation(self, password, output_dir: Path):
        try:
            from PyPDF2 import PdfReader, PdfWriter
        except ImportError as e:
            self.log(f"导入 PyPDF2 失败: {e}")
            self.root.after(0, self._enable_buttons)
            return

        success_count = 0
        fail_count = 0
        total_files = len(self.file_paths)

        for i, file_path in enumerate(self.file_paths):
            try:
                if not file_path.is_file():
                    self.log(f"[{i+1}/{total_files}] 失败: 文件不存在或不是文件 - {file_path}")
                    fail_count += 1
                    continue

                reader = PdfReader(str(file_path))

                if not self.is_encrypt_mode:
                    if not reader.is_encrypted:
                        self.log(f"[{i+1}/{total_files}] 失败: 文件未加密 - {file_path.name}")
                        fail_count += 1
                        continue

                if self.is_encrypt_mode:
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)

                    writer.encrypt(password)

                    # --- 更新逻辑：确定输出目录 ---
                    if output_dir and output_dir.is_dir():
                        out_dir = output_dir
                    else:
                        # 如果 output_dir 为 None 或无效，则使用源文件目录
                        out_dir = file_path.parent

                    filename = file_path.name
                    name = file_path.stem
                    ext = file_path.suffix
                    # --- 更新前缀为 "已加密_" ---
                    output_filename = f"已加密_{name}{ext}"
                    output_path = out_dir / output_filename

                    counter = 1
                    while output_path.exists():
                        output_filename = f"已加密_{name}_{counter}{ext}"
                        output_path = out_dir / output_filename
                        counter += 1
                        if counter > 1000:
                            raise Exception("无法生成唯一文件名")

                    with open(output_path, "wb") as out_file:
                        writer.write(out_file)

                    self.log(f"[{i+1}/{total_files}] 成功: 已加密并保存到 - {output_path}")

                else:
                    if reader.is_encrypted:
                        result = reader.decrypt(password)
                        if result == 0:
                            self.log(f"[{i+1}/{total_files}] 失败: 密码错误 - {file_path.name}")
                            fail_count += 1
                            continue

                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)

                    filename = file_path.name
                    name = file_path.stem
                    ext = file_path.suffix
                    # --- 更新前缀为 "已解密_" ---
                    output_filename = f"已解密_{name}{ext}"

                    # --- 更新逻辑：确定输出目录 ---
                    if output_dir and output_dir.is_dir():
                        out_dir = output_dir
                    else:
                        # 如果 output_dir 为 None 或无效，则使用源文件目录
                        out_dir = file_path.parent

                    output_path = out_dir / output_filename

                    counter = 1
                    while output_path.exists():
                        output_filename = f"已解密_{name}_{counter}{ext}"
                        output_path = out_dir / output_filename
                        counter += 1
                        if counter > 1000:
                            raise Exception("无法生成唯一文件名")

                    with open(output_path, "wb") as out_file:
                        writer.write(out_file)

                    self.log(f"[{i+1}/{total_files}] 成功: 已解密并保存到 - {output_path}")

                success_count += 1
            except Exception as e:
                self.log(f"[{i+1}/{total_files}] 失败: 处理文件 '{file_path.name}' 时出错 - {str(e)}")
                fail_count += 1

        self.log(f"--- 操作完成: 成功 {success_count}, 失败 {fail_count} ---")
        self.root.after(0, self._enable_buttons)

    def _enable_buttons(self):
         self.execute_button.config(state=tk.NORMAL, text="执行", bg='lightblue')
         self.clear_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFEncryptorApp(root)
    root.mainloop()



