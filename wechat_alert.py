import uiautomation as auto
import pygetwindow as pw
from winotify import Notification
import os
import time
import re
import json

# 聊天记录、pid文件存放位置，自行修改。 https://www.52pojie.cn/thread-2072706-1-1.html
dataDir = f'C:\\Users\evans\Desktop\dist'
records_path = f'{dataDir}\\chat-records'
pid_path = f'{dataDir}\\wechat.pid'
icon_path =f'{dataDir}\\wechat.png'
black_list = "服务号,公众号,文件传输助手,折叠的聊天,微信支付,服务通知"

auto.SetGlobalSearchTimeout(1)

def read_message():
    """
    查找微信消息列表
    """
    # 查找微信主 XView
    wx = auto.Control(searchDepth=10, ClassName='mmui::XView')
    show = wx.Exists(0)
    if not show:
        print("需要将微信打开在任务栏，可最小化但不能关闭窗口")
        return

    # 查找会话列表 XTableView
    sessions = wx.ListControl(Name="会话", searchDepth=10)
    show = sessions.Exists()
    if not show:
        return

    # 提取所有会话列表名
    sessionNames = [
        child.Name for child in sessions.GetChildren()
        if child.ControlTypeName == 'ListItemControl' and child.ClassName == 'mmui::ChatSessionCell'
    ]

    message_handle(sessionNames)

def message_handle(sessions):
    """
    微信消息处理
    """
    for full_name in sessions:
        session = parse_chat_name_flexible(full_name)
        if not session:
            continue    

        account = session["user"]
        message = session["msg"]
        unread = session["unread"].replace('条未读', '')
        unread = "99+" if len(unread) > 2 else unread

        # 聊天历史
        chat_records = load_records()

        if account in chat_records:
            if chat_records[account] == message:
                continue

        # 黑名单处理，但还是要处理成已读
        if account in black_list.split(","):
            chat_records[account] = message
            write_records(chat_records)
            continue

        # 过滤免打扰的消息，但还是要处理成已读
        if "消息免打扰" in session["time"] :
            chat_records[account] = message
            write_records(chat_records)
            continue

        # 微信在前台活动则不提醒，但还是要处理成已读
        title = pw.getActiveWindow().title
        if "微信" in title:
            chat_records[account] = message
            write_records(chat_records)
            continue   

        # 弹窗提醒
        notification_title = f"{account}({unread})" if len(unread) > 0 else account
        notification_message = message[0:15] + "..." if len(message) > 15 else message

        notify = Notification(
            app_id="微信",
            title=f"{notification_title}",
            msg=f"{notification_message}",
            icon=f"{icon_path}"
        )

        notify.show()
        chat_records[account] = message
        write_records(chat_records)
        break

def parse_chat_name_flexible(raw_name: str):
    """
    解析微信消息
    """

    # 去掉已置顶关键字
    raw_name = re.sub(r'已置顶\s', '', raw_name)

    parts = raw_name.split()
    if len(parts) < 2:
        return None

    user = parts[0]
    unread = ""
    time_str = ""

    start_idx = 1

    # 查找未读条数
    for i in range(start_idx, min(start_idx + 2, len(parts))):
        if "条未读" in parts[i]:
            unread = parts[i]
            start_idx = i + 1
            break

    # 查找时间
    for i in range(len(parts) - 1, start_idx - 1, -1):
        if ':' in parts[i] or '/' in parts[i] or '星期' in parts[i]:
            time_str = parts[i]
            end_idx = i
            break
        else:
            end_idx = len(parts)

    msg_parts = parts[start_idx:end_idx]
    msg = " ".join(msg_parts)

    # 清理发送人里的 [n条]
    msg_content = re.sub(r'\[\d+条\]', '', msg).strip()

    return {
        "user": user.strip(),
        "unread": unread.strip(),
        "msg": msg_content.strip(),
        "time": time_str.strip()
    }

#载入历史聊天记录
def load_records():
    try:
        with open(records_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        chat_records = {}
        write_records(chat_records)

# 写入最新一条聊天记录，避免重复提醒
def write_records(content):
    with open(records_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

def load_pid():
    with open(pid_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_pid(pid):
    with open(pid_path, 'w', encoding='utf-8') as file:
        file.write(str(pid)) 

# 防止启动多个python进程
def reset_pid():
    try:
      pid = load_pid()
      if len(pid) > 0:
        os.kill(int(pid), 9)
    except Exception:
      pass

    pid = os.getpid()
    write_pid(pid)
    return pid

def start():
    pid = reset_pid()
    while True:
        try:
          read_message()
          #2秒检测一次UI组件
          time.sleep(2)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    start()
