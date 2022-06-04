import requests,re,os,ssl
from urllib.parse import urlsplit
from os.path import basename
import traceback,urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        }
url=input('请输入知乎地址:')
id=re.search(r'.*zhihu.com/question/(\d+)/answer/\d+',url).group(1)
if not os.path.exists(id):
	os.mkdir(id)
res = requests.get(url,headers=header).text
imgs = re.findall(r'<img src="(https.+?)" ',res)
# imgs = re.findall(r'data-actualsrc="(https.+?)" ',res)
print('图片数',len(imgs))
for img in imgs:
	try:
		print('正在下载图片',img)
		res = requests.get(img,headers=header, verify=False)
		file_name = basename(urlsplit(img)[2])
		# with open(str(re.search('https://(.*?)/\d+/(.*)\.jpg',img).group(2)) + '.jpg','wb') as f:
		with open(id+os.sep+file_name,'wb') as f:
			f.write(res.content)
	except Exception as e:
		print('下载失败',e)
"""
<img src="https://pic2.zhimg.com/v2-7c6ec1be430d1117908b2a03bdf35187_r.jpg?source=1940ef5c" data-rawwidth="1080" data-rawheight="2340" data-size="normal" data-default-watermark-src="https://pic3.zhimg.com/50/v2-52a7fe4ae2f49c872008a29a2d403806_720w.jpg?source=1940ef5c" class="origin_image zh-lightbox-thumb lazy" width="1080" data-original="https://pic2.zhimg.com/v2-7c6ec1be430d1117908b2a03bdf35187_r.jpg?source=1940ef5c" data-actualsrc="https://pica.zhimg.com/50/v2-7c6ec1be430d1117908b2a03bdf35187_720w.jpg?source=1940ef5c" data-lazy-status="ok">
"""