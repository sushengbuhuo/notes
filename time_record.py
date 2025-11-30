import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
import winsound
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
 
#https://www.52pojie.cn/thread-2069371-1-1.html
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多功能计时器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f5f7fa")
 
        # 确保中文显示正常
        self.style = ttk.Style()
        self.style.configure(".", font=("SimHei", 10))
 
        # 应用状态
        self.running = False
        self.paused = False
        self.mode = "timer"  # timer, countdown, alarm
        self.start_time = 0
        self.elapsed_time = 0
        self.target_time = 0
        self.laps = []
        self.alarm_set = False
        self.alarm_time = None
        self.time_color = "#4a6fa5"  # 默认时间颜色
 
        # 主题设置
        self.dark_mode = False
        self.borderless_mode = False
        self.sound_enabled = True
 
        # 加载配置
        self.load_config()
 
        # 创建界面
        self.create_widgets()
 
        # 绑定快捷键
        self.bind_shortcuts()
 
        # 更新显示
        self.update_display()
 
    def create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
 
        # 当前时间显示
        self.current_time_label = ttk.Label(main_frame, text="", font=("SimHei", 12, "bold"))
        self.current_time_label.pack(pady=10)
 
        # 模式选择器
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(pady=15)
 
        self.mode_buttons = {}
        modes = [("计时器", "timer"), ("倒计时", "countdown"), ("闹钟", "alarm")]
        for text, mode in modes:
            btn = ttk.Button(mode_frame, text=text, command=lambda m=mode: self.set_mode(m))
            btn.pack(side=tk.LEFT, padx=5)
            self.mode_buttons[mode] = btn
 
        # 时间显示
        self.time_display = ttk.Label(
            main_frame,
            text="00:00:00.00",
            font=("SimHei", 48, "bold"),
            foreground=self.time_color
        )
        self.time_display.pack(pady=20)
 
        # 输入区域
        self.input_frame = ttk.Frame(main_frame)
        self.input_frame.pack(pady=10, fill=tk.X)
 
        # 计时器/倒计时输入
        self.time_input_frame = ttk.Frame(self.input_frame)
        self.create_time_inputs()
 
        # 闹钟时间输入
        self.alarm_input_frame = ttk.Frame(self.input_frame)
        self.create_alarm_inputs()
 
        # 控制按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=20)
 
        self.buttons = {
            "start": ttk.Button(control_frame, text="开始 (空格)", command=self.start),
            "pause": ttk.Button(control_frame, text="暂停 (P)", command=self.pause, state=tk.DISABLED),
            "reset": ttk.Button(control_frame, text="重置 (R)", command=self.reset, state=tk.DISABLED),
            "lap": ttk.Button(control_frame, text="计次 (L)", command=self.lap, state=tk.DISABLED),
            "set": ttk.Button(control_frame, text="设置 (S)", command=self.set_time)
        }
 
        for btn in self.buttons.values():
            btn.pack(side=tk.LEFT, padx=10, ipady=5, ipadx=10)
 
        # 计次显示
        self.laps_frame = ttk.LabelFrame(main_frame, text="计次记录")
        self.laps_frame.pack(pady=10, fill=tk.BOTH, expand=True)
 
        self.laps_listbox = tk.Listbox(self.laps_frame, font=("SimHei", 10), width=50, height=5)
        self.laps_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
 
        scrollbar = ttk.Scrollbar(self.laps_frame, orient=tk.VERTICAL, command=self.laps_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.laps_listbox.config(yscrollcommand=scrollbar.set)
 
        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="设置")
        settings_frame.pack(pady=10, fill=tk.X)
 
        # 主题切换
        self.dark_mode_var = tk.BooleanVar(value=self.dark_mode)
        dark_mode_check = ttk.Checkbutton(
            settings_frame,
            text="深色模式",
            variable=self.dark_mode_var,
            command=self.toggle_dark_mode
        )
        dark_mode_check.pack(side=tk.LEFT, padx=15)
 
        # 无边框模式
        self.borderless_var = tk.BooleanVar(value=self.borderless_mode)
        borderless_check = ttk.Checkbutton(
            settings_frame,
            text="无边框模式",
            variable=self.borderless_var,
            command=self.toggle_borderless_mode
        )
        borderless_check.pack(side=tk.LEFT, padx=15)
 
        # 声音开关
        self.sound_var = tk.BooleanVar(value=self.sound_enabled)
        sound_check = ttk.Checkbutton(
            settings_frame,
            text="启用提示音",
            variable=self.sound_var,
            command=self.toggle_sound
        )
        sound_check.pack(side=tk.LEFT, padx=15)
 
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
 
        # 初始显示正确的输入框
        self.update_mode_display()
 
    def create_time_inputs(self):
        # 时、分、秒输入框
        units = [("时", "hours"), ("分", "minutes"), ("秒", "seconds")]
        self.time_inputs = {}
 
        for label, key in units:
            frame = ttk.Frame(self.time_input_frame)
            frame.pack(side=tk.LEFT, padx=10)
 
            ttk.Label(frame, text=label).pack()
            entry = ttk.Entry(frame, width=5, font=("SimHei", 14))
            entry.insert(0, "00")
            entry.pack()
            self.time_inputs[key] = entry
 
    def create_alarm_inputs(self):
        # 日期和时间输入
        self.alarm_date = ttk.Entry(self.alarm_input_frame, width=12, font=("SimHei", 12))
        self.alarm_date.pack(side=tk.LEFT, padx=10)
        self.alarm_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
 
        self.alarm_time_entry = ttk.Entry(self.alarm_input_frame, width=8, font=("SimHei", 12))
        self.alarm_time_entry.pack(side=tk.LEFT, padx=10)
        self.alarm_time_entry.insert(0, "00:00:00")
 
        ttk.Label(self.alarm_input_frame, text="格式: YYYY-MM-DD 和 HH:MM:SS").pack(side=tk.LEFT, padx=10)
 
    def set_mode(self, mode):
        self.mode = mode
        self.reset()
 
        # 更新按钮状态
        for m, btn in self.mode_buttons.items():
            if m == mode:
                btn.config(style="Accent.TButton")
            else:
                btn.config(style="TButton")
 
        self.update_mode_display()
        self.status_var.set(f"已切换到{mode}模式")
 
    def update_mode_display(self):
        # 隐藏所有输入框
        self.time_input_frame.pack_forget()
        self.alarm_input_frame.pack_forget()
 
        # 根据模式显示相应的输入框
        if self.mode in ["timer", "countdown"]:
            self.time_input_frame.pack(fill=tk.X)
            if self.mode == "timer":
                self.time_display.config(text="00:00:00.00")
                self.status_var.set("计时器模式 - 按开始按钮启动")
            else:
                self.status_var.set("倒计时模式 - 设置时间后按开始")
        elif self.mode == "alarm":
            self.alarm_input_frame.pack(fill=tk.X)
            self.status_var.set("闹钟模式 - 设置时间后按开始")
 
    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
 
            if self.mode == "timer":
                if self.elapsed_time == 0:
                    self.start_time = time.time()
                else:
                    self.start_time = time.time() - self.elapsed_time
                self.status_var.set("计时器运行中...")
 
            elif self.mode == "countdown":
                if self.target_time == 0:
                    self.set_time()
 
                if self.target_time > 0:
                    self.start_time = time.time()
                    self.status_var.set("倒计时运行中...")
 
            elif self.mode == "alarm":
                if not self.alarm_set:
                    self.set_time()
 
                if self.alarm_set:
                    self.status_var.set(f"闹钟已设置 - {self.alarm_time.strftime('%Y-%m-%d %H:%M:%S')}")
 
            # 更新按钮状态
            self.buttons["start"]["state"] = tk.DISABLED
            self.buttons["pause"]["state"] = tk.NORMAL
            self.buttons["reset"]["state"] = tk.NORMAL
            self.buttons["lap"]["state"] = tk.NORMAL if self.mode == "timer" else tk.DISABLED
 
            # 启动计时线程
            threading.Thread(target=self.run_timer, daemon=True).start()
 
    def pause(self):
        if self.running and not self.paused:
            self.paused = True
            self.running = False
 
            if self.mode == "timer":
                self.elapsed_time = time.time() - self.start_time
                self.status_var.set("计时器已暂停")
            elif self.mode == "countdown":
                self.elapsed_time = time.time() - self.start_time
                self.target_time -= self.elapsed_time
                self.start_time = 0
                self.status_var.set("倒计时已暂停")
 
            # 更新按钮状态
            self.buttons["start"]["state"] = tk.NORMAL
            self.buttons["pause"]["state"] = tk.DISABLED
 
    def reset(self):
        self.running = False
        self.paused = False
        self.elapsed_time = 0
        self.target_time = 0
        self.start_time = 0
        self.laps = []
        self.alarm_set = False
        self.alarm_time = None
 
        self.laps_listbox.delete(0, tk.END)
        self.time_display.config(text="00:00:00.00", foreground=self.time_color)
 
        # 更新按钮状态
        self.buttons["start"]["state"] = tk.NORMAL
        self.buttons["pause"]["state"] = tk.DISABLED
        self.buttons["reset"]["state"] = tk.DISABLED
        self.buttons["lap"]["state"] = tk.DISABLED
 
        self.status_var.set(f"{self.mode}已重置")
 
    def lap(self):
        if self.mode == "timer" and self.running:
            current_time = time.time() - self.start_time
            lap_time = current_time - sum(self.laps) if self.laps else current_time
            self.laps.append(lap_time)
 
            # 格式化时间
            total_str = self.format_time(current_time)
            lap_str = self.format_time(lap_time)
 
            # 添加到列表
            lap_num = len(self.laps)
            self.laps_listbox.insert(tk.END, f"计次 {lap_num}: 总时间 {total_str} | 本次 {lap_str}")
            self.laps_listbox.see(tk.END)
 
            self.status_var.set(f"已记录第 {lap_num} 次计次")
 
    def set_time(self):
        if self.mode in ["timer", "countdown"]:
            try:
                hours = int(self.time_inputs["hours"].get() or 0)
                minutes = int(self.time_inputs["minutes"].get() or 0)
                seconds = int(self.time_inputs["seconds"].get() or 0)
 
                total_seconds = hours * 3600 + minutes * 60 + seconds
 
                if self.mode == "countdown":
                    self.target_time = total_seconds
                    self.time_display.config(text=self.format_time(total_seconds))
                    self.status_var.set(f"倒计时已设置为 {self.format_time(total_seconds)}")
                else:
                    self.elapsed_time = total_seconds
                    self.time_display.config(text=self.format_time(total_seconds))
                    self.status_var.set(f"计时器已设置为 {self.format_time(total_seconds)}")
 
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的数字")
 
        elif self.mode == "alarm":
            try:
                date_str = self.alarm_date.get()
                time_str = self.alarm_time_entry.get()
                datetime_str = f"{date_str} {time_str}"
                self.alarm_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
 
                now = datetime.now()
                if self.alarm_time <= now:
                    messagebox.showwarning("时间错误", "请设置一个未来的时间")
                    return
 
                self.alarm_set = True
                self.time_display.config(text=self.alarm_time.strftime("%Y-%m-%d %H:%M:%S"))
                self.status_var.set(f"闹钟已设置为 {datetime_str}")
 
            except ValueError:
                messagebox.showerror("输入错误", "请使用正确的格式 (YYYY-MM-DD HH:MM:SS)")
 
    def run_timer(self):
        while self.running:
            if self.mode == "timer":
                current_time = time.time() - self.start_time
                self.time_display.config(text=self.format_time(current_time))
 
            elif self.mode == "countdown":
                elapsed = time.time() - self.start_time
                remaining = self.target_time - elapsed
 
                if remaining <= 0:
                    self.time_display.config(text="00:00:00.00", foreground="#e74c3c")
                    self.running = False
                    self.status_var.set("倒计时结束!")
 
                    # 播放提示音
                    if self.sound_enabled:
                        self.play_alert()
 
                    # 更新按钮状态
                    self.root.after(0, lambda: self.buttons["start"].config(state=tk.NORMAL))
                    self.root.after(0, lambda: self.buttons["pause"].config(state=tk.DISABLED))
                    break
 
                # 最后10秒变红
                if remaining <= 10:
                    self.time_display.config(foreground="#e74c3c")
                else:
                    self.time_display.config(foreground=self.time_color)
 
                self.time_display.config(text=self.format_time(remaining))
 
            elif self.mode == "alarm" and self.alarm_set:
                now = datetime.now()
                if now >= self.alarm_time:
                    self.running = False
                    self.status_var.set("闹钟响了!")
 
                    # 播放提示音
                    if self.sound_enabled:
                        self.play_alert(repeat=True)
 
                    # 显示提示
                    self.root.after(0, lambda: messagebox.showinfo("闹钟", "时间到了!"))
 
                    # 更新按钮状态
                    self.root.after(0, lambda: self.buttons["start"].config(state=tk.NORMAL))
                    self.root.after(0, lambda: self.buttons["pause"].config(state=tk.DISABLED))
                    break
 
                # 显示剩余时间
                remaining = self.alarm_time - now
                self.time_display.config(text=self.format_timedelta(remaining))
 
            time.sleep(0.01)
 
    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds - int(seconds)) * 100)
 
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:02d}"
 
    def format_timedelta(self, delta):
        total_seconds = delta.total_seconds()
        return self.format_time(total_seconds)
 
    def update_display(self):
        # 更新当前时间
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.current_time_label.config(text=now)
 
        # 检查闹钟（即使未运行也检查）
        if self.mode == "alarm" and self.alarm_set and not self.running:
            now = datetime.now()
            if now >= self.alarm_time:
                self.status_var.set("闹钟响了!")
                if self.sound_enabled:
                    self.play_alert(repeat=True)
                messagebox.showinfo("闹钟", "时间到了!")
                self.alarm_set = False
 
        # 继续更新
        self.root.after(1000, self.update_display)
 
    def play_alert(self, repeat=False):
        try:
            if repeat:
                # 重复播放5次
                for _ in range(5):
                    winsound.Beep(1000, 500)
                    time.sleep(0.5)
            else:
                winsound.Beep(1000, 1000)
        except:
            pass  # 忽略声音播放错误
 
    def toggle_dark_mode(self):
        self.dark_mode = self.dark_mode_var.get()
        self.apply_theme()
        self.save_config()
 
    def toggle_borderless_mode(self):
        self.borderless_mode = self.borderless_var.get()
        self.root.overrideredirect(self.borderless_mode)
        self.save_config()
 
    def toggle_sound(self):
        self.sound_enabled = self.sound_var.get()
        self.status_var.set(f"提示音已{'启用' if self.sound_enabled else '禁用'}")
        self.save_config()
 
    def apply_theme(self):
        if self.dark_mode:
            self.root.configure(bg="#2c3e50")
            self.time_display.config(foreground="#3498db")
            self.time_color = "#3498db"
            self.style.configure(".", background="#2c3e50", foreground="#ecf0f1")
            self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1")
            self.style.configure("TButton", background="#34495e", foreground="#ecf0f1")
            self.style.configure("Accent.TButton", background="#3498db", foreground="#ffffff")
            self.laps_listbox.configure(bg="#34495e", fg="#ecf0f1", selectbackground="#3498db")
        else:
            self.root.configure(bg="#f5f7fa")
            self.time_display.config(foreground="#4a6fa5")
            self.time_color = "#4a6fa5"
            self.style.configure(".", background="#f5f7fa", foreground="#333333")
            self.style.configure("TLabel", background="#f5f7fa", foreground="#333333")
            self.style.configure("TButton", background="#e0e0e0", foreground="#333333")
            self.style.configure("Accent.TButton", background="#4a6fa5", foreground="#ffffff")
            self.laps_listbox.configure(bg="#ffffff", fg="#333333", selectbackground="#4a6fa5")
 
        # 更新模式按钮样式
        for m, btn in self.mode_buttons.items():
            if m == self.mode:
                btn.config(style="Accent.TButton")
            else:
                btn.config(style="TButton")
 
    def bind_shortcuts(self):
        self.root.bind("<space>", lambda e: self.start() if not self.running else self.pause())
        self.root.bind("r", lambda e: self.reset() if self.buttons["reset"]["state"] == tk.NORMAL else None)
        self.root.bind("l", lambda e: self.lap() if self.buttons["lap"]["state"] == tk.NORMAL else None)
        self.root.bind("s", lambda e: self.set_time())
        self.root.bind("t", lambda e: self.set_mode("timer"))
        self.root.bind("c", lambda e: self.set_mode("countdown"))
        self.root.bind("a", lambda e: self.set_mode("alarm"))
        self.root.bind("<Escape>", lambda e: self.root.quit() if self.borderless_mode else None)
 
    def load_config(self):
        try:
            config_path = Path.home() / ".timer_config.json"
            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
                    self.dark_mode = config.get("dark_mode", False)
                    self.borderless_mode = config.get("borderless_mode", False)
                    self.sound_enabled = config.get("sound_enabled", True)
 
                    # 应用无边框模式
                    self.root.overrideredirect(self.borderless_mode)
 
                    # 应用主题
                    self.apply_theme()
        except:
            pass  # 使用默认设置
 
    def save_config(self):
        try:
            config = {
                "dark_mode": self.dark_mode,
                "borderless_mode": self.borderless_mode,
                "sound_enabled": self.sound_enabled
            }
            config_path = Path.home() / ".timer_config.json"
            with open(config_path, "w") as f:
                json.dump(config, f)
        except:
            pass  # 忽略保存错误
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()