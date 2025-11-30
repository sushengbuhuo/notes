import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import time
import platform
import sys
from datetime import datetime, timedelta
#https://www.52pojie.cn/thread-2070732-1-1.html
class WeChatCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("微信垃圾专清工具2.2 ")
        self.root.geometry("550x580")
        self.root.minsize(530, 560)
        self.root.resizable(True, True)
         
        # 系统信息检测
        self.system_info = self.get_system_info()
         
        # 设置中文字体
        self.setup_fonts()
         
        # 初始化变量
        self.user_dir = tk.StringVar()
        self.selected_users = []
        self.clean_items = {
            "聊天记录": tk.BooleanVar(value=True),
            "聊天备份": tk.BooleanVar(value=True),
            "图片": tk.BooleanVar(value=True),
            "视频": tk.BooleanVar(value=True),
            "语音": tk.BooleanVar(value=True),
            "缓存文件": tk.BooleanVar(value=True)
        }
         
        # 时间选择相关变量
        self.time_option = tk.StringVar(value="all")  # all:全部, days:指定天数
        self.days_var = tk.StringVar(value="30")
         
        # 路径映射 - 适配微信3.9.11.19及新旧版本，补充FileStorage下的路径
        self.path_mappings = {
            "聊天记录": ["Msg", "Message", "msg", "message", "FileStorage/Msg"],
            "聊天备份": ["Backup", "backup", "FileStorage/Backup"],
            "图片": [
                "Image", "Photos", "image", "photos",
                "FileStorage/Image", "FileStorage/Images",  # 微信3.x新增路径
                "FileStorage/Image2", "FileStorage/Photo"   # 兼容更多变体
            ],
            "视频": [
                "Video", "video",
                "FileStorage/Video", "FileStorage/Videos",   # 微信3.x新增路径
                "FileStorage/Video2"
            ],
            "语音": [
                "Voice", "voice",
                "FileStorage/Voice", "FileStorage/Voices"    # 微信3.x新增路径
            ],
            "缓存文件": [
                "Cache", "Temp", "cache", "temp",
                "FileStorage/Cache", "FileStorage/Temp",     # 微信3.x新增路径
                "FileStorage/Cache2", "FileStorage/Temp2"
            ]
        }
         
        # 提取所有可能的微信特征子目录，用于识别用户文件夹
        self.wechat_feature_dirs = set()
        for dirs in self.path_mappings.values():
            self.wechat_feature_dirs.update(dirs)
         
        self.total_cleaned = 0
        self.estimated_size = 0
        self.is_cleaning = False
         
        # 自动获取默认微信目录
        self.set_default_dir()
         
        # 创建UI
        self.create_widgets()
     
    def get_system_info(self):
        """获取系统信息"""
        return {
            "system": platform.system(),
            "architecture": platform.architecture()[0],
            "release": platform.release()
        }
     
    def setup_fonts(self):
        """设置中文字体"""
        if self.system_info["system"] == "Windows":
            default_font = ("SimHei", 9)
        elif self.system_info["system"] == "Darwin":
            default_font = ("Heiti TC", 9)
        else:
            default_font = ("WenQuanYi Micro Hei", 9)
        self.root.option_add("*Font", default_font)
     
    def set_default_dir(self):
        """自动设置默认微信目录"""
        try:
            # 获取系统文档文件夹
            if self.system_info["system"] == "Windows":
                import ctypes.wintypes
                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                # 使用SHGetFolderPathW的兼容写法（Win7支持）
                ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
                docs_path = buf.value
            else:
                docs_path = os.path.expanduser("~/Documents")
             
            # 检查可能的微信目录
            possible_paths = [
                os.path.join(docs_path, "xwechat_files"),
                os.path.join(docs_path, "WeChat Files"),
                os.path.join(docs_path, "wechat_files"),
                os.path.join(os.path.expanduser("~"), "WeChat Files")  # 新增常见路径
            ]
             
            # 设置第一个存在的目录作为默认
            for path in possible_paths:
                if os.path.exists(path) and os.path.isdir(path):
                    self.user_dir.set(path)
                    return
             
            self.user_dir.set("")
             
        except Exception as e:
            self.user_dir.set("")
     
    def create_widgets(self):
        """创建界面组件"""
        # 主容器使用单列布局，所有控件横向充满
        main_frame = ttk.Frame(self.root, padding="5 5 5 5")
        main_frame.pack(fill="both", expand=True)
         
        # 0: 标题
        ttk.Label(
            main_frame, 
            text="微信垃圾专清工具", 
            font=("SimHei", 12, "bold")
        ).pack(fill="x", pady=(0, 5), anchor="w")
         
        # 1: 目录选择区域
        dir_frame = ttk.LabelFrame(main_frame, text="微信目录设置")
        dir_frame.pack(fill="x", pady=2)
         
        # 目录选择区内部分为一行，输入框占满剩余空间
        dir_inner = ttk.Frame(dir_frame)
        dir_inner.pack(fill="x", padx=3, pady=3)
        dir_inner.grid_columnconfigure(1, weight=1)  # 输入框自适应宽度
         
        ttk.Label(dir_inner, text="数据路径:").grid(row=0, column=0, padx=(0, 5), sticky="w")
        ttk.Entry(dir_inner, textvariable=self.user_dir).grid(row=0, column=1, sticky="ew")
         
        # 按钮框靠右放置
        btn_box = ttk.Frame(dir_inner)
        btn_box.grid(row=0, column=2, padx=(5, 0))
         
        ttk.Button(btn_box, text="浏览...", command=self.browse_dir, width=7).pack(side="left", padx=(0, 2))
        ttk.Button(btn_box, text="加载用户", command=self.load_users, width=7).pack(side="left")
         
        # 时间选择区域
        time_frame = ttk.LabelFrame(main_frame, text="清理时间范围")
        time_frame.pack(fill="x", pady=2)
         
        time_inner = ttk.Frame(time_frame)
        time_inner.pack(fill="x", padx=5, pady=3)
         
        ttk.Radiobutton(time_inner, text="清理所有文件", variable=self.time_option, value="all").grid(
            row=0, column=0, padx=10, sticky="w")
         
        ttk.Radiobutton(time_inner, text="仅清理指定天数之前的文件", variable=self.time_option, value="days").grid(
            row=0, column=1, padx=5, sticky="w")
         
        ttk.Label(time_inner, text="天数:").grid(row=0, column=2, padx=(5, 2), sticky="w")
         
        days_entry = ttk.Entry(time_inner, textvariable=self.days_var, width=5)
        days_entry.grid(row=0, column=3, sticky="w")
         
        ttk.Label(time_inner, text="天前（保留最近数据）").grid(row=0, column=4, padx=2, sticky="w")
         
        # 2: 清理选项区域
        clean_frame = ttk.LabelFrame(main_frame, text="选择清理内容")
        clean_frame.pack(fill="x", pady=2)
         
        options_frame = ttk.Frame(clean_frame)
        options_frame.pack(fill="x", padx=5, pady=2)
         
        # 每行3个选项，紧凑排列
        row, col = 0, 0
        for item in self.clean_items:
            ttk.Checkbutton(options_frame, text=item, variable=self.clean_items[item]).grid(
                row=row, column=col, padx=8, pady=1, sticky="w")
            col += 1
            if col >= 3:
                col = 0
                row += 1
         
        # 3: 用户选择区域（占满剩余高度）
        user_frame = ttk.LabelFrame(main_frame, text="选择微信用户")
        user_frame.pack(fill="both", expand=True, pady=2)
         
        user_inner = ttk.Frame(user_frame)
        user_inner.pack(fill="both", expand=True, padx=3, pady=3)
        user_inner.grid_columnconfigure(0, weight=1)
        user_inner.grid_rowconfigure(0, weight=1)
         
        self.user_listbox = tk.Listbox(user_inner, selectmode="extended", height=5)
        self.user_listbox.grid(row=0, column=0, sticky="nsew")
         
        scrollbar = ttk.Scrollbar(user_inner, orient="vertical", command=self.user_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.user_listbox.config(yscrollcommand=scrollbar.set)
         
        # 4: 预估空间区域
        estimate_frame = ttk.LabelFrame(main_frame, text="预估清理空间")
        estimate_frame.pack(fill="x", pady=2)
         
        estimate_inner = ttk.Frame(estimate_frame)
        estimate_inner.pack(fill="x", padx=5, pady=2)
        estimate_inner.grid_columnconfigure(0, weight=1)
         
        self.estimate_var = tk.StringVar(value="请选择用户和清理项后估算")
        ttk.Label(estimate_inner, textvariable=self.estimate_var).grid(row=0, column=0, sticky="w")
        ttk.Button(estimate_inner, text="估算空间", command=self.calculate_estimated_size, width=10).grid(row=0, column=1, padx=(5, 0))
         
        # 5: 进度和结果区域
        progress_frame = ttk.LabelFrame(main_frame, text="清理进度")
        progress_frame.pack(fill="x", pady=2)
         
        progress_inner = ttk.Frame(progress_frame)
        progress_inner.pack(fill="x", padx=5, pady=2)
        progress_inner.grid_columnconfigure(0, weight=1)
         
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_inner, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 2))
         
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(progress_inner, textvariable=self.status_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 1))
         
        self.result_var = tk.StringVar(value="清理结果将显示在这里")
        ttk.Label(progress_inner, textvariable=self.result_var, wraplength=500).grid(row=2, column=0, columnspan=2, sticky="w")
         
        # 6: 按钮区域（靠右对齐）
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=5)
         
        # 用空白标签将按钮推到右侧
        ttk.Label(btn_frame, text="").pack(side="left", expand=True)
         
        ttk.Button(btn_frame, text="一键清理", command=self.start_cleaning, width=10).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="退出", command=self.root.quit, width=8).pack(side="left")
     
    def is_wechat_user_dir(self, dir_path):
        """判断一个目录是否为微信用户数据目录"""
        try:
            # 获取目录下的所有子目录（包括一级子目录）
            subdirs = set()
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    subdirs.add(item.lower())
                    # 检查一级子目录下的二级目录（适配FileStorage结构）
                    for subitem in os.listdir(item_path):
                        subitem_path = os.path.join(item_path, subitem)
                        if os.path.isdir(subitem_path):
                            subdirs.add(f"{item.lower()}/{subitem.lower()}")
             
            # 检查是否包含至少一个微信特征子目录
            for feature in self.wechat_feature_dirs:
                if feature.lower() in subdirs:
                    return True
            return False
        except Exception:
            return False
     
    def is_valid_wechat_root_dir(self, dir_path):
        """判断一个目录是否为有效的微信根目录（包含至少一个用户目录）"""
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            return False
             
        try:
            # 检查目录下是否有至少一个微信用户目录
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    if (item.startswith("wxid_") or item.startswith("gh_")) or self.is_wechat_user_dir(item_path):
                        return True
            return False
        except Exception:
            return False
     
    def browse_dir(self):
        """浏览并选择目录，兼容自定义名称的微信文件夹"""
        dir_path = filedialog.askdirectory(title="选择微信数据文件夹")
        if dir_path:
            # 检查是否为有效的微信目录（不限制名称）
            if self.is_valid_wechat_root_dir(dir_path):
                self.user_dir.set(dir_path)
            else:
                messagebox.showwarning(
                    "目录验证", 
                    "所选目录未检测到微信用户数据。\n请确认这是存放微信用户数据的根目录。"
                )
     
    def load_users(self):
        """加载用户列表（支持新版和旧版微信用户文件夹）"""
        dir_path = self.user_dir.get()
        if not dir_path:
            messagebox.showwarning("警告", "请先选择微信数据文件夹")
            return
             
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            messagebox.showerror("错误", "所选路径不存在或不是一个有效的目录")
            return
         
        # 检查是否为有效的微信目录（不限制名称）
        if not self.is_valid_wechat_root_dir(dir_path):
            messagebox.showerror(
                "目录无效", 
                "所选目录未包含微信用户数据。\n请选择存放微信用户数据的根目录。"
            )
            return
         
        self.user_listbox.delete(0, tk.END)
         
        try:
            user_count = 0
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    # 识别条件：
                    # 1. 新版微信：以wxid_或gh_开头
                    # 2. 旧版微信：包含微信特征子目录（如Msg、Image等）
                    if (item.startswith("wxid_") or item.startswith("gh_")) or self.is_wechat_user_dir(item_path):
                        self.user_listbox.insert(tk.END, item)
                        user_count += 1
             
            if user_count == 0:
                messagebox.showinfo("信息", "未在该目录下找到微信用户数据")
            else:
                self.status_var.set(f"已加载 {user_count} 个微信用户")
        except Exception as e:
            messagebox.showerror("错误", f"加载用户失败: {str(e)}")
     
    def get_selected_users(self):
        """获取选中的用户"""
        selected_indices = self.user_listbox.curselection()
        if not selected_indices:
            return []
        return [self.user_listbox.get(i) for i in selected_indices]
     
    def get_selected_clean_items(self):
        """获取选中的清理项"""
        return [item for item, var in self.clean_items.items() if var.get()]
     
    def get_days_threshold(self):
        """获取天数阈值，返回时间戳"""
        if self.time_option.get() == "all":
            return None  # 清理所有文件
         
        try:
            days = int(self.days_var.get())
            if days <= 0:
                raise ValueError("天数必须为正数")
                 
            # 计算阈值时间（days天前的当前时间）
            threshold = datetime.now() - timedelta(days=days)
            return threshold.timestamp()
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的天数: {str(e)}")
            return None
     
    def format_size(self, size_bytes):
        """格式化文件大小显示"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
     
    def calculate_estimated_size(self):
        """计算预估清理空间，适配微信3.9.11.19的目录结构"""
        dir_path = self.user_dir.get()
        if not dir_path or not os.path.exists(dir_path):
            messagebox.showwarning("警告", "请先选择有效的微信数据文件夹")
            return
         
        self.selected_users = self.get_selected_users()
        if not self.selected_users:
            messagebox.showwarning("警告", "请至少选择一个微信用户")
            return
         
        selected_items = self.get_selected_clean_items()
        if not selected_items:
            messagebox.showwarning("警告", "请至少选择一项清理内容")
            return
         
        # 验证时间设置
        threshold = self.get_days_threshold()
        if threshold is None and self.time_option.get() == "days":
            return
         
        self.status_var.set("正在计算预估空间...")
        self.root.update()
         
        total_estimate = 0
        base_dir = self.user_dir.get()
         
        try:
            for user in self.selected_users:
                user_dir = os.path.join(base_dir, user)
                # 遍历所有选中的清理项
                for item in selected_items:
                    # 检查该清理项对应的所有可能路径（适配新版微信）
                    for subpath in self.path_mappings.get(item, []):
                        path = os.path.join(user_dir, subpath)
                        if os.path.exists(path):
                            # 根据时间条件计算需要清理的大小
                            if threshold:
                                total_estimate += self.get_filtered_dir_size(path, threshold)
                            else:
                                if os.path.isfile(path):
                                    total_estimate += os.path.getsize(path)
                                else:
                                    total_estimate += self.get_dir_size(path)
             
            self.estimated_size = total_estimate
            size_str = self.format_size(total_estimate)
             
            if threshold:
                days = int(self.days_var.get())
                self.estimate_var.set(f"预估可清理 {days} 天前的文件: {size_str}")
            else:
                self.estimate_var.set(f"预估可清理所有文件: {size_str}")
                 
            self.status_var.set("预估计算完成")
        except Exception as e:
            self.status_var.set("预估计算失败")
            messagebox.showerror("错误", f"计算预估空间失败: {str(e)}")
     
    def get_filtered_dir_size(self, path, threshold):
        """计算符合时间条件的文件总大小"""
        total_size = 0
         
        if os.path.isfile(path):
            # 检查单个文件是否符合条件
            file_mtime = os.path.getmtime(path)
            if file_mtime < threshold:
                total_size += os.path.getsize(path)
        else:
            # 检查目录中的文件（包含子目录递归）
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp) and not os.path.islink(fp):
                        try:
                            file_mtime = os.path.getmtime(fp)
                            if file_mtime < threshold:
                                total_size += os.path.getsize(fp)
                        except:
                            continue
        return total_size
     
    def start_cleaning(self):
        """开始清理过程"""
        dir_path = self.user_dir.get()
        if not dir_path or not os.path.exists(dir_path):
            messagebox.showwarning("警告", "请先选择有效的微信数据文件夹")
            return
         
        self.selected_users = self.get_selected_users()
        if not self.selected_users:
            messagebox.showwarning("警告", "请至少选择一个微信用户")
            return
         
        selected_items = self.get_selected_clean_items()
        if not selected_items:
            messagebox.showwarning("警告", "请至少选择一项清理内容")
            return
         
        # 验证时间设置
        threshold = self.get_days_threshold()
        if threshold is None and self.time_option.get() == "days":
            return
         
        # 计算预估大小
        if self.estimated_size == 0:
            self.calculate_estimated_size()
            if self.estimated_size == 0:
                time_desc = f"{self.days_var.get()}天前的" if self.time_option.get() == "days" else "所有"
                confirm = messagebox.askyesno(
                    "确认清理", 
                    f"未检测到可清理的{time_desc}文件，仍要继续清理吗？\n用户: {', '.join(self.selected_users)}\n项目: {', '.join(selected_items)}"
                )
                if not confirm:
                    return
         
        # 显示确认信息
        size_str = self.format_size(self.estimated_size)
        time_desc = f"{self.days_var.get()}天前的" if self.time_option.get() == "days" else "所有"
         
        confirm = messagebox.askyesno(
            "确认清理", 
            f"本次将清理{time_desc}: {', '.join(selected_items)}\n预估可释放: {size_str}\n用户: {', '.join(self.selected_users)}\n\n清理后数据将无法恢复，是否继续?"
        )
        if not confirm:
            return
         
        self.is_cleaning = True
        self.total_cleaned = 0
        self.progress_var.set(0)
        self.status_var.set("开始清理...")
         
        # 启动清理线程
        threading.Thread(target=self.perform_cleaning, args=(threshold,), daemon=True).start()
        self.update_progress()
     
    def perform_cleaning(self, threshold):
        """执行清理操作"""
        base_dir = self.user_dir.get()
        selected_items = self.get_selected_clean_items()
        total_users = len(self.selected_users)
         
        try:
            for user_idx, user in enumerate(self.selected_users):
                user_dir = os.path.join(base_dir, user)
                self.status_var.set(f"正在清理用户: {user}")
                 
                # 计算该用户需要处理的项目总数
                user_total_items = 0
                for item in selected_items:
                    for subpath in self.path_mappings.get(item, []):
                        path = os.path.join(user_dir, subpath)
                        if os.path.exists(path):
                            user_total_items += 1
                 
                # 处理每个清理项目
                item_count = 0
                for item in selected_items:
                    for subpath in self.path_mappings.get(item, []):
                        path = os.path.join(user_dir, subpath)
                        if os.path.exists(path):
                            item_count += 1
                            # 更新进度
                            progress = (user_idx / total_users) * 100 + (item_count / user_total_items) * (100 / total_users)
                            self.progress_var.set(progress)
                             
                            self.status_var.set(f"正在清理 {user} 的 {item}（{subpath}）")  # 显示当前处理的路径
                            # 根据时间条件清理
                            if threshold:
                                self.clean_filtered_path(path, item, threshold)
                            else:
                                self.clean_path(path, item)
             
            self.status_var.set("清理完成!")
            self.progress_var.set(100)
             
            size_str = self.format_size(self.total_cleaned)
            self.result_var.set(f"成功清理 {size_str} 的垃圾文件")
            messagebox.showinfo("完成", f"清理完成！共释放 {size_str} 存储空间")
             
        except Exception as e:
            self.status_var.set(f"清理过程中出错")
            self.result_var.set(f"错误: {str(e)}")
            messagebox.showerror("错误", f"清理失败: {str(e)}")
        finally:
            self.is_cleaning = False
     
    def clean_filtered_path(self, path, item_name, threshold):
        """清理符合时间条件的文件"""
        try:
            if os.path.isfile(path):
                file_mtime = os.path.getmtime(path)
                if file_mtime < threshold:
                    file_size = os.path.getsize(path)
                    os.remove(path)
                    self.total_cleaned += file_size
            elif os.path.isdir(path):
                # 先清理子文件
                for dirpath, _, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp) and not os.path.islink(fp):
                            try:
                                file_mtime = os.path.getmtime(fp)
                                if file_mtime < threshold:
                                    file_size = os.path.getsize(fp)
                                    os.remove(fp)
                                    self.total_cleaned += file_size
                            except:
                                continue
                 
                # 清理空目录
                for dirpath, dirnames, _ in os.walk(path, topdown=False):
                    for dirname in dirnames:
                        dp = os.path.join(dirpath, dirname)
                        if os.path.exists(dp) and len(os.listdir(dp)) == 0:
                            try:
                                os.rmdir(dp)
                            except:
                                continue
        except Exception as e:
            self.status_var.set(f"清理 {item_name} 时出错: {str(e)}")
            time.sleep(1)
     
    def clean_path(self, path, item_name):
        """清理所有文件（不考虑时间）"""
        try:
            if os.path.isfile(path):
                file_size = os.path.getsize(path)
                os.remove(path)
                self.total_cleaned += file_size
            elif os.path.isdir(path):
                dir_size = self.get_dir_size(path)
                shutil.rmtree(path, ignore_errors=True)
                self.total_cleaned += dir_size
        except Exception as e:
            self.status_var.set(f"清理 {item_name} 时出错: {str(e)}")
            time.sleep(1)
     
    def get_dir_size(self, path):
        """计算目录总大小"""
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp) and not os.path.islink(fp):
                    try:
                        total_size += os.path.getsize(fp)
                    except:
                        continue
        return total_size
     
    def update_progress(self):
        """更新进度条显示"""
        if self.is_cleaning:
            self.root.after(100, self.update_progress)
 
if __name__ == "__main__":
    # 修复Win7不兼容问题：仅在Win8及以上系统启用DPI感知
    if platform.system() == "Windows":
        try:
            # 检查系统版本是否 >= Win8（Win7版本号为6.1，Win8为6.2）
            import ctypes
            version = sys.getwindowsversion()
            if (version.major, version.minor) >= (6, 2):
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass  # Win7不支持则忽略
     
    root = tk.Tk()
    app = WeChatCleaner(root)
    root.mainloop()