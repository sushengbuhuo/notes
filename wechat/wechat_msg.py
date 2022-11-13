# coding=utf-8
# from __future__ import print_function
import frida
import sys
#查看撤回消息 
def on_message(message, data):
    print(message)  # 处理消息
 
 
def main(target_process):
    session = frida.attach(target_process)
    script = session.create_script("""var wechatWinAddress=Process.findModuleByName('WeChatWin.dll');
var recvMessageHookAddress = wechatWinAddress.base.add('0x4BF858'); //撤销时候会触发
Interceptor.attach(recvMessageHookAddress, {
    onEnter(args) {
        var esp = this.context.esp;
        var messageContent = Memory.readUtf16String(Memory.readPointer(esp.add("0x18")));
        var user = Memory.readUtf16String(Memory.readPointer(esp.add("0x94")));
        console.log(user+" 撤回了一条消息："+messageContent);
        send({messageContent});
    }
});
""")
    script.on('message', on_message)
    script.load()
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()

if __name__ == '__main__':
    main('WeChat.exe')# 也可以传pid，比如2个微信登陆