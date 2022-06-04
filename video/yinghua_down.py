import requests
import execjs as js
import re
import json
import os
import subprocess as proc
 
 
def get_js_data(url):
"""
获取JSfunc需要数据 https://www.52pojie.cn/thread-1641942-1-1.html
"""
    res = requests.get(url)
    data = re.findall(
        r'<script type="text/javascript">var player_aaaa=(.*\d})?</script>', res.text)
    result = json.loads(data[0])
    url = result['url']
    encrty = result['encrypt']
    return url, encrty
 
 
def decode_jsurl(url):
"""
解密参数，返回m3u8下载地址
"""
    encodeurl, encrty = get_js_data(url)
    with open(os.path.join(os.path.dirname(__file__), 'jsencrypt.js'), 'r', encoding='utf8') as f:
        code = f.read()
    func = js.compile(code)
    url_result = func.call('get_url', encodeurl, encrty)
    return url_result
 
 
def mkdir(path):
"""
创建文件夹，返回路径
"""
    if not os.path.exists(path):
        os.makedirs(path)
    return path
 
 
def download(url, num):
"""
下载m3u8合成MP4
"""
    msg = proc.check_call([os.path.join(os.path.dirname(__file__),'download_m3u8.exe'), decode_jsurl(url), '--workDir', mkdir(
        os.path.join(os.path.dirname(__file__), 'download')), '--saveName', num, '--enableDelAfterDone'])
    print(msg)
 
 
if __name__ == '__main__':
    # 地址入口 
    for num in range(2,13):
        url = 'https://www.xyhdm.cc/vodplay/8052-3-{num}.html'.format(num=num)
        download(url,str(num))