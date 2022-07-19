import logging,os,html
from PyPDF2 import  PdfFileReader, PdfFileWriter,PdfFileMerger#pip install PyPDF2
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_writer = PdfFileWriter()
merger = PdfFileMerger()
num = 0
# for root, dirs, files in os.walk('.'):
#     # 循环读取合并pdf文件https://www.zhihu.com/question/344805337/answer/1116258929
#     for name in files:
#         if name.endswith(".pdf"):#glob.glob('*.pdf')
#             logger.info(name);file_reader = PdfFileReader(f"{name}")
#             file_writer.addBookmark(html.unescape(name).replace('.pdf',''), num, parent=None)#书签名 指向页数  父书签  颜色   加粗   斜体   缩放类型  缩放的参数值
#             # 遍历每个pdf的每一页
#             for page in range(file_reader.getNumPages()):
#                 num += 1
#                 file_writer.addPage(file_reader.getPage(page))
# with open(r"公众号苏生不惑历史文章合集.pdf",'wb') as f:
#     file_writer.write(f)

def bookmark_export(lines):
    bookmark = ''
    for line in lines:
        if isinstance(line, dict):
            bookmark += line['/Title'] + ','+str(line['/Page']+1)+'\n'
        else:
            bookmark_export(line)
    return bookmark
with open('公众号苏生不惑历史文章合集.pdf', 'rb') as f:
    #一个嵌套的列表
    lines = PdfFileReader(f).getOutlines();#[{'/Title': '2020-09-13_公众号第一篇文章', '/Page': 0, '/Type': '/Fit'}]
    bookmark = bookmark_export(lines)

with open('公众号苏生不惑历史文章合集.csv', 'a+', encoding='utf-8-sig') as f:
    f.write(bookmark)