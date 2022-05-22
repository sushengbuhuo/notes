import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import requests
from alive_progress import alive_bar
from fake_useragent import UserAgent
from rich.console import Console

#https://www.52pojie.cn/thread-1635183-1-1.html
console = Console()
headers = {'User-Agent': UserAgent().random}
logging.basicConfig(level=logging.INFO
                    ,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
                    ,datefmt='%a, %d %b %Y %H:%M:%S'
                    ,filename='xigua_download.log'
                    ,filemode='w')
logging.getLogger(__name__)

def retry(exception=Exception, tries=3, delay=1, logger=logging):
    '''
    重试装饰器
    :param exception: 异常类型
    :param tries: 重试次数
    :param delay: 重试间隔
    :param logger: 日志对象
    :return:
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _tries = tries
            while _tries > 1:
                try:
                    return f(*args, **kwargs)
                except exception as e:
                    _tries -= 1
                    if logger:
                        logger.error(e)
                    time.sleep(delay)
            return f(*args, **kwargs)
        return wrapper
    return decorator


@retry()
def get_xigua_video_url(xigua_url:str) -> str:
    '''
    西瓜视频API接口
    xigua_url: 西瓜网页链接地址
    '''
    url = 'http://47.99.158.118/video-crack/v2/parse'
    data = {'content': xigua_url}

    response = requests.post(url, headers=headers,data=data,timeout=15)
    return response.json()['data']['url']

def chunk_write(chunk, f):
    '''
    文件块写入函数
    chunk: 文件块
    f: 文件对象
    '''
    f.write(chunk)
    f.flush()
    return True
    

def filename_filter(filename:str) -> str:
    '''
    去除文件名非法字符
    filename: 文件名
    '''
    illegal_characters = ['\\','/',':','*','?','"','<','>','|','\n','\r','\t',' ']
    for char in illegal_characters:
        filename = filename.replace(char,'')
    if filename == '':
        filename = 'xigua_video_ ' + str(time.time()) + '.mp4'
    elif filename.split('.')[-1] != 'mp4':
        filename += '.mp4'
    elif len(filename.split('.')) < 2:
        filename += '.mp4'
    else:
        return filename
    return filename
def mkdir_path(path:str=os.path.join(os.getcwd(),'西瓜视频')) -> str:
    '''
    创建目录
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    return path
@retry()
def xigua_video_download(url:str, filename_path:str,max_workers=16) -> str:
    '''
    多线程西瓜视频下载
    url: 西瓜视频链接
    filename: 保存文件名
    max_workers: 最大线程数
    '''
    # https://docs.python-requests.org/en/latest/user/advanced/#body-content-workflow 参考文献
    with requests.get(url,stream=True,verify=False,headers=headers,timeout=15) as r:
        start_time = time.time()
        # 支持分块下载
        try:
            file_size = r.headers['content-length']
            # file_size = int(file_size)/1024/1024 # MB(float)
        except:
            logging.error('error:获取文件大小失败,检查URL,或不支持对线程下载')

        # 每个线程要下载的文件大小
        chunk_size = int(int(file_size)/max_workers)
        with open(filename_path, 'wb') as f:
            with alive_bar(max_workers+1,force_tty=True,enrich_print=False) as bar,ThreadPoolExecutor(max_workers=max_workers) as executor:
                [executor.submit(chunk_write, chunk,f).add_done_callback(lambda func: bar()) for chunk in r.iter_content(chunk_size=chunk_size)]
        spend = time.time() - start_time
        speed = float(int(file_size)/1024/1024/spend)
        logging.info(f"下载完成，耗时{spend}秒，速度{speed}MB/s")
        console.print(f'[green][*]状态:下载完成！！！\n[yellow][+]文件保存在:{os.path.dirname(filenamepath)}\n[+]耗时{spend:.2f}秒\n[+]平均速度{speed:.2f}MB/s')

if __name__ == '__main__':
    xigua_url = input("请输入西瓜视频链接：").strip()
    filename = input("请输入保存文件名：").strip()
    filename = filename_filter(filename)
    path = mkdir_path()
    max_workers = input("请输入最大线程数(回车默认线程数16):").strip()
    xigua_url = get_xigua_video_url(xigua_url)
    filenamepath = os.path.join(path,filename)
    xigua_video_download(xigua_url,filenamepath) if max_workers == '' else xigua_video_download(xigua_url,filenamepath,int(max_workers))
