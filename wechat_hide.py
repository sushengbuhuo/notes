import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import ctypes
from ctypes import wintypes
import win32gui
import win32con
from pynput.keyboard import Controller, Key
from PIL import Image, ImageTk
import pystray
import sys
import os
# 全局互斥锁名称
MUTEX_NAME = "WeChatAutoLockTool_Mutex"
# 定义获取系统空闲时间的函数
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_uint)]
def get_idle_duration():
    last_input_info = LASTINPUTINFO()
    last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info))
    current_tick = ctypes.windll.kernel32.GetTickCount()
    return (current_tick - last_input_info.dwTime) / 1000.0
# 定义激活目标窗口的函数
def activate_target_window(class_name):
    hwnd = win32gui.FindWindow(class_name, None)
    if hwnd:
        # 移除透明样式（如果存在）
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if ex_style & win32con.WS_EX_LAYERED:
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style & ~win32con.WS_EX_LAYERED)
         
        # 激活并前置窗口
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
         
        # 强制重绘窗口
        win32gui.RedrawWindow(hwnd, None, None,
                              win32con.RDW_ERASE | win32con.RDW_FRAME | win32con.RDW_INVALIDATE)
        return hwnd  # 返回窗口句柄
    return 0  # 返回0表示未找到窗口
# 定义发送快捷键的函数
def send_ctrl_l():
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press('l')
    keyboard.release('l')
    keyboard.release(Key.ctrl)
    
class IdleMonitorApp:
    def __init__(self, root):
        # ==== 单实例检查 ====
        self.mutex = ctypes.windll.kernel32.CreateMutexW(None, False, MUTEX_NAME)
        last_error = ctypes.windll.kernel32.GetLastError()
         
        # 检测到已有实例运行时
        if last_error == 183:  # ERROR_ALREADY_EXISTS
            self.create_already_running_ui(root)
            return  # 不再继续初始化
         
        # ==== 原有初始化代码 ====
        self.root = root
        self.root.title("微信自动锁定工具")
        self.root.geometry("650x460")  # 增大窗口高度以容纳新控件
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        # 尝试加载图标
        try:
            myicon_path = os.path.join(os.path.dirname(__file__), "myicon.ico")
            self.root.iconbitmap(myicon_path)
        except:
            pass  # 如果找不到图标则忽略
         
        # 监控状态变量
        self.monitoring = False
        self.stop_event = threading.Event()
        self.idle_threshold_sec = 600  # 默认监控时间600秒
        self.target_window_class = "Qt51514QWindowIcon"  # 默认监控微信窗口
        self.time_lock = threading.Lock()  # 用于线程安全更新阈值
         
        # 创建托盘图标
        self.tray_icon = None
        self.tray_thread = None
         
        # 创建界面
        self.create_widgets()
         
        # 初始状态
        self.update_status("就绪 - 等待启动监控")
         
        # 创建托盘图标
        self.create_tray_icon()
    
    def create_already_running_ui(self, root):
        """创建程序已运行的提示界面"""
        root.title("程序已运行")
        root.geometry("370x200")
        root.resizable(False, False)
         
        # 设置窗口图标
        try:
            myicon_path = os.path.join(os.path.dirname(__file__), "myicon.ico")
            root.iconbitmap(myicon_path)
        except:
            pass
         
        # 主容器框架
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
         
        # 创建警告图标
        warning_icon = tk.Label(main_frame, text="&#9888;", font=("Arial", 24), foreground="orange")
        warning_icon.pack(pady=(0, 15))
         
        # 创建提示标签
        label = ttk.Label(main_frame, text="微信自动锁定工具已在运行中！", font=("Arial", 11))
        label.pack()
         
        # 创建详细说明标签
        detail = ttk.Label(main_frame, text="请检查系统托盘图标或使用任务管理器查看运行中的程序",
                          foreground="gray", wraplength=350)
        detail.pack(pady=(5, 15))
         
        # 创建确定按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
         
        button = ttk.Button(button_frame, text="确定", width=15, command=root.destroy)
        button.pack()
         
        # 窗口居中显示
        self.center_window(root)
    
    def center_window(self, window):
        """使窗口居中显示"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        # 状态标签
        status_frame = ttk.Frame(self.root, padding=10)
        status_frame.pack(fill=tk.X)
         
        self.waPojie_var = tk.StringVar(value="")
        self.waPojie = ttk.Label(status_frame, textvariable=self.waPojie_var,
                                    font=("Arial", 10, "bold"), foreground="red")
        self.waPojie.pack(side=tk.RIGHT, padx=10)
        ttk.Label(status_frame, text="当前状态:").pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="就绪 - 等待启动监控")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                    font=("Arial", 10, "bold"), foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=10)
         
        # 监控时间设置框架
        threshold_frame = ttk.LabelFrame(self.root, text="监控时间设置", padding=10)
        threshold_frame.pack(fill=tk.X, padx=10, pady=5)
         
        ttk.Label(threshold_frame, text="空闲时间阈值(秒):").grid(row=0, column=0, padx=5, sticky=tk.W)
         
        # 使用IntVar绑定输入框值
        self.threshold_var = tk.IntVar(value=self.idle_threshold_sec)
        self.threshold_entry = ttk.Entry(threshold_frame, textvariable=self.threshold_var, width=8)
        self.threshold_entry.grid(row=0, column=1, padx=5)
         
        # 设置按钮
        set_btn = ttk.Button(threshold_frame, text="设置", command=self.set_threshold)
        set_btn.grid(row=0, column=2, padx=10)
         
        # 添加输入验证，只允许输入数字
        validate_cmd = (self.root.register(self.validate_number), '%P')
        self.threshold_entry.config(validate="key", validatecommand=validate_cmd)
         
        # 当前设置显示
        ttk.Label(threshold_frame, text="当前设置:").grid(row=0, column=3, padx=(20, 5))
        self.cur_threshold_var = tk.StringVar(value=f"{self.idle_threshold_sec}秒")
        ttk.Label(threshold_frame, textvariable=self.cur_threshold_var,
                 font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)
         
        # 目标窗口设置区域
        window_frame = ttk.LabelFrame(self.root, text="目标窗口设置", padding=10)
        window_frame.pack(fill=tk.X, padx=10, pady=5)
         
        ttk.Label(window_frame, text="窗口类名:").grid(row=0, column=0, padx=5, sticky=tk.W)
         
        # 窗口类名输入框
        self.window_class_var = tk.StringVar(value=self.target_window_class)
        self.class_entry = ttk.Entry(window_frame, textvariable=self.window_class_var, width=25)
        self.class_entry.grid(row=0, column=1, padx=5, sticky=tk.W)
         
        # 测试按钮
        test_btn = ttk.Button(window_frame, text="测试窗口", command=self.test_window_class)
        test_btn.grid(row=0, column=2, padx=10)
         
        # 当前设置显示
        ttk.Label(window_frame, text="当前监控:").grid(row=0, column=3, padx=(20, 5))
        self.cur_window_var = tk.StringVar(value=self.target_window_class)
        ttk.Label(window_frame, textvariable=self.cur_window_var,
                 font=("Arial", 9)).grid(row=0, column=4, padx=5, sticky=tk.W)
         
        # 空闲时间显示
        idle_frame = ttk.Frame(self.root, padding=10)
        idle_frame.pack(fill=tk.X, padx=10)
         
        ttk.Label(idle_frame, text="系统空闲时间:").pack(side=tk.LEFT)
        self.idle_var = tk.StringVar(value="0 秒")
        ttk.Label(idle_frame, textvariable=self.idle_var,
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
         
        # 控制按钮
        btn_frame = ttk.Frame(self.root, padding=20)
        btn_frame.pack(fill=tk.X)
         
        self.start_btn = ttk.Button(btn_frame, text="启动监控",
                                  command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=10)
         
        self.stop_btn = ttk.Button(btn_frame, text="停止监控",
                                 command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
         
        self.licen_btn = ttk.Button(btn_frame, text="检测窗口名",
                                 command=self.print_all_windows)
        self.licen_btn.pack(side=tk.LEFT, padx=10)
         
        # 日志区域
        log_frame = ttk.LabelFrame(self.root, text="操作日志", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
         
        self.log_text = tk.Text(log_frame, height=8, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
         
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
    # 检测窗口
    def print_all_windows(self):
        self.add_log("正在扫描系统窗口...")
        self.add_log("{:<15} {:<40} {:<30}".format("句柄(Hex)", "窗口标题", "类名"))
        self.add_log("-" * 85, raw=True)  # 使用raw参数避免时间戳
        def enum_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)[:50]
                class_name = win32gui.GetClassName(hwnd)
                log_line = f"0x{hwnd:08X} | {title:<40} | {class_name:<30}"
                self.add_log(log_line, raw=True)
        win32gui.EnumWindows(enum_callback, None)
        self.add_log("\n提示：请从上述列表中找到微信窗口的【类名】或【标题】")
    # 输入验证函数，确保只输入数字
    def validate_number(self, new_value):
        if new_value == "":
            return True
        try:
            int(new_value)
            return True
        except ValueError:
            return False
    
    # 设置新的监控时间阈值
    def set_threshold(self):
        new_threshold = self.threshold_var.get()
        if new_threshold <= 0:
            messagebox.showerror("错误", "监控时间必须大于0秒")
            return
         
        with self.time_lock:
            self.idle_threshold_sec = new_threshold
            self.cur_threshold_var.set(f"{new_threshold}秒")
         
        self.add_log(f"监控时间已设置为: {new_threshold}秒")
    
    # 查找类名
    def test_window_class(self):
        class_name = self.window_class_var.get().strip()
        if not class_name:
            messagebox.showerror("错误", "请输入窗口类名")
            return
         
        hwnd = win32gui.FindWindow(class_name, None)
        if hwnd:
            self.target_window_class = class_name
            self.cur_window_var.set(class_name)
            messagebox.showinfo("成功", f"找到窗口类名: {class_name}")
            self.add_log(f"窗口类名已设置为: {class_name}")
        else:
            messagebox.showerror("错误", f"未找到类名为 {class_name} 的窗口")
    
    def create_tray_icon(self):
        # 创建托盘图标（内存中生成）
        image = Image.new('RGB', (64, 64), color=(70, 130, 180))
        self.tray_image = image
         
        # 托盘菜单
        menu = (pystray.MenuItem('显示窗口', self.show_window),
                pystray.MenuItem('退出', self.quit_app))
         
        self.tray_icon = pystray.Icon("idle_monitor", self.tray_image,
                                     "窗口自动激活工具", menu)
         
        # 在独立线程中运行托盘图标
        self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        self.tray_thread.start()
    
    def update_status(self, message):
        self.status_var.set(message)
        self.add_log(message)
    
    def add_log(self, message, raw=False):
        self.log_text.config(state=tk.NORMAL)
        if raw:
            self.log_text.insert(tk.END, message + "\n")
        else:
            self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def start_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.stop_event.clear()
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
             
            # 启动监控线程
            self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.monitor_thread.start()
             
            self.update_status("监控已启动 - 检测系统空闲状态中...")
    
    def stop_monitoring(self):
        if self.monitoring:
            self.monitoring = False
            self.stop_event.set()
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.update_status("监控已停止")
    
    def monitor_loop(self):
        self.update_status("监控运行中 - 当检测到无操作后将激活目标窗口并最小化")
         
        while self.monitoring and not self.stop_event.is_set():
            # 获取当前阈值（线程安全）
            with self.time_lock:
                current_threshold = self.idle_threshold_sec
             
            idle_seconds = get_idle_duration()
            self.idle_var.set(f"{int(idle_seconds)} 秒")
             
            if idle_seconds >= current_threshold:
                self.update_status(f"检测到系统空闲超过{current_threshold}秒，激活目标窗口...")
                
                # 获取窗口句柄
                hwnd = activate_target_window(self.target_window_class)
                
                if hwnd:  # 判断句柄有效性
                    self.update_status("目标窗口已激活，正在发送Ctrl+L快捷键...")
                    time.sleep(1)  # 等待窗口激活
                    send_ctrl_l()
                     
                    # 发送快捷键后最小化窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    self.update_status("快捷键已发送，窗口已最小化")
                else:
                    self.update_status(f"未找到类名为 {self.target_window_class} 的窗口")
             
            # 每10秒检查一次，但检查停止标志更频繁
            for _ in range(50):
                if self.stop_event.is_set():
                    break
                time.sleep(0.2)
    
    def minimize_to_tray(self):
        self.root.withdraw()
        self.update_status("程序已最小化到系统托盘")
    
    def show_window(self, icon=None, item=None):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.update_status("窗口已从托盘恢复")
    
    def quit_app(self, icon=None, item=None):
        self.stop_monitoring()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
        os._exit(0)
if __name__ == "__main__":
    root = tk.Tk()
    app = IdleMonitorApp(root)
    
    if hasattr(app, 'mutex') and ctypes.windll.kernel32.GetLastError() != 183:
        root.mainloop()