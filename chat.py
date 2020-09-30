import requests
import time

question = input("请开始你们的表演：") # 输入问题开始表演
#http://www.justdopython.com/2020/05/20/Python_Twoai_chat/
girl = "小姐姐"
boy = "小哥哥"

print(boy+':'+question)

while True:
    boy_data = {
       "key": "9fd874929409453991db78f8b46a446b",
       "info": question,      #构建发送的数据
       "userid": "622952"
    }
    boy_url = 'http://www.tuling123.com/openapi/api'
    boy_content = requests.post(boy_url, data=boy_data)    #发送请求数据
    print(boy + ':' + eval(boy_content.text)["text"])  # 用eval函数处理一下图灵返回的消息
    question = eval(boy_content.text)["text"]

    girl_data = {
        "question": question,  # 构建发送的数据
        "api_key": "a6ec389908bcc23fceb2bbe998e3313e",
        "api_secret": "bsa0yv06pl1p"
    }
    girl_url = 'http://i.itpk.cn/api.php'#http://www.itpk.cn/
    girl_content = requests.post(girl_url, data=girl_data)  # 发送请求数据
    print(girl + ':' + girl_content.text)
    time.sleep(1)