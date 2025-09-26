import ctypes
import threading
import time
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image
 
#https://www.52pojie.cn/thread-2049231-1-1.html
def lock_screen():
    ctypes.windll.user32.LockWorkStation()
 
 
class LockScreenGuard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WinLLock")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
 
        # 状态变量
        self.is_listening = False
        self.alt_pressed = False
        self.last_alt_l_time = 0
        self.activation_delay = 2.0
 
        # 初始化UI
        self.setup_ui()
 
        # 启动监听
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.keyboard_listener.start()
        self.mouse_listener = None
 
        # 绑定最小化事件
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.tray_icon = None
        self.setup_tray_icon()
 
        self.root.mainloop()
 
    def setup_ui(self):
        self.status_var = tk.StringVar(value="当前状态: 等待ALT+L")
        status_label = ttk.Label(self.root, textvariable=self.status_var, font=("Arial", 12))
        status_label.pack(pady=20)
 
        exit_button = ttk.Button(self.root, text="退出程序", command=self.safe_exit)
        exit_button.pack(side="bottom", pady=10)
 
    def on_key_press(self, key):
        # 检测ALT键按下
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            self.alt_pressed = True
 
        # 检测L键按下且ALT已按下（ALT+L组合）
        elif self.alt_pressed and key == keyboard.KeyCode.from_char('l'):
            current_time = time.time()
 
            # 关键修改：监听状态下按ALT+L关闭监听 [4](@ref)
            if self.is_listening:
                self.stop_listening()
                return
 
            # 首次触发或超过延时窗口
            if current_time - self.last_alt_l_time > self.activation_delay:
                self.last_alt_l_time = current_time
                self.start_listening_after_delay()
 
        # 监听模式下非ALT+L的任意按键触发锁屏
        elif self.is_listening:
            self.trigger_lock()
 
    def on_key_release(self, key):
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            self.alt_pressed = False
 
    def on_mouse_move(self, x, y):
        if self.is_listening:
            self.trigger_lock()
 
    def on_mouse_click(self, x, y, button, pressed):
        if self.is_listening and pressed:
            self.trigger_lock()
 
    def start_listening_after_delay(self):
        self.status_var.set("状态: 计时2秒...")
        threading.Timer(self.activation_delay, self.activate_listening).start()
 
    def activate_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.mouse_listener = mouse.Listener(
                on_move=self.on_mouse_move,
                on_click=self.on_mouse_click
            )
            self.mouse_listener.start()
            self.status_var.set("状态: 开始 ")
 
    def stop_listening(self):
        """关闭监听状态（新增方法）[4](@ref)"""
        if self.is_listening:
            self.is_listening = False
            if self.mouse_listener:
                self.mouse_listener.stop()
            self.status_var.set("状态: 关闭")
            self.last_alt_l_time = time.time()  # 重置计时器
 
    def trigger_lock(self):
        lock_screen()
        self.stop_listening()  # 改为调用统一方法
        self.status_var.set("状态: 已关闭")
 
    def safe_exit(self):
        self.stop_listening()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
 
    def minimize_to_tray(self):
        self.root.withdraw()
        if self.tray_icon:
            self.tray_icon.update_menu()
 
    def setup_tray_icon(self):
        # 这里需要替换为你自己的图标文件路径
        image = Image.open("icon.png")
        
        self.tray_icon.run_detached()
 
    def show_window(self):
        self.root.deiconify()
 
 
if __name__ == "__main__":
    guard = LockScreenGuard()