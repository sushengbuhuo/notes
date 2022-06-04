import json
import os.path
import re
import subprocess
 
import requests
 
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
    'referer': 'https://www.bilibili.com/'
}

# import plotly.graph_objects as go
# import plotly.express as px
# import numpy as np
# import pandas as pd
# df = px.data.tips()
# fig = go.Figure(go.Sunburst(
#     labels=["Female", "Male", "Dinner", "Lunch", 'Dinner ', 'Lunch '],
#     parents=["", "", "Female", "Female", 'Male', 'Male'],
#     values=np.append(
#         df.groupby('sex').tip.mean().values,
#         df.groupby(['sex', 'time']).tip.mean().values),
#     marker=dict(colors=px.colors.sequential.Emrld)),
#                 layout=go.Layout(paper_bgcolor='rgba(0,0,0,0)',
#                                  plot_bgcolor='rgba(0,0,0,0)'))

# fig.update_layout(margin=dict(t=0, l=0, r=0, b=0),
#                   title_text='Tipping Habbits Per Gender, Time and Day')
# fig.show()
def main(url):
    # 获取页面html代码 https://www.52pojie.cn/thread-1643533-1-1.html
    resp = requests.get(url=url, headers=headers)
    html_code = resp.text
    # 解析标题
    title = re.findall('<h1 id="video-title" title="(.*?)" class="video-title">', html_code)[0]
    # 解析播放地址
    play_info = re.findall('<script>window.__playinfo__=(.*?)</script>', html_code)[0]
    print(title)
    print(play_info)
    json_data = json.loads(play_info)
    # 获取音频地址
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
    print(audio_url)
    # 获取视频地址  默认最清晰
    video_url = json_data['data']['dash']['video'][0]['baseUrl']
    print(video_url)
    audio_resp = requests.get(url=audio_url, headers=headers, stream=True)
    # if not os.path.exists('movie'):
    #     os.mkdir('movie')
    with open(f'{title}.mp3', mode='wb') as f:
        for audio_data in audio_resp.iter_content(10240):
            f.write(audio_data)
    video_resp = requests.get(url=video_url, headers=headers, stream=True)
    with open(f'{title}.mp4', mode='wb') as f:
        for video_data in video_resp.iter_content(10240):
            f.write(video_data)
    command = f'ffmpeg -i {title}.mp4 -i {title}.mp3 -c:v copy -c:a aac -strict experimental {title}-merger.mp4'
    print(command)
    subprocess.run(command, shell=True)
 
# if __name__ == '__main__':
    # main('https://www.bilibili.com/video/BV1qL4y1L7dH?p=2')