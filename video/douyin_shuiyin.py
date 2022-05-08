import re
import time

import requests

temp_data = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.138 Mobile Safari/537.36  aweme_170401 JsSdk/1.0 NetType/WIFI Channel/update AppName/aweme app_version/17.4.0 ByteLocale/zh-CN Region/CN AppTheme/light SystemFontScale/1.0 BytedanceWebview/d8a21c6'
    }
}

# 取视频ID
def GetVideo(Str_url):
    # 正则取文本内网址
    patt = re.compile(r'(((https?|ftp|file)://|)[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])', re.S)
    data = patt.findall(Str_url)[3][0]
    if 'v.douyin.com' in data:
        try:
            res = requests.get(
                data,
                headers=temp_data['headers'],
                allow_redirects=False
            )
        except None:
            temp_data['GetVideo'] = False
        else:
            Location = res.headers['Location']
            if 'www.douyin.com/404' in Location:
                temp_data['GetVideo'] = False
            else:
                # 取视频ID
                video_id = re.search('\\d{19}/', Location)[0].replace("/", "")
                temp_data['GetVideo'] = video_id
    else:
        temp_data['GetVideo'] = False

# 获取无水印视频地址https://www.52pojie.cn/thread-1513911-1-1.html
def analysis_url(video_id):
    try:
        res = requests.get(
            'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/',
            headers=temp_data['headers'],
            params={
                'item_ids': video_id
            }
        ).json()
    except None:
        temp_data['analysis_url'] = False
    else:
        if res['status_code'] == 0:
            play_url = res['item_list'][0]['video']['vid']
            temp_data[
                'analysis_url'] = 'https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}&ratio=1080p&line=0'.format(
                video_id=play_url
            )
        else:
            temp_data['analysis_url'] = False

# 下载无水印视频
def down_video(video_url):
    try:
        res = requests.get(
            video_url,
            headers=temp_data['headers']
        ).content
    except None:
        temp_data['down_video'] = False
    else:
        with open('{time}.mp4'.format(time=int(time.time())), 'wb') as f:
            f.write(res)
        temp_data['down_video'] = True

if __name__ == '__main__':
    share_url = '6.92 OxF:/ 好TMD真实  https://v.douyin.com/dBVkpXo/ 复制此链接，打开Dou音搜索，直接观看视频！'
    # 获取视频ID
    GetVideo(share_url)
    if not temp_data['GetVideo']:
        print("解析视频ID失败")
    else:
        # 解析无水印视频地址
        analysis_url(temp_data['GetVideo'])
        if not temp_data['analysis_url']:
            print('获取视频地址失败')
        else:
            # 下载视频
            down_video(temp_data['analysis_url'])
            if not temp_data['down_video']:
                print('下载视频失败')
            else:
                print('视频下载成功！')