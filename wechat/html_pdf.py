import os,pdfkit,requests
import os,sys
import requests
import json
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from time import sleep
config_pdf = pdfkit.configuration(wkhtmltopdf=r'd:\wkhtmltopdf\bin\wkhtmltopdf.exe')
#把一个文件夹下的html文件都转为pdf
def PDFDir(htmldir,pdfdir):
    if not os.path.exists(pdfdir):
        os.makedirs(pdfdir)
    flist = os.listdir(htmldir)
    for f in flist:
        if (not f[-5:]==".html") or ("tmp" in f): #不是html文件的不转换，含有tmp的不转换
            continue
        htmlpath = htmldir+"/"+f
        tmppath = htmlpath[:-5] + "_tmp.html"#生成临时文件，供转pdf用
        htmlstr = ReadFile(htmlpath)
        bs = BeautifulSoup(htmlstr, "lxml")
        title = ""
        # pdf文件名中包含文章标题，但如果标题中有不能出现在文件名中的符号则会转换失败
        titleTag = bs.find(id="activity-name")
        if titleTag is not None:
            title = "_" + titleTag.get_text().replace(" ", "").replace("  ","").replace("\n","").replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')
        ridx = htmlpath.rindex("/") + 1
        pdfname = htmlpath[ridx:-5] + title
        pdfpath = pdfdir+"/"+ pdfname + ".pdf"

        """
            把js等去掉，减少转PDF时的加载项，
            注意此处去掉了css(link），如果发现pdf格式乱了可以不去掉css
        """
        [s.extract() for s in bs(["script", "iframe", "link"])]
        SaveFile(tmppath, str(bs))
        try:
            PDFOne(tmppath,pdfpath)
        except Exception as e:
            print(e)
        
#保存文件
def SaveFile(fpath,fileContent):
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(fileContent)
        
#读取文件
def ReadFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        all_the_text = f.read()
    return all_the_text
#把一个Html文件转为pdf
def PDFOne(htmlpath,pdfpath,skipExists=True,removehtml=True):
    if skipExists and os.path.exists(pdfpath):
        print("pdf exists",pdfpath)
        if removehtml:
            os.remove(htmlpath)
        return
    exepath = "wkhtmltopdf.exe"#把wkhtmltopdf.exe文件保存到与本py文件相同的目录下
    cmdlist =[]
    cmdlist.append(" --load-error-handling ignore ")
    cmdlist.append(" --page-height 200 ") #数字可以自己调节，也可以不加这两行
    cmdlist.append(" --page-width 140 ")
    cmdlist.append(" " + htmlpath +" ")
    cmdlist.append(" " + pdfpath + " ")
    cmdstr = exepath + "".join(cmdlist)
    print(cmdstr)
    result = subprocess.check_call(cmdstr, shell=False)
    # stdout,stderr = result.communicate()
    # result.wait() #等待转换完一个再转下一个
    if removehtml:
        os.remove(htmlpath)


    """
        1.设置：
            先去config.json文件中设置
            jsonDir：Fiddler生成的文件
            htmlDir：保存html的目录，路径中不能有空格
            pdfDir：保存pdf的目录，路径中不能有空格
            {
    "jsonDir": "D:/download/vWeChatCrawl/json",
    "htmlDir": "D:/download/vWeChatCrawl/html",
    "pdfDir": "D:/download/vWeChatCrawl/pdf"
}
        2.使用方法：    
            运行 python start.py      #开始下载html  
            运行 python start.py pdf  #把下载的html转pdf 
    """
PDFDir('.','pdf')
# flist = os.listdir('.')
# for f in flist:
# 	print(f)
# 	if f.endswith('html'):
# 		(name, ext) = os.path.splitext(f)
# 		name=name.replace(' ', '').replace('|', '，').replace('\\', '，').replace('/', '，').replace(':', '，').replace('*', '，').replace('?', '，').replace('<', '，').replace('>', '，').replace('"', '，')
# 		with open(f,encoding='utf-8') as file:
# 			pdfkit.from_string(file.read(),f'{name}.pdf', configuration=config_pdf) 
# 		# pdfkit.from_file(f,f'{name}.pdf', configuration=config_pdf) 