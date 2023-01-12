import requests,re,html
# 下载音频 https://geektutu.com/post/quick-python.html
headers = {
    "Cookie": '',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040026)"
    }
def audio(page):
    url = 'xe.course.business.column.items.get/2.0.0'
    res=requests.post(url,json={"bizData":{"column_id":"p_5f33a4a6e4b0b4059c4bc801","page_index":page,"page_size":8,"sort":"desc"}}, headers=headers, verify=False).json()
    if not res["data"]["list"]:
        return False
    if len(res["data"]["list"]) > 0:
        ids = []
        titles = {}
        for v in res["data"]["list"]:
            ids.append(v["resource_id"])
            titles[v["resource_id"]] = v["resource_title"]
        print(titles,ids)
        res2=requests.post('xe.course.business.audio.audio_list.get/2.0.0',json={"bizData":{"resource_ids":ids}}, headers=headers, verify=False).json()
        for k2,v2 in res2["data"].items():
            audio_data = requests.get(v2,headers=headers)
            with open(titles[k2]+'.mp3','wb') as f:
                f.write(audio_data.content)
        audio(page+1) 
def audio2(page):
    url = 'xe.course.business.column.items.get/2.0.0'
    res=requests.post(url,json={"bizData":{"column_id":"p_5f33a4a6e4b0b4059c4bc801","page_index":page,"page_size":8,"sort":"desc"}}, headers=headers, verify=False).json()
    if not res["data"]["list"]:
        return False
    if len(res["data"]["list"]) > 0:
        ids = []
        titles = {}
        for v in res["data"]["list"]:
            ids.append(v["resource_id"])
            titles[v["resource_id"]] = v["resource_title"]
        print(titles,ids)
        res2=requests.post('xe.course.business.audio.audio_list.get/2.0.0',json={"bizData":{"resource_ids":ids}}, headers=headers, verify=False).json()
        for k2,v2 in res2["data"].items():
            audio_data = requests.get(v2,headers=headers)
            with open(titles[k2]+'.mp3','wb') as f:
                f.write(audio_data.content)
    return True 
page = 1
while True:
    print("页数：",page)
    res = audio2(page)
    if not res:
        break
    page+=1