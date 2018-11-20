###[PHP 输出 json乱码](https://www.v2ex.com/t/340206#reply28)
echo 之前加 ob_clear(); 

代码有顶格,无 bom, 是 utf-8.
后面是 C3 AF C2 BB 么？仍然是 BOM 头，只是转换过。而如果是 EF BB BF 则是没有转换过的。 
一个典型的 PHP 程序文件应该以“<?php 开头”。这个标签开始之前不应该有任何东西，包括不可见字符。 

当然还有一种可能性，就是你手头上的程序主动输出了那些内容。如果是这样， Debug 会变得很复杂：你需要去掉所有的 Output Buffer 控制（就是让内容直接输出），然后用 headers_list 以及 headers_sent 函数检查到底是谁发送了“ï”字符。
###[代码表白](https://www.zhihu.com/question/55736593)
```js
算法题目 http://hmbb.hustoj.com/  
>>> print('\x42\x65\x20\x77\x69\x74\x68\x20\x6d\x65')
Be with me
>>> print(''.join(['\\'+hex(ord(i))[1:] for i in 'be with me']))
\x62\x65\x20\x77\x69\x74\x68\x20\x6d\x65
```
###[一个循环语句输出九九乘法表](https://www.zhihu.com/question/55768263)
```js
n = 9

for i in range(n * n):
    x = i % n + 1
    y = i // n + 1

    a = lambda: print(str(x) + '*' + str(y) + '=' + str(x * y), end=chr(10 + 22 * int(x != y)))
    b = lambda: 1
    [a, b][int(x > y)]()

import math
R = map(lambda x: (int( (math.sqrt( 8 * x + 1 ) + 1) / 2), x),range(0,45))
RC = map(lambda x: (x[0], x[1] + 1 - (x[0] - 1) * x[0] / 2), R)
T = map(lambda x: ("%d*%d=%d"%(x[1],x[0],x[0]*x[1]) + ("\n" if(x[0]==x[1]) else " ")), RC)
print "".join(T)

print '\n'.join([' '.join([str(i * j) for i in xrange(1,j+1)]) for j in xrange(1,10)])
print ' '.join([x % 10 and ((x / 10 < x % 10) and ' ' or (chr((x / 10) + ord('0')) + "x" + chr((x % 10) + ord('0')))) or '\n' for x in range(1, 101 , 1)])
print str.join('',[str((i-i%9)/9+1)+'*'+str(i%9+1)+'='+str((i%9+1)*((i-i%9)/9+1))+' \n'[i%9] for i in xrange(80)])
console.log([...Array(9)].reduce((m, _, x) => m + [...Array(x + 1)].reduce((m, _, y) => m + `${y + 1}*${x + 1}=${(x + 1) * (y + 1)} `, "") + "\n", ""))




console.log([...Array(45)].reduce(([x, y, s]) => [[x + 1, y, s + `${x}*${y}=${x*y} `], [1, y + 1, s + `${x}*${y}=${x*y}\n`]][1 + Math.sign(x - y)], [1, 1, ""])[2])

// 同上，加了换行，好读点
console.log(
    [...Array(45)].reduce(
        ([x, y, s]) => [
            [x + 1, y, s + `${x}*${y}=${x*y} `],
            [1, y + 1, s + `${x}*${y}=${x*y}\n`]
        ][1 + Math.sign(x - y)],
        [1, 1, ""])
    [2]
)

// 或者这样
console.log(
    [...Array(45)].reduce(
        ([x, y, s]) => ({
            "true":  [x + 1, y, s + `${x}*${y}=${x*y} `],
            "false": [1, y + 1, s + `${x}*${y}=${x*y}\n`]
        })[String(x < y)],
        [1, 1, ""])
    [2]
)
```
###[nginx跨域的设置](https://www.v2ex.com/t/340648#reply7)
if ($http_origin ~* ( https?://.*\.example\.com(:[0-9]+)?$)) { 
add_header Access-Control-Allow-Origin: $http_origin; 
}
###[mysql select count(*)](https://www.v2ex.com/t/339758#reply15)
select （*）在 myiaam 中是常数级的， innodb 却不是的 http://dba.stackexchange.com/questions/17926/why-doesnt-innodb-store-the-row-count
###[解决Python2.x编码之殇](https://zhuanlan.zhihu.com/p/25272901)
```js
print sys.getdefaultencoding()    #系统默认编码
print sys.getfilesystemencoding() #文件系统编码
print locale.getdefaultlocale()   #系统当前编码
print sys.stdin.encoding          #终端输入编码
print sys.stdout.encoding         #终端输出编码
 将unicode格式的字符串存入到文件时，python内部会默认将其先转换为Str格式的系统编码，然后再执行存入步骤
 #! -*- coding:utf-8 -*-
a=u"中文"
f=open("test.txt","w")
f.write(a)
import sys
reload(sys)
sys.setdefaultencoding('gbk')

#! -*- coding:utf-8 -*-
a='你好'
b=a.decode("utf-8").encode("gbk")
print b
f=codecs.open("test.txt", encoding='gbk').read()
a="\\u8fdd\\u6cd5\\u8fdd\\u89c4" # unicode转化为中文
b=a.decode('unicode-escape')
print b
```
###[PHP 就碰到 PDO 扩展的一个大坑](https://www.v2ex.com/t/339840#reply74)
PDO 的参数绑定 bindParam 方法第二个参数是传递一个引用类型，而不是值
###[查看 js 中一个变量值是怎样一步一步生成](https://www.v2ex.com/t/338996#reply5)
```js
如果你知道变量名，可以通过 Object.defineProperty(obj,变量名，{set: function(){console.trace();}} );可以追踪到何时被赋值，何时被修改
o._value = o.value 

Object.defineProperty(o, 'value', { 
get: function() { 
console.trace(); 
return o._value; 
}, 
set : function(val) { 
console.trace(); 
o._value = val; 
} 
});
```
###[Ostagram：一款强大的图片艺术滤镜工具](https://link.zhihu.com/?target=http%3A//ostagram.ru/)
###[利用TensorFlow搞定知乎验证码之《让你找中文倒转汉字》](https://zhuanlan.zhihu.com/p/25297378)
```js
python生成汉字的代码

# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont
import random
import math, string
import logging
# logger = logging.Logger(name='gen verification')

class RandomChar():
    @staticmethod
    def Unicode():
        val = random.randint(0x4E00, 0x9FBF)
        return unichr(val)    

    @staticmethod
    def GB2312():
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = ( head << 8 ) | (body << 4) | tail
        str = "%x" % val
        return str.decode('hex').decode('gb2312')    

class ImageChar():
    def __init__(self, fontColor = (0, 0, 0),
    size = (100, 40),
    fontPath = '/Library/Fonts/Arial Unicode.ttf',
    bgColor = (255, 255, 255),
    fontSize = 20):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', size, bgColor)

    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw    

    def drawTextV2(self, pos, txt, fill, angle=180):
        image=Image.new('RGB', (25,25), (255,255,255))
        draw = ImageDraw.Draw(image)
        draw.text( (0, -3), txt,  font=self.font, fill=fill)
        w=image.rotate(angle,  expand=1)
        self.image.paste(w, box=pos)
        del draw

    def randRGB(self):
        return (0,0,0)

    def randChinese(self, num, num_flip):
        gap = 1
        start = 0
        num_flip_list = random.sample(range(num), num_flip)
        # logger.info('num flip list:{0}'.format(num_flip_list))
        print 'num flip list:{0}'.format(num_flip_list)
        char_list = []
        for i in range(0, num):
            char = RandomChar().GB2312()
            char_list.append(char)
            x = start + self.fontSize * i + gap + gap * i
            if i in num_flip_list:
                self.drawTextV2((x, 6), char, self.randRGB())
            else:
                self.drawText((x, 0), char, self.randRGB())
        return char_list, num_flip_list
    def save(self, path):
        self.image.save(path)



err_num = 0
for i in range(10):
    try:
        ic = ImageChar(fontColor=(100,211, 90), size=(280,28), fontSize = 25)
        num_flip = random.randint(3,6)
        char_list, num_flip_list = ic.randChinese(10, num_flip)
        ic.save(''.join(char_list)+'_'+''.join(str(i) for i in num_flip_list)+".jpeg")
    except:
        err_num += 1
        continue

http://link.zhihu.com/?target=https%3A//github.com/burness/tensorflow-101/tree/master/zhihu_code/src
```
###[通过微博 API 和 Pushbullet 准实时关注你的心上人](https://zhuanlan.zhihu.com/p/25297732)
https://link.zhihu.com/?target=https%3A//www.pushbullet.com/
https://link.zhihu.com/?target=https%3A//gist.github.com/xlzd/01b8b8e1909ae0f601c85e142f2bd15b
###[把 Markdown 文件转化为 PDF](https://www.zhihu.com/question/20849824)
如果你的md文件使用chrome预览，就比较简单了。
点打印，目标，选本地另存为pdf，即可
pandoc README -o example13.pdf  https://link.zhihu.com/?target=http%3A//www.reportlab.com/  http://pandoc.org/installing.html 
$pandoc -N -s --toc --smart --latex-engine=xelatex -V CJKmainfont='PingFang SC' -V mainfont='Monaco' -V geometry:margin=1in 1.md 2.md 3.md ... xx.md  -o output.pdf

Atom有一个Markdown Preview的插件，Markdown文件下按ctrl+shit+m就可以预览Markdown，然后右键生成的预览文件可以保存为html文件，再用chrome打开这个html文件，右键Print里面转换成pdf。  http://www.markdowntopdf.com/ 
 https://github.com/fraserxu/electron-pdf   $ electron-pdf index.html ~/Desktop/index.pdf
选择reportlab以及基于reportlab的chrisglass/xhtml2pdf https://github.com/xhtml2pdf/xhtml2pdf ，这样你就可以简单的pandoc转为html，再由html轻松地转为pdf啦
xhtml2pdf不能识别汉字，需要在html文件中通过CSS的方式嵌入code2000字体，代码是这样的：html { 
font-family: code2000; 
}
###[Python练习第四题，批量修改图片分辨率](https://zhuanlan.zhihu.com/p/25232848)
```js
http://pillow-cn.readthedocs.io/zh_CN/latest/index.html  
>>> from PIL import Image
>>> im=Image.open(r'F:\1.jpg')
>>> print(im.format,im.size,im.mode)
import os
import glob
from PIL import Image

def thumbnail_pic(path):
    a = glob.glob(r'*.jpg')
    for x in a:
        name = os.path.join(path, x)
        im = Image.open(name)
        im.thumbnail((1136, 640))
        print(im.format, im.size, im.mode)
        im.save(name, 'JPEG')
    print('Done!')

if __name__ == '__main__':
    path = '.'
    thumbnail_pic(path)
作者：崔斯特
链接：https://zhuanlan.zhihu.com/p/25232848
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

from PIL import Image

def change_resolution(picPath, reslution):
    img = Image.open(picPath)
    x, y = img.size
    print x, y
    changex = float(x) / reslution[0]
    changey = float(y) / reslution[1]

    # 判断分辨率是否满足
    if changex > 1 or changey > 1:
        change = changex if changex > changey else changey
        print change
        print int(reslution[0] / change), int(reslution[1] / change)
        img.resize((int(x / change), int(y / change))).save('result.jpg')

if __name__ == '__main__':
    change_resolution('pictest.jpg', (1136, 640))
```
###[Python爬取百度图片及py文件转换exe](https://zhuanlan.zhihu.com/p/24854051?refer=linjichu)
```js
作者：崔斯特
链接：https://zhuanlan.zhihu.com/p/24854051
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

#coding:utf-8
import requests
import os
import re
import json
import itertools
import urllib
import sys

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}

def decode(url):
	for key,value in str_table.items():
		url = url.replace(key,value)
	return url.translate(char_table)

def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

re_url = re.compile(r'"objURL":"(.*?)"')
def resolveImgUrl(html):
	imgUrls = [decode(x) for x in re_url.findall(html)]
	return imgUrls

def downImg(imgUrl,dirpath,imgName):
	filename = os.path.join(dirpath,imgName)
	try:
		res = requests.get(imgUrl,timeout=15)
		if str(res.status_code)[0] == '4':
			print(str(res.status_code),":",imgUrl)
			return False
	except Exception as e:
		print('抛出异常:',imgUrl)
		print(e)
		return False
	with open(filename+'.jpg','wb') as f:
		f.write(res.content)
	return True
def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

if __name__ == '__main__':
    print("欢迎使用百度图片下载脚本！\n目前仅支持单个关键词。")
    print("下载结果保存在脚本目录下的img文件夹中。")
    print("=" * 50)
    word = input("请输入你要下载的图片关键词：\n")

    dirpath = mkDir("img")

    urls = buildUrls(word)
    index = 0
    for url in urls:
        print("正在请求：", url)
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                print("已下载 %s 张" % index)
                
pip install pyinstaller
pyinstaller -F baiduimg.py
目录下，dist文件下就有baiduimg.exe文件了，双击即可
```
###[生成激活码](https://zhuanlan.zhihu.com/p/25169905?refer=linjichu)
```js

import uuid

uuids = []
for i in range(200):
	uuids.append(uuid.uuid1())
print uuids
```
###[在图片上加入数字](https://zhuanlan.zhihu.com/p/25147821?refer=linjichu)
```js

from PIL import Image, ImageDraw, ImageFont

img = Image.open('girl.jpg')
draw = ImageDraw.Draw(img)
myfont = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=80)
fillcolor = "#ff0000"
width, height = img.size
draw.text((40,40),'hello', font=myfont, fill=fillcolor)
img.save('result.jpg','jpeg')

 https://github.com/zhangslob/Image  python3下用方正字迹 ，能显示出中文
 
 photo_url = "http://p3.pstatp.com/large/159f00010b30d6736512"
photo_name = photo_url.rsplit('/', 1)[-1] + '.jpg'

with request.urlopen(photo_url) as res, open(photo_name, 'wb') as f:
    f.write(res.read())

 
```
###[python爬虫学习资源整理](https://zhuanlan.zhihu.com/p/25250739)
###[php ecshop修饰符preg_replace/e不安全的几处改动](http://www.epooll.com/archives/841/)
```js
主要集中在 upload/includes/cls_template.php 文件中：

1：line 300 ：

原语句：

return preg_replace("/{([^\}\{\n]*)}/e", "\$this->select('\\1');", $source);

修改为：

return preg_replace_callback("/{([^\}\{\n]*)}/", function($r) { return $this->select($r[1]); }, $source);

2：line 495：

原语句：

$out = "<?php \n" . '$k = ' . preg_replace("/(\'\\$[^,]+)/e" , "stripslashes(trim('\\1','\''));", var_export($t, true)) . ";\n";

修改为：

$replacement = preg_replace_callback("/(\'\\$[^,]+)/" ,

function($matcher){

return stripslashes(trim($matcher[1],'\''));

},

var_export($t, true));

$out = "<?php \n" . '$k = ' . $replacement . ";\n";

3：line 554： //zuimoban.com 转载不带网址，木JJ

原语句：

$val = preg_replace("/\[([^\[\]]*)\]/eis", "'.'.str_replace('$','\$','\\1')", $val);

修改为：

$val = preg_replace_callback("/\[([^\[\]]*)\]/is",

function ($matcher) {

return '.'.str_replace('$','\$',$matcher[1]);

},

$val);

4：line 1071：

原语句：

$replacement = "'{include file='.strtolower('\\1'). '}'";

$source = preg_replace($pattern, $replacement, $source);

修改为：

$source = preg_replace_callback($pattern,

function ($matcher) {

return '{include file=' . strtolower($matcher[1]). '}';

},

$source);
```
###[用PHP蜘蛛做旅游数据分析 ](http://www.epooll.com/archives/843/)
https://github.com/owner888/phpspider  马蜂窝
###[PHP DOMDocument保存xml时中文出现乱码](http://www.epooll.com/archives/842/)
```js
$doc = new DOMDocument();
$doc->loadHTML('<?xml encoding="UTF-8">' . $html);
foreach ($doc->childNodes as $item)
{
    if ($item->nodeType == XML_PI_NODE)
    {
        $doc->removeChild($item); // remove hack
    }
}
$doc->encoding = 'UTF-8'; // insert proper
echo iconv("UTF-8", "GB18030//TRANSLIT", $dom->saveXML($n) );
```
###[Android 窃取手机中微信聊天记录](http://icodeyou.com/2015/06/05/2015-06-05-%20%E8%8E%B7%E5%8F%96%E5%BE%AE%E4%BF%A1%E8%81%8A%E5%A4%A9%E8%AE%B0%E5%BD%95/)
###[手把手教你搭建ngrok服务－轻松外网调试本机站点](https://aotu.io/notes/2016/02/19/ngrok/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io)
###[CSRF实战：借刀杀人之全民助我投诉吧主](https://zhuanlan.zhihu.com/p/24411110?refer=codes)
###[laravel 翻译](https://github.com/cw1997/laravel-Simplified-Chinese)
###[QQ好友列表数据获取](https://zhuanlan.zhihu.com/p/24580113?refer=codes)
https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?uin=123&follow_flag=1&groupface_flag=0&fupdate=1&g_tk=1742568391
###[Python爬虫实战入门六：提高爬虫效率—并发爬取智联招聘](https://zhuanlan.zhihu.com/p/24930071)
```js


# coding:utf-8

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_zhaopin(page):
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=python&p={0}&kt=3'.format(page)
    print("第{0}页".format(page))
    wbdata = requests.get(url).content
    soup = BeautifulSoup(wbdata,'lxml')

    job_name = soup.select("table.newlist > tr > td.zwmc > div > a")
    salarys = soup.select("table.newlist > tr > td.zwyx")
    locations = soup.select("table.newlist > tr > td.gzdd")
    times = soup.select("table.newlist > tr > td.gxsj > span")

    for name, salary, location, time in zip(job_name, salarys, locations, times):
        data = {
            'name': name.get_text(),
            'salary': salary.get_text(),
            'location': location.get_text(),
            'time': time.get_text(),
        }
        print(data)

if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map_async(get_zhaopin,range(1,pages+1))
    pool.close()
    pool.join()
```
###[Python爬虫实战入门四：使用Cookie模拟登录——获取电子书下载链接](https://zhuanlan.zhihu.com/p/24786095)
```js
 

# coding:utf-8
import requests
from bs4 import BeautifulSoup

cookie = '''cisession=19dfd70a27ec0eecf1fe3fc2e48b7f91c7c83c60;CNZZDATA1000201968=1815846425-1478580135-https%253A%252F%252Fwww.baidu.com%252F%7C1483922031;Hm_lvt_f805f7762a9a237a0deac37015e9f6d9=1482722012,1483926313;Hm_lpvt_f805f7762a9a237a0deac37015e9f6d9=1483926368'''

header = {    
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',    
'Connection': 'keep-alive',       
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',  
'Cookie': cookie}

url = 'https://kankandou.com/book/view/22353.html'
wbdata = requests.get(url,headers=header).text
soup = BeautifulSoup(wbdata,'lxml')
print(soup)


 
# coding:utf-8
import requests
from bs4 import BeautifulSoup

cookie = {
"cisession":"19dfd70a27ec0eecf1fe3fc2e48b7f91c7c83c60",          
"CNZZDATA100020196":"1815846425-1478580135-https%253A%252F%252Fwww.baidu.com%252F%7C1483922031",          
"Hm_lvt_f805f7762a9a237a0deac37015e9f6d9":"1482722012,1483926313",          
"Hm_lpvt_f805f7762a9a237a0deac37015e9f6d9":"1483926368"
}

url = 'https://kankandou.com/book/view/22353.html'
wbdata = requests.get(url,cookies=cookie).text
soup = BeautifulSoup(wbdata,'lxml')
print(soup)
```
###[爬取了20万淘宝店铺信息](https://zhuanlan.zhihu.com/p/24389378)
```js
def get_taobao_cate():
    url = 'https://shopsearch.taobao.com/search?app=shopsearch'
    driver = webdriver.PhantomJS(executable_path="F:\\phantomjs.exe")
    driver.get(url)
    driver.implicitly_wait(3)
    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')
    cate_name = re.findall(r"q=(.*?)&amp;tracelog=shopsearchnoqcat",str(soup))
    for c in cate_name:
        cname = urllib.parse.unquote(c,encoding='gb2312')
        cate_list.append(c)
        print(cname)
    print(cate_list)

作者：Lerther
链接：https://zhuanlan.zhihu.com/p/24389378
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

def get_taobao_seller(keywords):
    # 爬取指定数量的店铺信息
    def get_seller_from_num(nums):
        url = "https://shopsearch.taobao.com/search?data-key=s&data-value={0}&ajax=true&_ksTS=1481770098290_1972&callback=jsonp602&app=shopsearch&q={1}&js=1&isb=0".format(nums,keywords)
        # url = "https://shopsearch.taobao.com/search?data-key=s&data-value={0}&ajax=true&callback=jsonp602&app=shopsearch&q={1}".format(nums,keywords)
        wbdata = requests.get(url).text[11:-2]
        data = json.loads(wbdata)
        shop_list = data['mods']['shoplist']['data']['shopItems']
        for s in shop_list:
            name = s['title'] # 店铺名
            nick = s['nick'] # 卖家昵称
            nid = s['nid'] # 店铺ID
            provcity = s['provcity'] # 店铺区域
            shopUrl = s['shopUrl'] # 店铺链接
            totalsold = s['totalsold'] # 店铺宝贝数量
            procnt = s['procnt'] # 店铺销量
            startFee = s['startFee'] # 未知
            mainAuction = s['mainAuction'] # 店铺关键词
            userRateUrl = s['userRateUrl'] # 用户评分链接
            dsr = json.loads(s['dsrInfo']['dsrStr'])
            goodratePercent = dsr['sgr']  # 店铺好评率
            srn = dsr['srn'] # 店铺等级
            category = dsr['ind'] # 店铺分类
            mas = dsr['mas'] # 描述相符
            sas = dsr['sas']  # 服务态度
            cas = dsr['cas']  # 物流速度
            data = {
                'name':name,
                'nick':nick,
                'nid':nid,
                'provcity':provcity,
                'shopUrl':shopUrl,
                'totalsold':totalsold,
                'procnt':procnt,
                'startFee':startFee,
                'goodratePercent':goodratePercent,
                # 'mainAuction':mainAuction,
                'userRateUrl':userRateUrl,
                'srn':srn,
                'category':category,
                'mas':mas,
                'sas':sas,
                'cas':cas
            }
            print(data)
            seller_info.insert_one(data)
            print("插入数据成功")
	    if __name__ == '__main__':
    pool = Pool(processes=4)
    pool.map_async(get_taobao_seller,cate_list)
    pool.close()
    pool.join()
 
```
###[一个获取 QQ 好友名单（号码、名称、头像、等级）的方法](https://www.v2ex.com/t/330033)
1. 登录 “我的 QQ 中心”： http://id.qq.com/ 
2. 来到 “资料-我的等级” 这页： http://id.qq.com/index.html#mylevel 
3. 打开 Chrome 的 Network 监视（或任意浏览器的监视功能、或抓包工具，都行） 
4. 筛选监视列表中的 qqlevel_rank 页面 
5. 这个页面本身就是个 json 格式的列表
项目地址：https://github.com/abosexy/QFriends
https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?uin=QQ 号码&follow_flag=1&groupface_flag=0&fupdate=1&g_tk=替换 GTK 
###[Python爬虫入门实战七：使用Selenium--以抓取QQ空间好友说说为例](https://zhuanlan.zhihu.com/p/25006226)
```js


from bs4 import BeautifulSoup
from selenium import webdriver
import time

#使用selenium
driver = webdriver.PhantomJS(executable_path="D:\\phantomjs.exe")
driver.maximize_window()
#登录QQ空间
def get_shuoshuo(qq):
    driver.get('http://user.qzone.qq.com/{}/311'.format(qq))
    time.sleep(5)
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False
    if a == True:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()#选择用户名框
        driver.find_element_by_id('u').send_keys('QQ号')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('QQ密码')
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_id('QM_OwnerInfo_Icon')
        b = True
    except:
        b = False
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        content = driver.find_elements_by_css_selector('.content')
        stime = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        for con,sti in zip(content,stime):
            data = {
                'time':sti.text,
                'shuos':con.text
            }
            print(data)
        pages = driver.page_source
        soup = BeautifulSoup(pages,'lxml')

    cookie = driver.get_cookies()
    cookie_dict = []
    for c in cookie:
        ck = "{0}={1};".format(c['name'],c['value'])
        cookie_dict.append(ck)
    i = ''
    for c in cookie_dict:
        i += c
    print('Cookies:',i)
    print("==========完成================")

    driver.close()
    driver.quit()

if __name__ == '__main__':
    get_shuoshuo('好友QQ号')
    
  pages = driver.page_source
soup = BeautifulSoup(pages,'lxml')
driver.execute_script("JS代码")
driver.save_screenshot('保存的文件路径及文件名')
```
https://github.com/inconshreveable/ngrok  
###[50 行代码实现微信股价提示](https://zhuanlan.zhihu.com/p/25247206)
```js
作者：ipreacher
链接：https://zhuanlan.zhihu.com/p/25247206
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

__author__ = 'ipreacher'


import time
import itchat
import datetime
import tushare as ts


stock_symbol = input('请输入股票代码 \n>  ')
price_low = input('请输入最低预警价格 \n>  ')
price_high = input('请输入最高预警价格 \n>  ')


# 登陆微信
def login():
    itchat.auto_login()


# 获取股价并发送提醒
def stock():
    time = datetime.datetime.now()    # 获取当前时间
    now = time.strftime('%H:%M:%S') 
    data = ts.get_realtime_quotes(stock_symbol)    # 获取股票信息
    r1 = float(data['price'])
    r2 = str(stock_symbol) + ' 的当前价格为 ' + str(r1)
    content = now + '\n' + r2
    itchat.send(content, toUserName='filehelper')
    print(content)
    # 设置预警价格并发送预警信息
    if r1 <= float(price_low):
        itchat.send('低于最低预警价格', toUserName='filehelper')
        print('低于最低预警价格')
    elif r1 >= float(price_high):
        itchat.send('高于最高预警价格', toUserName='filehelper')
        print('高于最高预警价格')
    else:
        itchat.send('价格正常', toUserName='filehelper')
        print('价格正常')


# 每 3 秒循环执行
if __name__ == '__main__':
    login()
    while True:   
        try:   
            stock()
            time.sleep(3)
        except KeyboardInterrupt:
            itchat.send('Stock_WeChat 已执行完毕！\n'
                '更多有意思的小玩意，请戳---->\n'
                '[https://github.com/ipreacher/tricks]', 
                toUserName='filehelper')
            print('Stock_WeChat 已执行完毕！\n'
                '更多有意思的小玩意，请戳---->\n'
                '[https://github.com/ipreacher/tricks]')
            break
```
###[爬虫程序扒下知乎某个回答所有点赞用户名单](https://www.zhihu.com/question/36338520)
```js
from zhihu import ZhihuClient

client = ZhihuClient('cookies.json')

url = 'http://www.zhihu.com/question/36338520/answer/67029821'
answer = client.answer(url)

print('问题：{0}'.format(answer.question.title))
print('答主：{0}'.format(answer.author.name))
print('此答案共有{0}人点赞：\n'.format(answer.upvote_num))

for upvoter in answer.upvoters:
    print(upvoter.name, upvoter.url)
ZhihuClient().create_cookies('cookies.json')

作者：路人甲
链接：https://www.zhihu.com/question/36338520/answer/142481574
来源：知乎
著作权归作者所有，转载请联系作者获得授权。

#encoding=utf8
import time,requests
from bs4 import BeautifulSoup

headers = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}
s = requests.session()
BASE_URL = 'https://www.zhihu.com'
PHONE_LOGIN = BASE_URL + '/login/phone_num'

def login():
    '''登录知乎'''
    username = ''#你自己的帐号密码
    password = ''
    data = {"phone_num":username,"password":password,"captcha":'HHHH'}
    r = s.post(PHONE_LOGIN,headers = headers,data= data)
    print (r.json())

def zan(ans_id):
    user_list = []
    zanBaseURL = 'http://www.zhihu.com/answer/{}/voters_profile?&offset={}'
    page = 0
    count = 0
    while 1:
        zanURL = zanBaseURL.format(ans_id,str(page))
        page += 10
        zanREQ = s.get(zanURL, headers=headers)
        zanData = zanREQ.json()['payload']
        if not zanData:
            break
        for item in zanData:
            # print item
            zanSoup = BeautifulSoup(item, "html.parser")
            zanInfo = zanSoup.find('a', {'target': "_blank", 'class': 'zg-link'})
            if zanInfo:
                user_id = zanInfo.get('href').split('/')[-1]
                print('userId:', user_id)
                user_list.append(user_id)
                #print 'person_url:', zanInfo.get('href')
            else:
                anonymous = zanSoup.find(
                    'img', {'title': True, 'class': "zm-item-img-avatar"})
                print(anonymous.get('title'))
            count += 1
        print(count)

    return user_list

def get_data_id(answer_list):
    id_list = []
    for answer_url in answer_list:
        soup = BeautifulSoup(s.get(answer_url, headers=headers).content, "html.parser")
        temp_id = soup.find('div',{'tabindex':'-1','itemtype':'http://schema.org/Answer'})
        id_list.append(temp_id['data-aid'])
    return id_list

def find_her():
    #下面填上你要查询的那个回答的url，随便放多少个
    ans_id_list  = get_data_id(['https://www.zhihu.com/question/31427895/answer/140473534',
                                'https://www.zhihu.com/question/50015995/answer/140826031',
                                'https://www.zhihu.com/question/54714393/answer/140950904'])
    llist = []
    for x in ans_id_list:
        llist.extend(zan(x))

    print('\n-----你要找的她就在这里：-----')

    for x in set(llist):
        if llist.count(x) == len(ans_id_list):
            print(x)

login()
find_her()
```
###[JavaScript 如何找到字符串中缺失的括号](https://zhuanlan.zhihu.com/p/25236822)
```js
function checkParanthesis(str){
  var depth = 0;
  for(var i in str){
    if(str[i]=="("||str[i]=="{"||str[i]=="[")
      depth++;
    else if(str[i]==")"||str[i]=="}"||str[i]=="]")
      depth--;
  }
  if(depth !=0) return false;
  return true;
}
console.log(checkParanthesis("() test"));
 
```
###[php文件上传漏洞](https://zhuanlan.zhihu.com/p/25220150)

if($_FILES['userfile']['type'] != "image/gif")  
#这里对上传的文件类型进行判断，如果不是image/gif类型便返回错误。
                {   
                 echo "Sorry, we only allow uploading GIF images";
                 exit;
                 }
         $uploaddir = 'uploads/';
         $uploadfile = $uploaddir . basename($_FILES['userfile']['name']);
         if (move_uploaded_file($_FILES['userfile']['tmp_name'], $uploadfile))
             {
                 echo "File is valid, and was successfully uploaded.\n";
                } else {
                     echo "File uploading failed.\n";
    }
    GIF89a<?php phpinfo(); ?>
###[ppt online](https://www.zhihu.com/question/20204473)
###[史上最全的CSS自适应布局总结](https://zhuanlan.zhihu.com/p/25220324)
###[Ubuntu 有什么奇技淫巧](https://www.zhihu.com/question/27764060)
sudo apt-get install figlet
sudo apt-get install toilet
试一下这两个小命令，生成艺术字
figlet some text
toilet some other text
打开终端输入telnet towel.blinkenlights.nl 按下Ctrl+]后输入quit退出
#安装小工具
sudo apt install fortune
sudo apt install fortune-zh
sudo apt install cowsay
sudo apt install lolcat

#小牛讲道理
for i in {1..5};do echo `fortune`|cowsay;done

#加个颜色
for i in {1..5};do echo `fortune`|cowsay|lolcat;done

###[python 12306 余票](https://zhuanlan.zhihu.com/p/24606846)
```js
 import ssl
ssl._create_default_https_context = ssl._create_unverified_context
req_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2017-01-11&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=BJP&purpose_codes=ADULT'
resp = urllib2.urlopen(req_url)
resp_info = resp.read()
print resp_info
###[pickle 来直接序列化 requests.的 session.cookies](https://www.v2ex.com/t/341375#reply5)
sess=requests.session()
resp=sess.get('http://www.so.com')
f=open('cookiefile','wb')
pickle.dump(resp.cookies,f)  #为什么很多代码都不是这样,而是使用 cookielib 的 LWPCookieJar?
f.close()
```
###[从MySQL binlog解析出你要的SQL](https://github.com/danfengcao/binlog2sql)
shell> git clone https://github.com/danfengcao/binlog2sql.git && cd binlog2sql
shell> pip install -r requirements.txt
MySQL server必须设置以下参数:

[mysqld]
server_id = 1
log_bin = /var/log/mysql/mysql-bin.log
max_binlog_size = 100M
binlog_format = row
user需要的最小权限集合：

select, super/replication client, replication slave

建议授权
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 
shell> python binlog2sql.py -h127.0.0.1 -P3306 -uadmin -p'admin' -dtest -t test3 test4 --start-file='mysql-bin.000002'
误删数据回滚 
shell> python binlog2sql/binlog2sql.py -h127.0.0.1 -P3306 -uadmin -p'admin' -dtest -ttbl --start-file='mysql-bin.000052' --start-position=3346 --stop-position=3556 -B > rollback.sql | cat
shell> mysql -h127.0.0.1 -P3306 -uadmin -p'admin' < rollback.sql

###[Laravel 使用 env 读取环境变量为 null 的问题](https://laravel-china.org/topics/3362)
如果执行 php aritisan config:cache 命令，Laravel 将会把 app/config 目录下的所有配置文件“编译”整合成一个缓存配置文件到 bootstrap/cache/config.php，每个配置文件都可以通过 env 函数读取环境变量，这里是可以读取的。但是一旦有了这个缓存配置文件，在其他地方使用 env 函数是读取不到环境变量的，所以返回 null.

在配置文件即 app/config 目录下的其他地方，读取配置不要使用 env 函数去读环境变量，这样你一旦执行 php artisan config:cache 之后，env 函数就不起作用了。所有要用到的环境变量，在 app/config 目录的配置文件中通过 env 读取，其他地方要用到环境变量的都统一读配置文件而不是使用 env 函数读取。
###[一个php技术栈后端猿的知识储备大纲](https://github.com/TIGERB/easy-tips)
###[一种记录生产环境数据库表结构变更历史的方法](https://www.v2ex.com/t/325614)
https://github.com/seanlook/DBschema_gather/tree/master/schema_structure
###[PHP写文件加锁](https://blog.tanteng.me/2016/11/flock-write/)
```js
public function handle()
{
    $testTxt = storage_path('test2.txt');
    $handle = fopen($testTxt, 'wr');
    flock($handle, LOCK_EX | LOCK_NB);
    for ($i = 0; $i < 100000; $i++) {
        $this->comment('writing...');
        fwrite($handle, 'wo shi tanteng.' . PHP_EOL);
    }
    flock($handle, LOCK_UN);
    fclose($handle);
    $this->comment('time:' . round(microtime(true) - LARAVEL_START, 2));
}
public function handle()
{
    $testTxt = storage_path('test.txt');
    for ($i = 0; $i < 100000; $i++) {
        $this->comment('writing...');
        file_put_contents($testTxt, 'wo shi tanteng.' . PHP_EOL, FILE_APPEND);
    }
    $this->comment('time:' . round(microtime(true) - LARAVEL_START, 2));
}
```
###[error: cannot open .git/FETCH_HEAD: Permission denied](https://blog.tanteng.me/2017/02/git-fetch-permission-denied/)
发现 FETCH_HEAD 的用户和组都是 root 权限，而发布系统的运行进程是 nobody 用户，所以没有权限执行这个 git 命令：git fetch -q –all
cd /data/vhosts/project  && git checkout -q master && git fetch -q –all && git/bin/git clean -fd && git/bin/git reset -q –hard origin/master
###[PHP捕捉异常中断](https://blog.tanteng.me/2016/09/register-shutdown-function/)
```js
class IndexController extends Controller
{
    /**
     * 脚本执行是否完成
     * @var bool
     */
    protected $complete = false;
 
    public function __construct()
    {
        register_shutdown_function([$this, 'shutdown']);
    }
 
    /**
     * 异常处理
     */
    public function shutdown()
    {
        if ($this->complete === false) {
            dump('www.tanteng.me'); //此处应该输出日志并进行异常处理操作
        }
    }
}
设置一个属性为 false，在执行完成时设为 true，最后通过 register_shutdown_function 函数指定的方法进行判断，并做进一步异常处理
调用条件：
1、当页面被用户强制停止时
2、当程序代码运行超时时
3、当ＰＨＰ代码执行完成时
```
###[Laravel 报错: Declaration of XXX](https://blog.tanteng.me/2016/09/laravel-declaration-sessionguard/)
将 clear-compiled 替换，具体修改如下：
"post-install-cmd": [
-       "php artisan clear-compiled",
+       "Illuminate\\Foundation\\ComposerScripts::postInstall",
        "php artisan optimize"
],
"post-update-cmd": [
-        "php artisan clear-compiled",
+        "Illuminate\\Foundation\\ComposerScripts::postUpdate",
         "php artisan optimize"
]
再次执行 sudo composer update 之后，再执行一次 sudo composer dump-autoload 就恢复正常了
###[MySQL大表加字段思路](https://blog.tanteng.me/2017/01/mysql-alter-table-big-data/)
给 MySQL 大表加字段的思路如下：

① 创建一个临时的新表，首先复制旧表的结构（包含索引）

create table new_table like old_table;

② 给新表加上新增的字段

③ 把旧表的数据复制过来

insert into new_table(filed1,filed2…) select filed1,filed2,… from old_table

④ 删除旧表，重命名新表的名字为旧表的名字
###[PHP数组同值稳定排序](https://blog.tanteng.me/2016/11/php-array-sort-order/)
```js
如何保证 PHP 数组同值元素排序后顺序保持不变呢？
function stable_uasort(&$array, $cmp_function) {
    if(count($array) < 2) {
        return;
    }
    $halfway = count($array) / 2;
    $array1 = array_slice($array, 0, $halfway, TRUE);
    $array2 = array_slice($array, $halfway, NULL, TRUE);
 
    stable_uasort($array1, $cmp_function);
    stable_uasort($array2, $cmp_function);
    if(call_user_func($cmp_function, end($array1), reset($array2)) < 1) {
        $array = $array1 + $array2;
        return;
    }
    $array = array();
    reset($array1);
    reset($array2);
    while(current($array1) && current($array2)) {
        if(call_user_func($cmp_function, current($array1), current($array2)) < 1) {
            $array[key($array1)] = current($array1);
            next($array1);
        } else {
            $array[key($array2)] = current($array2);
            next($array2);
        }
    }
    while(current($array1)) {
        $array[key($array1)] = current($array1);
        next($array1);
    }
    while(current($array2)) {
        $array[key($array2)] = current($array2);
        next($array2);
    }
    return;
}
 
function cmp($a, $b) {
    if($a['n'] == $b['n']) {
        return 0;
    }
    return ($a['n'] > $b['n']) ? -1 : 1;
}
 
$a = $b = array(
    'a' => array("l" => "A", "n" => 1),
    'b' => array("l" => "B", "n" => 2),
    'c' => array("l" => "C", "n" => 1),
    'd' => array("l" => "D", "n" => 2),
    'e' => array("l" => "E", "n" => 2),
);
 
uasort($a, 'cmp');
print_r($a);
 
stable_uasort($b, 'cmp');
print_r($b);
也可以使用 PHP 扩展包，这里有一个扩展包 vanderlee/php-stable-sort-functions 就是专门解决这个问题的
```
###[PHP二进制封包](https://blog.tanteng.me/2017/01/php-pack/)
 /**
     * 包头二进制封包
     * @param $length
     * @return string
     */
    private function getHeaderPack($length)
    {
        $header = [
            'version'     => 1,
            'seq'         => time(),
            'body_length' => $length,
        ];
        $headerPack = pack('L3', $header['version'], $header['seq'], $header['body_length']);
        //$this->unPackHeader($headerPack);
        return $headerPack;
    }
这种封包的方式本身也是一种数据加密的方式，你必须知道每个字段的类型和顺序，才能解析数据，所以这个协议的定义也要保密。
###[SSO单点登录系统接入](https://blog.tanteng.me/2016/09/sso-access/)
```js
SSO 登录请求接口往往是接口加上一个回调地址，访问这个地址会跳转到回调地址并带上一个 ticket 参数，拿着这个 ticket 参数再请求接口可以获取到用户信息，如果存在用户则自动登录，不存在就新增用户并登录。
interface SSOLogin
{
    /**
     * 获取登录用户信息
     * @param $ticket
     * @return mixed
     */
    public function getInfoFromTicket($ticket);
 
    /**
     * 单点登录授权地址
     * @return mixed
     */
    public function getAuthUrl();
}
/**
 * 检测是否单点登录
 * @return bool|string
 */
public function actionCheck()
{
    $ticket = Yii::$app->getRequest()->get('ticket');
    if (!$ticket) {
        return $this->renderAuthError('请先授权', sprintf('<a href="%s">点击登录单点登录系统</a>', SSOlogin::getInstance()->getAuthUrl()));
    }
    $userInfo = SSOlogin::getInstance()->getInfoFromTicket($ticket);
    if (empty($userInfo['username'])) {
        return $this->renderAuthError('请先授权', sprintf('<a href="%s">点击登录单点登录系统</a>', SSOlogin::getInstance()->getAuthUrl()));
    }
 
    $username = $this->getUserName($userInfo['username']);
    $user = User::find()->canLogin()->username($username)->one();
    if (!$user) {
        $newUser = [];
        $newUser['username'] = $userInfo['username'];
        $newUser['email'] = $this->getUserName($userInfo['username']);
        $newUser['role'] = User::ROLE_DEV;
        $newUser['is_email_verified'] = 1;
        $newUser['realname'] = $userInfo['truename'];
        $user = $this->addUser($newUser);
    }
    $isLogin = Yii::$app->user->login($user, 3600 * 24 * 30);
    if ($isLogin) {
        $this->redirect('/task/index');
    }
    return true;
}
```
