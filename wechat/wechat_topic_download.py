import requests
import re
import json
import time
import os
 

class WechatAudio(object):
    audio_list_url_api = "https://mp.weixin.qq.com/mp/appmsgalbum?"
    audio_item_url = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }
    audio_voice_url = "https://res.wx.qq.com/voice/getvoice?mediaid="
    all_audio_url = []
    audio_list_url_api_param = {
        "count": 10,
        "begin_itemidx": 1,
        "action": "getalbum",
        "uin": "",
        "key": "",
        "pass_ticket": "",
        "wxtoken": "",
        "devicetype": "",
        "clientversion": "",
        "appmsg_token": "",
        "x5": 0,
        "f": "json",
    }
 
    def __init__(self, list_url):
        # pass
        self.first_req(list_url)
 
    def send_request(self, url, params={}):
        response = requests.get(url, params=params, headers=self.headers)
        # print(response.url)
        return response.content.decode("utf-8")
 
    def first_req(self, list_url):
        start_page = self.send_request(list_url)
        self.audio_list_url_api_param['__biz'] = re.search(r'__biz=(.*?)&', list_url).group(1)
        self.audio_list_url_api_param['album_id'] = re.search(r'album_id=(.*?)&', list_url).group(1)
        self.audio_list_url_api_param['begin_msgid'] = re.findall('data-msgid="(.*)"', start_page)[-1]
        links = re.findall('data-link="(.*)"', start_page)
        self.all_audio_url = [link for link in links]
        self.more_url_list(self.audio_list_url_api_param)
 
    def more_url_list(self, params):
        api_res = json.loads(self.send_request(self.audio_list_url_api, params))['getalbum_resp']['article_list']
        for res_item in api_res:
            self.all_audio_url.append(res_item['url'])
        if int(api_res[-1]['pos_num']) >= 10:
            self.audio_list_url_api_param['begin_msgid'] = api_res[-1]['msgid']
            self.audio_list_url_api_param['begin_itemidx'] = api_res[-1]['itemidx']
            time.sleep(10)
            print(len(self.all_audio_url))
            self.more_url_list(self.audio_list_url_api_param)
 
        for audio_url in self.all_audio_url:
            self.down_audio_file(audio_url)
            time.sleep(5)
 
    def down_audio_file(self, link_url):
        dt_res = self.send_request(link_url)
        voice_id = re.findall(r'voice_encode_fileid=\"(.*?)\"', dt_res)[0]
        title = re.search(r"property=\"og:title\" content=\"(.*?)\"", dt_res).group(1)
        audio_data = requests.get(self.audio_voice_url + voice_id)
        aduio_path = "."
        isExists = os.path.exists(aduio_path)
        if not isExists:
            os.makedirs(aduio_path)
        print('正在下载音频：' + title + '.mp3')
        with open(aduio_path+title + '.mp3', 'wb') as f:
            f.write(audio_data.content)
 
 
if __name__ == "__main__":
    topic_url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5NjAxOTU4MA==&action=getalbum&album_id=1681628721901830149&scene=173"
    wechatAudio = WechatAudio(topic_url)