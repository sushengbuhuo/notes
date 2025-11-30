import requests
from bs4 import BeautifulSoup
import time
import json
import argparse
import sys
 
#https://www.52pojie.cn/thread-2071590-1-1.html https://cnb.cool/IIIStudio/PYQianDao/tieba-demo
class TiebaSign:
    def __init__(self, tieba_cookie, pushplus_token, tbs=None):
        self.PUSHPLUS_URL = "https://www.pushplus.plus/send/"
        self.PUSHPLUS_TOKEN = pushplus_token
        self.sign_url = "https://tieba.baidu.com/sign/add"
        self.mylike_base_url = "https://tieba.baidu.com/f/like/mylike"
         
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "cookie": tieba_cookie,
            "host": "tieba.baidu.com",
            "pragma": "no-cache",
            "referer": "https://tieba.baidu.com/",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "\"Android\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
        }
         
        self.tbs = tbs or "0f40da5e9a52307a1752800824"
 
    def send_notification(self, title, content):
        """发送PushPlus通知"""
        payload = {
            "token": self.PUSHPLUS_TOKEN,
            "title": title,
            "content": content
        }
        try:
            res = requests.post(self.PUSHPLUS_URL, json=payload)
            if res.status_code == 200:
                print("通知发送成功")
                return True
            else:
                print(f"通知发送失败，状态码：{res.status_code}")
                return False
        except Exception:
            print("通知发送异常")
            return False
 
    def get_all_followed_tieba(self, session):
        """获取所有页面的关注贴吧，优化分页检测"""
        titles = []
        page = 1
        max_pages = 10
 
        while page <= max_pages:
            params = {"pn": page}
            try:
                timestamp = int(time.time() * 1000)
                params["t"] = timestamp
                response = session.get(self.mylike_base_url, params=params, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException:
                print(f"第{page}页请求失败")
                self.send_notification("贴吧列表分页请求失败", f"第{page}页获取失败")
                break
 
            soup = BeautifulSoup(response.text, 'html.parser')
            current_page_titles = []
             
            for a_tag in soup.select('a[href^="/f?kw="]:not(.like_badge)'):
                title = a_tag.get('title')
                if title and title not in titles:
                    current_page_titles.append(title)
                    titles.append(title)
 
            print(f"第{page}页获取到{len(current_page_titles)}个贴吧")
 
            has_next_page = False
            next_page_tags = soup.select('a[href*="pn={}"]'.format(page + 1))
            next_text_tags = soup.select('a:-soup-contains("下一页")')
            if next_page_tags or next_text_tags:
                has_next_page = True
 
            if len(current_page_titles) < 20:
                has_next_page = False
 
            if not has_next_page or len(current_page_titles) == 0:
                print(f"已获取所有页面（共{page}页），总贴吧数：{len(titles)}")
                break
 
            time.sleep(1.5)
            page += 1
 
        return titles
 
    def toSign(self, tbName, session):
        """签到单个贴吧，处理已签到情况"""
        if not tbName:
            return "参数错误：贴吧名称为空"
          
        try:
            data = {
                "ie": "utf-8",
                "kw": tbName,
                "tbs": self.tbs
            }
            res = session.post(url=self.sign_url, data=data, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            return "请求失败"
          
        try:
            json_data = res.json()
        except json.JSONDecodeError:
            return "响应格式错误，非JSON数据"
          
        if json_data.get("no") == 1101 or "已经签过了" in json_data.get("error", ""):
            return "已签到"
        elif json_data.get("no") == 0 or (json_data.get("data") and json_data["data"].get("errmsg") == "success"):
            return "签到成功"
        else:
            error_msg = json_data.get("error", "未知错误")
            return f"签到失败：{error_msg}（错误码：{json_data.get('no')}）"
 
    def run(self):
        """执行签到任务"""
        try:
            session = requests.Session()
            session.headers.update(self.headers)
              
            # 验证Cookie有效性
            test_response = session.get(self.mylike_base_url, params={"pn": 1}, timeout=10)
            if "请登录" in test_response.text:
                self.send_notification("贴吧签到失败", "Cookie无效或已过期，请重新登录获取Cookie")
                return False
              
            # 获取所有关注的贴吧
            all_tieba = self.get_all_followed_tieba(session)
            if not all_tieba:
                self.send_notification("贴吧签到完成", "未发现关注的贴吧，无需签到")
                return True
 
            # 逐个签到并统计结果
            sign_results = []
            success_count = 0
            already_signed_count = 0
            fail_count = 0
              
            for tb in all_tieba:
                result = self.toSign(tb, session)
                sign_results.append(f"{tb}：{result}")
                  
                if "签到成功" in result:
                    success_count += 1
                elif "已签到" in result:
                    already_signed_count += 1
                else:
                    fail_count += 1
                      
                time.sleep(1)
 
            # 汇总结果并发送通知
            content = "\n".join(sign_results)
            self.send_notification(
                f"贴吧签到汇总（共{len(all_tieba)}个）",
                f"成功：{success_count}个 | 已签到：{already_signed_count}个 | 失败：{fail_count}个\n\n{content}"
            )
            return True
 
        except Exception:
            error_msg = "程序异常"
            print(error_msg)
            self.send_notification("贴吧签到错误", error_msg)
            return False
 
 
def main():
    parser = argparse.ArgumentParser(description='百度贴吧自动签到脚本')
    parser.add_argument('--cookie', '-c', required=True, help='贴吧Cookie（必需）')
    parser.add_argument('--pushplus', '-p', required=True, help='PushPlus Token（必需）')
    parser.add_argument('--tbs', help='TBS参数（可选）', default="0f40da5e9a52307a1752800824")
     
    args = parser.parse_args()
     
    # 执行签到
    signer = TiebaSign(args.cookie, args.pushplus, args.tbs)
    success = signer.run()
     
    if success:
        print("贴吧签到任务完成")
    else:
        print("贴吧签到任务失败")
        sys.exit(1)
 
 
if __name__ == "__main__":
    main()