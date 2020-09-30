from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 FirePHP/0.7.4",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "referer": "https://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=https%3A%2F%2Fweibo.com%2Ftv%2Fv%2FI9cdSBVBP&domain=.weibo.com&ua=php-sso_sdk_client-0.6.28&_rand=1569807841.8018"
}
#https://old-panda.com/2020/01/02/python-selenium-download-weibo-video/

def parse_weibo_video(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path="d:\download\chromedriver.exe", chrome_options=option)
    driver.get(url)
    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        user = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='player_info']//div[@class='clearfix']/a/span"))
        )
        return element.get_property("src"), user.text#视频标签出现之后，直接返回其 src 的值，即为视频链接
    finally:
        driver.quit()

print(parse_weibo_video('https://www.weibo.com/tv/v/In7Oce2uO'))        