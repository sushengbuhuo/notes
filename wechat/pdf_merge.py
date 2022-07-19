import logging,os,html
from PyPDF2 import  PdfFileReader, PdfFileWriter#pip install PyPDF2
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
file_writer = PdfFileWriter()
num = 0
for root, dirs, files in os.walk('.'):
    # 循环读取合并pdf文件
    for name in files:
        if name.endswith(".pdf"):
            logger.info(name);file_reader = PdfFileReader(f"{name}")
            file_writer.addBookmark(html.unescape(name).replace('.pdf',''), num, parent=None)#书签名 指向页数  父书签  颜色   加粗   斜体   缩放类型  缩放的参数值
            # 遍历每个pdf的每一页
            for page in range(file_reader.getNumPages()):
                num += 1
                file_writer.addPage(file_reader.getPage(page))
with open(r"公众号苏生不惑历史文章合集.pdf",'wb') as f:
    file_writer.write(f)