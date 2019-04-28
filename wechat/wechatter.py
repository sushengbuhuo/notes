#! /usr/bin/env python   
# -*- coding: utf-8 -*
import itchat
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time,threading

#----------status check 微信聊天机器人https://github.com/Yzstr/WeChatter/blob/master/WeChatter.py----------#
task_list = [("00:01", "I'm stay'in alive")]

def  task_remind():
    for task in task_list:
        task_time = task[0]
        task_content = task[1]
        if datetime.datetime.now().strftime("%H:%M") == task_time:
           
            receiver = itchat.search_friends(name="Yzstr")[0]["UserName"]
            itchat.send_msg(task_content, receiver)

def remind_run():
    sched = BlockingScheduler()
    sched.add_job(task_remind, 'cron', second=0)
    sched.start()
#--------------------------------#


#------------chat bot------------# 
# answer by userId
userId = ''

# get friends' message
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE])
def text_reply(msg):
    # let ice answer
    global userId
    userId = msg['FromUserName']
    xbAnswer(msg)
    # print(getUserNickName(msg) + "send:\n" + getText(msg))

# group message
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE], isGroupChat = True)
def group_reply(msg):
    fromUserName = msg['FromUserName']
    group = itchat.search_chatrooms(userName=fromUserName)
    # print(group['NickName'] + "group " + msg['ActualNickName'] + " message:\n" + getText(msg) )

    if msg['isAt'] == True :
        global userId
        userId = msg['FromUserName']
        xbAnswer(msg)

# group message
@itchat.msg_register(itchat.content.PICTURE, isGroupChat = True)
def group_pic(msg):
    msg['Text'](msg['FileName'])
    itchat.send_image(msg['FileName'])

# mp message
@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE], isMpChat = True)
def map_reply(msg):
    text = getText(msg)
    global userId
    if msg['Type'] == 'Picture':
        msg['Text'](msg['FileName'])
        itchat.send_image(msg['FileName'],userId)
        # itchat.send_msg(' ', userId)
    else:
        itchat.send_msg(text + " ", userId)
        receiver = itchat.search_friends(name=u"Yzstr")[0]["UserName"]
        itchat.send_msg(text+"\n----------\nauto reply", receiver)

# get name
def getUserNickName(msg):
    fromUserName = msg['FromUserName']
    fromUser = itchat.search_friends(userName=fromUserName)
    nickName = fromUser['NickName']
    return nickName

# get text
def getText(msg):
    if msg['Type'] == 'Text':
        return msg['Text']
    else:
        return " type failed "

# ask ice
def xbAnswer(msg):
    xb = itchat.search_mps(name=u'小冰')[0]
    quest = getText(msg)
    if msg['Type'] == 'Picture':
        msg['Text'](msg['FileName'])
        itchat.send_image(msg['FileName'],xb['UserName'])
    else:
        receiver = itchat.search_friends(name=u"Yzstr")[0]["UserName"]
        # target=itchat.search_friends(userName='xb['UserName']')
        itchat.send_msg(quest+"\n----------\nsend by "+getUserNickName(msg), receiver)
        itchat.send_msg(quest, xb['UserName'])
#--------------------------------#

#----------making threads--------#
t1=threading.Thread(target=itchat.run,name='itchat')
t2=threading.Thread(target=remind_run,name='remind')
#--------------------------------#

if __name__=='__main__':
    itchat.auto_login(hotReload=True,enableCmdQR=0)    
    t1.start()  
    t2.start()
