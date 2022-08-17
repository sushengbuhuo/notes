import base64
import hashlib
import re
import time
from pathlib import Path
 
import requests
from Crypto.Cipher import AES
from H_m3u8DL import m3u8download
from loguru import logger
from lxml import etree
from urllib3 import disable_warnings
 
base_dir = Path(__file__).parent
logger.add(base_dir.joinpath('xiaoxiong.log'))

disable_warnings()
 
# 逆向目标-网-站 ： [url=https://www.xxys520.com/]https://www.xxys520.com/[/url] 小熊影视（蓝光影片较多，网速一般，故此使用解密手段下载影视）
#https://www.52pojie.cn/thread-1662890-1-1.html
@logger.catch
def get_response(url,mode='get',data=None):
    """ 请求函数 """
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    if mode == 'get':
        return requests.get(url,headers=headers,verify=False,timeout=30).text
    else:
        return requests.post(url,headers=headers,verify=False,data=data,timeout=30).json()
         
def decrypt(enStr):
    """ Zeropadding 解密函数 """
    vi = "NXbHoWJbpsEOin8b".encode('utf8')
    key = hashlib.md5("rXjWvXl6".encode()).hexdigest().encode('utf8')
    enStr  = base64.b64decode(enStr)
    cipher = AES.new(key,AES.MODE_CBC,vi)
    msg = cipher.decrypt(enStr)
    msg = msg.rstrip(b'\0')
    msg = msg.decode('utf8')
    logger.info(f'解密的m3u8网址是:{msg}')
    return msg # m3u8 网址
 
def get_encryption_field(url):
    """获取加密字段"""
    res_text = get_response(url)
    try:
        title = etree.HTML(res_text).xpath('/html/head/title/text()')[0]
    except Exception as e:
        title = f'为找到正确的title_{time.time()}'
        logger.error('title 未找到，请注意')
    string = r'<script type="text/javascript">var player_aaaa=({.*?})</script>'
    str_json = re.findall(string,res_text,re.I)[0]
    encrypted_url = eval(str_json).get('url')
    return encrypted_url,title
 
def get_the_m3u8_url(encrpyted_url):
    """获取m3u8下载地址"""
    url = "https://player.xxys520.com/5348837768202767938.php"
    _json = get_response(url,mode='post',data={'url':encrpyted_url})
    m3u8_url = decrypt(_json.get('url'))
    return m3u8_url
 
def main(filename):
    """
    主要逻辑
    """
    with open(base_dir.joinpath(filename),'r',encoding='utf8') as f:
        urls = f.readlines()
    for url in urls:
        encrypted_url,title = get_encryption_field(url)
        m3u8_url = get_the_m3u8_url(encrypted_url)
        m3u8download(m3u8_url,title,work_dir=str(base_dir.joinpath('movies')))
        logger.info(f'{title}已经下载完成')
 
if __name__ == '__main__':
    filename = 'address_url.txt' # 每行一个网址，逐行下载
    main(filename)