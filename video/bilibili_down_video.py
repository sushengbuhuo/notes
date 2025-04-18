import requests
import time
import json,html
import random,re,os,csv
from bs4 import BeautifulSoup
import subprocess
requests.packages.urllib3.disable_warnings()
sname=input('请输入txt文件名：')
with open(f'{sname}.txt', encoding='utf-8') as f:
    contents = f.read()
urls=contents.split('\n')
for url in urls:
    try:
        result = subprocess.run(['lux', url], capture_output=True, text=True, check=True)
        print("脚本执行成功，输出如下:",url)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"脚本执行失败，错误信息: {e.stderr}")