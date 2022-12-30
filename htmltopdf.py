import asyncio,os
from pyppeteer import launch
import tkinter
def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height
if not os.path.exists('pdf'):
    os.mkdir('pdf')
async def main():
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith(".html"):
                print(name)
                try:
                    browser = await launch()#await launch(headless=False)  # 开启浏览器界面可视模式 保存数据 launch(headless=False, userDataDir='./userdata', args=['--disable-infobars'])
                    page = await browser.newPage()
                    # url = "https://mp.weixin.qq.com/s/6VBXs19icV0O5hT7cHYwgw"
                    url = os.getcwd()+f"/{name}"
                    # url = "https://mp.weixin.qq.com/s/S24LAiMtAfdGS9XM0ZMU2A"
                    # 查看当前 桌面视图大小 https://miyakogi.github.io/pyppeteer/reference.html https://github.com/kiwi0fruit/pyppdf
                    #tk = tkinter.Tk()
                    #width = tk.winfo_screenwidth()
                    #height = tk.winfo_screenheight()
                    #tk.quit()
                    #print(f'设置窗口为：width：{width} height：{height}')

                    # 设置网页 视图大小https://zmister.com/archives/1611.html
                    #await page.setViewport(viewport={'width': width, 'height': height})
                    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36')
                    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})') #防止被检测到 WebDriver 
                    await page.goto(url)
                    # page_text = await page.content()  # 页面内容 await page.cookies()
                    # await page.screenshot(path='example.png')  # 截图
                    # await asyncio.sleep(100)
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
                }, 100);
                });
                   }''')
                    await page.pdf({"path": 'pdf/'+name.replace('.html', '')+'.pdf', "format": 'A4'})
                    await browser.close()
                except Exception as e:
                    print(e)
        # break
        # htmls += [name for name in files if name.endswith(".html")]
    # print(htmls)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())