import requests
import json,jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 模拟浏览器请求
headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Accept': '*/*',
}
# 构建 URL 以及 POSt 参数
url = 'https://music.163.com/weapi/v1/play/record?csrf_token='
data = {
    'params': 'B5iB/PvlOxS4eNIHbHw3OjWa4OAoOXW6T1pXuZeN/LgtrTQBLBoMgLMUgw6mPSPc0MpwGf1TN73sFqm805nj3YzGjiGG2hojDTn4UKWdW+81fT1vIdwhKPtQah9lLghI3d8j3sA064t3Wyul6jsmd96IJ57JX/xW9wf2yc04a4+tu9xRcAuzLEAZycQR6rrl+ItcGyvN6bMcfCEhwdqWMXqGZO1M/7fGcAcAh+HPd/s=',
    'encSecKey': '6235e66e0bf82a479e445f75eb4705b5325a9885c48e21023eca46cea5b84233a081f51d3ba9bffef1d419a73c66cece196adc45120676af77f63b26f9be77477d84dd1a12c7a0a525fcd180ce59328b812307598e59d3803b5763783b5e0e901e25b2a6200eadbfee32d8433a98a81ce65c7ed0bb1b7f03a43c15f91e14fa70'
}
# 发送请求
req = requests.post(url, data)  # 发送 post 请求，第一个参数是 URL，第二个参数是参数
# print(json.loads(req.text))
# 输出结果
# {"allData":[{"playCount":0,"score":100,"song":{"name":"盛夏光年 (2013版)","id":28181110,"pst":0,"t":0,"ar":[{"id":13193,"name":"五月天","tns":...
result = json.loads(req.text)
names = []
for i in range(100):
    names.append(result['allData'][i]['song']['ar'][0]['name'])

# names = jieba.cut(str(names), cut_all=False)
print(len(names))
text = ",".join(list(set(names)))
print(len(list(set(names))))
print(text)

def show_word_cloud(text):
    wc = WordCloud(font_path='c:/windows/fonts/simhei.ttf', background_color="white", scale=2.5,
                   contour_color="lightblue", ).generate(text)
    # 读入背景图片
    # w = WordCloud(background_color='white', scale=1.5).generate(text)
    wc.to_file("music_list.png")
    plt.figure(figsize=(16, 9))
    plt.imshow(wc)
    plt.axis('off')
    # plt.show()

show_word_cloud(text)