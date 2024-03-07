import asyncio,os
from pyppeteer import launch
import tkinter,time
import shutil
# import pyppeteer.chromium_downloader
# PYPPETEER_CHROMIUM_REVISION = '1263111'
# print('默认版本：{}'.format(pyppeteer.__chromium_revision__))
# print('可执行文件默认路径：{}'.format(pyppeteer.chromium_downloader.chromiumExecutable.get('win64')))
# print('win64平台下载链接为：{}'.format(pyppeteer.chromium_downloader.downloadURLs.get('win64')))
# from playwright.sync_api import sync_playwright 文件名带#会失败
if not os.path.exists('pdf'):
    os.mkdir('pdf')
async def main():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    html_files = [file for file in files if file.endswith('.html')]
    if True:
    # for root, dirs, files in os.walk('.'):
        html_files.sort(reverse = True)
        num = 0
        browser = await launch()
        # browser = await launch()# {'args': ['--disable-infobars'],'userDataDir': './userdata'} 登录后保存cookie
        for name in html_files:
            if name.endswith(".html"):
                num +=1
                print(name,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),'文章数量：',num)
                try:
                    page = await browser.newPage()
                    # page.setDefaultNavigationTimeout(60000)  # 设置为60秒
                    # url = "https://mp.weixin.qq.com/s/6VBXs19icV0O5hT7cHYwgw"
                    url = os.getcwd()+f"/{name}"
                    # url = "https://mp.weixin.qq.com/s/S24LAiMtAfdGS9XM0ZMU2A"
                    # 查看当前 桌面视图大小 https://miyakogi.github.io/pyppeteer/reference.html
                    #tk = tkinter.Tk()
                    #width = tk.winfo_screenwidth()
                    #height = tk.winfo_screenheight()
                    #tk.quit()
                    #print(f'设置窗口为：width：{width} height：{height}')
                    # await asyncio.sleep(4.12)
                    # 设置网页 视图大小
                    #await page.setViewport(viewport={'width': width, 'height': height})
                    #参数 https://ld246.com/article/1566221786951  https://blog.csdn.net/weixin_45961774/article/details/112848584
                    #await page.evaluateOnNewDocument('function(){Object.defineProperty(navigator, "webdriver", {get: () => undefined})}')
                    #await page.setExtraHTTPHeaders(headers={"referer":"https://weibo.com"})
                    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36')
                    await page.goto(url)
                    # page_text = await page.content()  # 页面内容
                    # cookies = await page.cookies()
                    await page.evaluate('''async () => {
                    await new
                Promise((resolve, reject) => {
                    var
                totalHeight = 0;
                var
                distance = 100;
                var
                timer = setInterval(() => {
                    var
                scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight >= scrollHeight){
                clearInterval(timer);
                resolve();
                }
                }, 200);
                });
                   }''')
                    # 等待页面加载完成
                    # await page.waitForNavigation()
                    await page.pdf({"path": 'pdf/'+name.replace('.html', '')+'.pdf', "format": 'A4'})
                    await page.close()
                except Exception as e:
                    if not os.path.exists('failed'):
                        os.mkdir('failed')
                    shutil.copy(name, 'failed')
                    # Navigation Timeout Exceeded: 30000 ms exceeded
                    print('下载失败',e,name)
        # break
        # htmls += [name for name in files if name.endswith(".html")]
        await browser.close()
    # print(htmls)
async def main2():
    for root, dirs, files in os.walk('.'):
        files.sort(reverse = True)
        for name in files:
            if name.endswith(".html"):
                print(name,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                try:
                    pdf_file = 'pdf/'+name.replace('.html', '')+'.pdf'
                    os.system(f'playwright pdf {name} {pdf_file}')
                    # os.system(f'wkhtmltopdf {name} {pdf_file}')
                except Exception as e:
                    print(e)
        # break
        # htmls += [name for name in files if name.endswith(".html")]
    # print(htmls)
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())