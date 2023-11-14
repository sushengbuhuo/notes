import win32gui
import win32api
import win32con
import time
import win32clipboard
import pyperclip
import pyautogui
 
#打开微信程序
win32api.ShellExecute(0, 'open', r'D:\WeChat\WeChat.exe', '', '', 1)
#获取微信主窗口句柄
win = win32gui.FindWindow(None, '微信')
title=win32gui.GetWindowText(win)
print(f'找到{title}主窗口句柄:{win}')
 
#设置和粘贴剪贴板
def ClipboardText(aString):
        #设置剪贴板
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, aString)
        win32clipboard.CloseClipboard()
        time.sleep(1)
        #将剪贴板文本进行粘贴
        win32api.keybd_event(win32con.VK_CONTROL,0,0,0)  #ctrl键位码是17
        win32api.keybd_event(ord('V'),0,0,0)  #v键位码是86
        win32api.keybd_event(win32con.VK_CONTROL,0,win32con.KEYEVENTF_KEYUP,0) #释放CTRL按键
        win32api.keybd_event(ord('V'),0,win32con.KEYEVENTF_KEYUP,0)#释放V键
 
 
#搜索微信好友或者微信群
def search(wxname):
        if win != 0:
                win32gui.SetForegroundWindow(win) # 获取控制     
                # 模拟按下Ctrl+F快捷键,ctrl+f搜索
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                win32api.keybd_event(ord('F'), 0, 0, 0)
                win32api.keybd_event(ord('F'), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                ClipboardText(wxname)
                time.sleep(1)
                # 模拟按下Enter键
                win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
                win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        else:
                # 模拟按下Enter键
                print(f'请注意：找不到【{wxname}】这个人（或群）！')
                exit()
 
#模拟发送动作,alt+s键发送
def SendMsg():
        win32api.keybd_event(win32con.VK_MENU, 0, 0, 0) #Alt键位码18,win32con.VK_MENU键位码代表ALT键
        win32api.keybd_event(ord('S'),0,0,0) #s键位码83
        win32api.keybd_event(win32con.VK_MENU,0,win32con.KEYEVENTF_KEYUP,0) #释放ALT按键
        win32api.keybd_event(ord('S'),0,win32con.KEYEVENTF_KEYUP,0)#释放S按键
 
#发送文本
def sendText(chatrooms,text):
        for chatroom in chatrooms:
                search(chatroom)
                #文字首行留空，防止带表情复制不完全
                ClipboardText(" "+text)
                SendMsg()
                print(f'微信消息:{text} 已发送至:{chatroom}')
 
 
# 使用示例
chatrooms = ['微信群名字', '文件传输助手']
text='微信自动发信息....'
 
sendText(chatrooms,text)