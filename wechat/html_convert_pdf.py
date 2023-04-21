import time
import re,os
import requests,json
from bs4 import BeautifulSoup
from pdf2docx import Converter
import pdfkit
#convert
def to_pdf():
    print('转换PDF...')
    if not os.path.exists('pdf'):
        os.mkdir('pdf')
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
    print('转换word...')
    htmls = []
    if not os.path.exists('word'):
        os.mkdir('word')
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
# to_word()