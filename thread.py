from concurrent.futures import ThreadPoolExecutor
import requests
import threading
from bs4 import BeautifulSoup
 
url_web = "https://www.99tu.com/"
 
 
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
# }
 
def download_img(img_src, img_path):
    img_responce = requests.get(img_src)
    img_name = str(img_src).split("/")[-1]
    with open(img_path + img_name, "wb") as f:
        f.write(img_responce.content)
    print(threading.current_thread().name + "执行下载完成=>" + img_src)
 
 
def download():
    responce = requests.get(url_web)
    html = BeautifulSoup(responce.text, "html.parser")
    imgs = html.find_all("img")
    img_path = "D:\\img\\"
 
    # 定义线程池数量为 设置线程数为5
    with ThreadPoolExecutor(max_workers=5) as pool:
 
        for i in imgs:
            img_src = i.get("src")
            if img_src.__contains__("jpg"):
                # 提交线程
                pool.submit(download_img, img_src, img_path)
 
 
if __name__ == '__main__':
    download()