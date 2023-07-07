from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     for browser_type in [p.chromium]:
#         browser = browser_type.launch(headless=False)
#         page = browser.new_page()
#         page.goto('https://www.baidu.com')
#         page.wait_for_load_state('networkidle')
    # html = page.content()
    # href = page.get_attribute('a.name', 'href')
    # elements = page.query_selector_all('a.name')
    # element = page.query_selector('a.name')
    # for element in elements:
    #     print(element.get_attribute('href'))
    #     print(element.text_content())
#         page.screenshot(path=f'screenshot-{browser_type.name}.png', full_page=True)
#         print(page.title())
#         browser.close()

# playwright codegen -o script.py -b firefox
def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.baidu.com/
    page.goto("https://www.baidu.com/")

    # Click input[name="wd"]
    page.click("input[name=\"wd\"]")

    # Fill input[name="wd"]
    page.fill("input[name=\"wd\"]", "nba")

    # Click text=百度一下 
    with page.expect_navigation():
        page.click("text=百度一下")

    context.close()
    browser.close()
"""
我这边用模拟浏览器（playwright）完成了小红书X-s参数的获取，感兴趣可以看下，https://github.com/NanmiCoder/MediaCrawler
https://cuiqingcai.com/36045.html https://aitechtogether.com/python/50312.html 
playwright pdf  "2018-11-27-大佬的意图很明确.html" 2018-11-27-大佬的意图很明确.pdf
wkhtmltopdf "2018-11-27-大佬的意图很明确.html" 2018-11-27-大佬的意图很明确2.pdf
Web自动化办公Playwright 
https://www.52pojie.cn/thread-1543086-1-1.html
录制操作生成代码 https://cuiqingcai.com/36045.html
playwright codegen -o script.py -b firefox
playwright codegen -o pokemon.js --target javascript https://cn.bing.com
playwright screenshot --full-page www.baidu.com baidu-full.png
playwright screenshot \
    --device="iPhone 11" \
    --color-scheme=dark \
    --wait-for-timeout=3000 \
    twitter.com twitter-iphone.png
# 生成PDF
playwright pdf https://en.wikipedia.org/wiki/PDF wiki.pdf


"""
# with sync_playwright() as playwright:
#     run(playwright)
def on_response(response):
    # print(f'Statue {response.status}: {response.url}')
    if '/api/movie/' in response.url and response.status == 200:
        print(response.json())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.on('response', on_response)
    page.goto('https://spa6.scrape.center/')
    page.wait_for_load_state('networkidle')
    browser.close()


