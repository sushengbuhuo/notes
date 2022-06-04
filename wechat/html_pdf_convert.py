import time
import re
import os
import requests,json
from bs4 import BeautifulSoup
from pdf2docx import Converter
#convert
def to_pdf():
    import pdfkit
    print('导出 PDF...')
    htmls = []
    for root, dirs, files in os.walk('.'):
    	for name in files:
    		if name.endswith(".html"):
    			print(name)
    			try:
    				pdfkit.from_file(name, 'pdf/'+name.replace('.html', '')+'.pdf')
    			except Exception as e:
    				print(e)
        # htmls += [name for name in files if name.endswith(".html")]
    # print(htmls)
    # pdfkit.from_file(sorted(htmls), 'out.pdf')
def to_word():
    print('导出 word...')
    htmls = []
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith(".pdf"):
                print(name)
                try:
                    cv = Converter(name)
                    cv.convert('word/'+name.replace('.pdf', '')+'.docx')
                    cv.close()
                except Exception as e:
                    print(e)
        # htmls += [name for name in files if name.endswith(".html")]
    # print(htmls)
    # pdfkit.from_file(sorted(htmls), 'out.pdf')
to_pdf()
to_word()