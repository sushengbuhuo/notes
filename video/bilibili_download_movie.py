import requests
import re
import os
import shutil
from bs4 import BeautifulSoup
import time
 
def type_of_video(url):
    response = requests.get(url, headers=headers1)
    type = BeautifulSoup(response.text, 'lxml').find(attrs={'property': 'og:type'})['content']
    if 'movie' in type:
        return 'movie'
    elif 'anime' in type:
        return 'anime'
    elif 'documentary' in type:
        return 'documentary'
    elif 'tv' in type:
        return 'tv'
    else:
        return 'video'
 
 
def get_all_url(url, type):
    if type == 'anime' or type == 'tv' or type == 'documentary':
        response = requests.get(url, headers=headers1)
        text = response.text
        pattern1 = 'upInfo.*</html>'
        pattern2 = '"share_url":"(http.*?)"'
        a = re.sub(pattern1, '', text)
        result = re.findall(pattern2, a)
        return result
    else:
        return url
 
 
def get_downloadurl(url, type):         #获取视频和音频的下载地址
    try:
        response = requests.get(url, headers=headers1)
        if response.status_code == 200:
            text = response.text
            title_of_series = BeautifulSoup(text, 'lxml').find(attrs={'property': 'og:title'})['content']
            if type == 'movie' or type == 'video':
                title_of_series = 'Bilibili下载视频'
                pattern_title = '.__INITIAL_STATE__.*?[tT]itle.*?:"(.*?)"'
            else:
                pattern_title = '.__INITIAL_STATE__.*?[tT]itle.*?:"' + title_of_series + '.*?：(.*?)"'
            pattern_video = '"video":.+?"baseUrl".*?"(https://.*?.m4s.*?)"'
            pattern_audio = '"audio":.+?"baseUrl".*?"(https://.*?.m4s.*?)"'
            url_video = re.search(pattern_video, text)[1]
            url_audio = re.search(pattern_audio, text)[1]
            title = re.search(pattern_title, text)[1]
            urls = {
                'video': url_video,
                'audio': url_audio,
                'title': title,
                'title_of_series': title_of_series
            }
            return urls
    except ConnectionError as e:
        print(e.args)
        print('获取视频和音频的下载地址失败')
        return None
 
 
def merge(title, output):
    os.system('D:/ffmpeg/bin/ffmpeg -i ./download/"' + title + '.mp3" -i ./download/"' + title + '.mp4" \
-acodec copy -vcodec copy ./' + output + '/"' +title + '.mp4"')
 
 
def down_video(urls):
    if not os.path.exists('./download'):
        os.mkdir('./download')  # 创建临时文件夹以便存放音频，视频
    if not os.path.exists(urls['title_of_series']):
        os.mkdir(urls['title_of_series'])
    try:
        video = requests.get(urls['video'], headers=headers2, stream=True)
        if video.status_code == 206:
            chunk_size = 1024
            content_size = int(video.headers['content-length'])
            data_count = 0
            with open('./download/' + urls['title'] + '.mp4', 'wb') as f:
                for data in video.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    data_count += len(data)
                    progress = data_count * 100 / content_size
                    print('\r 正在下载视频：[%s%s] %d%%' % (int(progress) * '█', ' ' * (100 - int(progress)), progress), end=' ')
    except:
        print("Error!")
        shutil.rmtree('./download')
        return False
    try:
        audio = requests.get(urls['audio'], headers=headers2, stream=True)
        if audio.status_code == 206:
            chunk_size = 1024
            content_size = int(audio.headers['content-length'])
            data_count = 0
            with open('./download/' + urls['title'] + '.mp3', 'wb') as f:
                for data in audio.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    data_count += len(data)
                    progress = data_count * 100 / content_size
                    print('\r 正在下载音频[%s%s] %d%%' % (int(progress) * '█', ' ' * (100 - int(progress)), progress), end=' ')
    except:
        print('Error!')
        shutil.rmtree('./download')
        return False
    merge(urls['title'], urls['title_of_series'])
    shutil.rmtree('./download')
    return True
 
 
if __name__ == '__main__':
    cookie = '_uuid=9B64DFDF-77FA-B534-2E72-49A106CE110DC682289infoc; \
    buvid3=50623E02-1028-4685-AE64-7853FDE84A31167635infoc; b_nut=1638072282; \
    buvid_fp=50623E02-1028-4685-AE64-7853FDE84A31167635infoc; video_page_version=v_old_home; \
    rpdid=|(u~)|mlu~k)0J\'uYJ)|~kJ|); DedeUserID=700337367; DedeUserID__ckMd5=ba3f79c73c36273c; \
    SESSDATA=3ba827d6%2C1653630220%2Ceff2c*b1; bili_jct=3c92286f654e3688607a4b9ad6c49735; \
    LIVE_BUVID=AUTO1316382472513699; PVID=1; sid=aobl97oa; fingerprint3=875983947f1f5d5f3781bd48cdee2293; \
    buvid_fp_plain=50623E02-1028-4685-AE64-7853FDE84A31167635infoc; \
    fingerprint=97327f5a28a5092d2105923cc76c56a6; fingerprint_s=112f5b51fab3c4a7c5d194de1798920e; \
    i-wanna-go-back=-1; b_ut=5; CURRENT_BLACKGAP=0; blackside_state=0; CURRENT_FNVAL=2000; \
    CURRENT_QUALITY=116'
    headers1 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
        'cookie': cookie
    }
    headers2 = {
        'referer': 'https://www.bilibili.com/bangumi/play/ep402225/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
        'range': 'bytes=0-1000000000000'
    }
    end_download = False
    while not end_download:
        url = input('请输入要下载的视频网址：')
        type = type_of_video(url)
        allurls = get_all_url(url, type)
        if isinstance(allurls, str):
            urls = get_downloadurl(allurls, type)
            is_succeessful = down_video(urls)
            if is_succeessful:
                print("下载完成")
            else:
                print('下载失败')
        else:
            choice = input("是否下载全部剧集（y/n）：")
            while choice != 'y' and choice != 'n':
                print(choice)
                choice = input('请输入y或n：')
            if choice == 'y':
                download_all = True
            else:
                download_all = False
            if download_all:
                i = 0
                while i < len(allurls):
                    urls = get_downloadurl(allurls[i].encode('utf8').decode("unicode_escape"), type)
                    if urls:
                        is_succeessful = down_video(urls)
                        if is_succeessful:
                            print("第%d集下载完成  已完成：%.2f%%" % (i+1, i+1/len(allurls)-1))
                            i += 1
                        else:
                            print('第%d集下载失败，将于30分钟后再次尝试下载' % (i+1))
                            time.sleep(1800)
                    else:
                        print('第%d集下载失败，将于30分钟后再次尝试下载' % (i+1))
                        time.sleep(1800)
            else:
                urls = get_downloadurl(url, type)
                is_succeessful = down_video(urls)
                if is_succeessful:
                    print("下载完成")
                else:
                    print('下载失败')
            choice = input('是否继续下载？（y/n）：')
            while choice != 'y' and choice != 'n':
                print(choice)
                choice = input('请输入y或n：')
            if choice == 'y':
                end_download = False
            else:
                end_download = True