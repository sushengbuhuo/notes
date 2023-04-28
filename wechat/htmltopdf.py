import asyncio,os
from pyppeteer import launch
import tkinter
from urllib import parse
if not os.path.exists('pdf'):
    os.mkdir('pdf')
async def main():
    for root, dirs, files in os.walk('.'):
        files.sort(reverse = True)
        for name in files:
            if name.endswith(".html"):
                print(name)
                name=parse.quote(name)
                try:
                    browser = await launch()
                    page = await browser.newPage()
                    # url = "https://mp.weixin.qq.com/s/6VBXs19icV0O5hT7cHYwgw"
                    url = os.getcwd()+f"/{name}"
                    # url = "https://mp.weixin.qq.com/s/S24LAiMtAfdGS9XM0ZMU2A"
                    # 查看当前 桌面视图大小 https://miyakogi.github.io/pyppeteer/reference.html
                    #tk = tkinter.Tk()
                    #width = tk.winfo_screenwidth()
                    #height = tk.winfo_screenheight()
                    #tk.quit()
                    #print(f'设置窗口为：width：{width} height：{height}')
                    # 设置网页 视图大小
                    #await page.setViewport(viewport={'width': width, 'height': height})
                    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36')
                    # await page.setExtraHTTPHeaders({"referer":"https://weibo.com/"})
                    await page.goto(url)
                    # page_text = await page.content()  # 页面内容
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
                    await page.pdf({"path": 'pdf/'+parse.unquote(name).replace('.html', '')+'.pdf', "format": 'A4'})
                    await browser.close()
                except Exception as e:
                    print(e)
        # break
        # htmls += [name for name in files if name.endswith(".html")]
    # print(htmls)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())