import winreg
import tkinter as tk
from tkinter import messagebox, ttk
  
def set_registry_value():
    key_path = r"SOFTWARE\Microsoft\WindowsUpdate\UX\Settings"
    value_name = "FlightSettingsMaxPauseDays"
    value_data = 36500
     
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
            messagebox.showinfo(" 成功", "注册表值设置成功！\n\n请打开Windows设置→更新与安全→Windows更新→暂停更新\n在此处设置最大暂停周数。\n\n注意：由于周数较多，设置时可能会卡顿，请耐心等待。")
             
    except WindowsError as e:
        if e.winerror  == 2:
            try:
                with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value_data)
                    messagebox.showinfo(" 成功", "注册表键和值创建成功！\n\n请打开Windows设置→更新与安全→Windows更新→暂停更新\n在此处设置最大暂停周数。\n\n注意：由于周数较多，设置时可能会卡顿，请耐心等待。")
            except WindowsError as e:
                messagebox.showerror(" 错误", f"创建键失败: {e}\n\n请以管理员权限运行此程序")
        elif e.winerror  == 5:
            messagebox.showerror(" 错误", "权限不足，请以管理员身份运行此程序")
        else:
            messagebox.showerror(" 错误", f"操作失败: {e}")
  
def create_ui():
    root = tk.Tk()
    root.title("Windows 更新暂停设置工具")
    root.geometry("500x500") 
     
    try:
        root.iconbitmap(default='system.ico')
    except:
        pass
     
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(expand=True,  fill=tk.BOTH)
    title_label = ttk.Label(main_frame, text="Windows更新暂停设置工具", font=('Arial', 14, 'bold'))
    title_label.pack(pady=10) 
     
    # 说明文本  https://www.52pojie.cn/thread-2045638-1-1.html
    info_text = """此工具将修改注册表，允许您设置更长的Windows更新暂停时间。
  
操作步骤：
1. 点击下方"设置注册表"按钮
2. 成功后，打开Windows设置 
3. 转到"更新与安全"→"Windows更新"
4. 点击"暂停更新"设置最大暂停周数 
  
注意：
- 需要管理员权限运行 
- 设置大量周数时可能会卡顿，请耐心等待
- 36500天≈100年（最大值)
"""
    info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT)
    info_label.pack(pady=10,  padx=10, anchor=tk.W)
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=20) 
    set_btn = ttk.Button(btn_frame, text="设置注册表", command=set_registry_value)
    set_btn.pack(side=tk.LEFT,  padx=10)
    exit_btn = ttk.Button(btn_frame, text="退出", command=root.destroy) 
    exit_btn.pack(side=tk.LEFT,  padx=10)
    copyright_label = ttk.Label(main_frame, text="2025 Windows更新管理工具", foreground="gray")
    copyright_label.pack(side=tk.BOTTOM,  pady=5)
    root.mainloop() 
  
if __name__ == "__main__":
    create_ui()