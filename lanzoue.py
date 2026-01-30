import os
import re
import json
import time
import base64
import argparse
import traceback
import requests
import execjs  # PyExecJS
from tqdm import tqdm
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Tuple, Any
from urllib.parse import urlparse, parse_qs, unquote
from html import unescape
class LanzouDownloader:
    
    def __init__(self, timeout: int = 30, debug: bool = False):
        """
        初始化下载器
         
        Args:
            timeout: 请求超时时间
            debug: 是否启用调试模式
        """
        self.timeout = timeout
        self.debug = debug
        self.session = self._create_session()
        self.cookies = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
         
        if self.debug:
            print(f"[DEBUG] 初始化下载器，超时时间: {timeout}秒")
            print("[DEBUG] 注意：此版本专门处理蓝奏云的反爬虫机制")
    
    def _create_session(self) -> requests.Session:
        """创建带重试机制的session"""
        if self.debug:
            print("[DEBUG] 创建带重试机制的session")
         
        session = requests.Session()
        retry = Retry(
            total=5,
            read=5,
            connect=5,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def _request(self, url: str, method: str = 'GET', data: Optional[Dict] = None,
                 headers: Optional[Dict] = None, allow_redirects: bool = True,
                 stream: bool = False) -> requests.Response:
        """发送请求"""
        if self.debug:
            print(f"[DEBUG] 发送请求: {method} {url}")
            if data:
                print(f"[DEBUG] 请求数据: {data}")
         
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
         
        try:
            if method.upper() == 'GET':
                response = self.session.get(
                    url,
                    headers=request_headers,
                    cookies=self.cookies,
                    timeout=self.timeout,
                    allow_redirects=allow_redirects,
                    stream=stream
                )
            else:
                response = self.session.post(
                    url,
                    headers=request_headers,
                    cookies=self.cookies,
                    data=data,
                    timeout=self.timeout,
                    allow_redirects=allow_redirects,
                    stream=stream
                )
             
            if self.debug:
                print(f"[DEBUG] 响应状态码: {response.status_code}")
                print(f"[DEBUG] 响应URL: {response.url}")
                print(f"[DEBUG] 响应头: {dict(response.headers)}")
                if self.debug and len(response.text) < 500:
                    print(f"[DEBUG] 响应预览: {response.text[:300]}...")
             
            # 更新cookies
            self.cookies.update(response.cookies.get_dict())
            if self.debug and self.cookies:
                print(f"[DEBUG] 更新cookies: {self.cookies}")
             
            return response
             
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] 请求异常: {e}")
                traceback.print_exc()
            raise
    
    def parse_acw_sc_v2_javascript(self, html_content: str) -> Optional[str]:
        """
        解析并执行 acw_sc__v2 的 JavaScript 代码
        这是蓝奏云的反爬虫机制
        """
        if self.debug:
            print("[DEBUG] 尝试解析 acw_sc__v2 JavaScript 代码")
         
        # 查找 JavaScript 代码
        script_pattern = r'<script[^>*>([\s\S*?)</script>'
        scripts = re.findall(script_pattern, html_content)
         
        if not scripts:
            if self.debug:
                print("[DEBUG] 未找到 JavaScript 代码")
            return None
         
        # 找到包含 acw_sc__v2 的脚本
        target_script = None
        for script in scripts:
            if 'acw_sc__v2' in script or '_0x4818' in script:
                target_script = script
                break
         
        if not target_script:
            if self.debug:
                print("[DEBUG] 未找到 acw_sc__v2 相关代码")
            return None
         
        if self.debug:
            print("[DEBUG] 找到 acw_sc__v2 JavaScript 代码")
            print(f"[DEBUG] 脚本长度: {len(target_script)} 字符")
         
        # 提取 arg1
        arg1_pattern = r"var\s+arg1\s*=\s*'([^'+)'"
        arg1_match = re.search(arg1_pattern, target_script)
         
        if not arg1_match:
            if self.debug:
                print("[DEBUG] 未找到 arg1 参数")
            return None
         
        arg1 = arg1_match.group(1)
         
        if self.debug:
            print(f"[DEBUG] 提取到 arg1: {arg1}")
         
        try:
            # 提取 posList - 修复：手动解析十六进制数组
            pos_pattern = r'var\s+posList\s*=\s*\[([^+)'
            pos_match = re.search(pos_pattern, target_script)
             
            if not pos_match:
                if self.debug:
                    print("[DEBUG] 未找到 posList")
                return None
             
            # 手动解析包含十六进制数的数组
            pos_list_str = pos_match.group(1)
            # 分割字符串并转换十六进制为十进制
            pos_list = []
            for item in pos_list_str.split(','):
                item = item.strip()
                if item.startswith('0x'):
                    # 十六进制转换为十进制
                    pos_list.append(int(item, 16))
                else:
                    # 十进制直接转换
                    pos_list.append(int(item))
             
            if self.debug:
                print(f"[DEBUG] 位置列表: {pos_list}")
                print(f"[DEBUG] 位置列表长度: {len(pos_list)}")
             
            # 提取 mask - 从 _0x3e9e 数组中提取
            # 查找 _0x3e9e 数组
            str_array_pattern = r"var\s+_0x3e9e\s*=\s*(\[[^)"
            str_array_match = re.search(str_array_pattern, target_script)
             
            if str_array_match:
                str_array_str = str_array_match.group(1)
                # 手动解析数组，处理引号问题
                str_array = []
                in_quotes = False
                current_str = ""
                for i, char in enumerate(str_array_str):
                    if char == "'" or char == '"':
                        if in_quotes:
                            if current_str:
                                str_array.append(current_str)
                                current_str = ""
                            in_quotes = False
                        else:
                            in_quotes = True
                    elif in_quotes:
                        current_str += char
                
                if self.debug:
                    print(f"[DEBUG] 找到字符串数组，长度: {len(str_array)}")
                    print(f"[DEBUG] 字符串数组: {str_array}")
                
                # 解码 base64 字符串
                decoded_strings = []
                for s in str_array:
                    try:
                        # 确保字符串是有效的base64
                        s = s.strip()
                        if s:
                            # 添加必要的填充
                            missing_padding = len(s) % 4
                            if missing_padding:
                                s += '=' * (4 - missing_padding)
                            decoded = base64.b64decode(s).decode('utf-8')
                            decoded_strings.append(decoded)
                    except Exception as e:
                        if self.debug:
                            print(f"[DEBUG] 解码失败: {s}, 错误: {e}")
                        decoded_strings.append(s)
                
                if self.debug:
                    print(f"[DEBUG] 解码后的字符串: {decoded_strings}")
                
                # 根据代码逻辑，mask 应该是最后一个元素之前的某个
                # 通常 mask 是类似 "3000176000856006061501533003690027800375" 的字符串
                mask = None
                for s in decoded_strings:
                    if len(s) == 40 and all(c in '0123456789abcdefABCDEF' for c in s):
                        mask = s
                        break
                
                if not mask:
                    # 如果找不到，使用默认值
                    mask = "3000176000856006061501533003690027800375"
            else:
                # 如果找不到字符串数组，使用默认值
                mask = "3000176000856006061501533003690027800375"
             
            if self.debug:
                print(f"[DEBUG] 使用的 mask: {mask}")
             
            # 重新排列 arg1 - 根据 posList 重新排列字符
            out_put_list = [''] * len(pos_list)
             
            for i, char in enumerate(arg1):
                target_pos = i + 1  # JavaScript 中索引从1开始
                if target_pos in pos_list:
                    idx = pos_list.index(target_pos)
                    out_put_list[idx] = char
             
            arg2 = ''.join(out_put_list)
             
            if self.debug:
                print(f"[DEBUG] 重新排列后的 arg2: {arg2}")
                print(f"[DEBUG] arg2 长度: {len(arg2)}, mask 长度: {len(mask)}")
             
            # XOR 操作
            arg3 = ''
            # 确保我们只处理有效长度
            min_len = min(len(arg2), len(mask))
            # 确保是偶数长度
            if min_len % 2 != 0:
                min_len -= 1
             
            for i in range(0, min_len, 2):
                if i + 2 <= len(arg2) and i + 2 <= len(mask):
                    try:
                        str_char = int(arg2[i:i+2], 16)
                        mask_char = int(mask[i:i+2], 16)
                        xor_char = str_char ^ mask_char
                        hex_str = hex(xor_char)[2:]  # 去掉 '0x' 前缀
                        if len(hex_str) == 1:
                            hex_str = '0' + hex_str
                        arg3 += hex_str
                    except ValueError:
                        if self.debug:
                            print(f"[DEBUG] XOR 错误在位置 {i}: arg2={arg2[i:i+2]}, mask={mask[i:i+2]}")
             
            if self.debug:
                print(f"[DEBUG] XOR 后的 arg3: {arg3}")
                print(f"[DEBUG] arg3 长度: {len(arg3)}")
             
            # 构建 cookie 值
            return arg3
             
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] 解析 JavaScript 失败: {e}")
                traceback.print_exc()
            return None
    
    def bypass_cloudflare(self, url: str) -> bool:
        """
        尝试绕过 Cloudflare 保护
        """
        if self.debug:
            print(f"[DEBUG] 尝试绕过 Cloudflare 保护: {url}")
         
        try:
            # 第一次请求，获取 JavaScript 挑战
            response = self._request(url, allow_redirects=False)
             
            # 检查是否被重定向或返回了挑战页面
            if response.status_code in [301, 302, 303, 307, 308]:
                location = response.headers.get('Location')
                if location:
                    if self.debug:
                        print(f"[DEBUG] 被重定向到: {location}")
                    return True
             
            # 检查响应内容
            content = response.text
             
            # 检查是否是 JavaScript 挑战
            if 'acw_sc__v2' in content or 'cloudflare' in content.lower() or 'challenge' in content.lower():
                if self.debug:
                    print("[DEBUG] 检测到 Cloudflare/反爬虫挑战")
                
                # 尝试解析 JavaScript 并获取 cookie
                arg3 = self.parse_acw_sc_v2_javascript(content)
                
                if arg3:
                    if self.debug:
                        print(f"[DEBUG] 成功获取 acw_sc__v2 值: {arg3}")
                     
                    # 设置 cookie
                    self.cookies['acw_sc__v2'] = arg3
                    self.session.cookies.set('acw_sc__v2', arg3)
                     
                    # 等待一段时间，模拟浏览器
                    time.sleep(3)
                     
                    # 重新请求
                    response2 = self._request(url)
                     
                    # 检查是否成功
                    if response2.status_code == 200 and 'acw_sc__v2' not in response2.text:
                        if self.debug:
                            print("[DEBUG] 成功绕过 Cloudflare 保护")
                        return True
                    else:
                        if self.debug:
                            print("[DEBUG] 绕过失败，响应可能仍然包含挑战")
                            if len(response2.text) < 500:
                                print(f"[DEBUG] 响应内容: {response2.text}")
                
                # 尝试使用 execjs 执行 JavaScript
                if self.debug:
                    print("[DEBUG] 尝试使用 execjs 执行 JavaScript...")
                
                try:
                    # 提取 JavaScript 代码
                    script_pattern = r'<script[^>*>([\s\S*?)</script>'
                    scripts = re.findall(script_pattern, content)
                    js_code = None
                    for script in scripts:
                        if 'acw_sc__v2' in script or '_0x4818' in script:
                            js_code = script
                            break
                     
                    if js_code:
                        # 使用 execjs 执行
                        ctx = execjs.compile(js_code)
                         
                        # 尝试获取 cookie
                        try:
                            # 在 JavaScript 代码后面添加获取 cookie 的代码
                            js_code += """
                            function getCookie() {
                                var expiredate = new Date();
                                expiredate.setTime(expiredate.getTime() + 1000 * 3600);
                                var theHost = location.host;
                                var theHostSplit = theHost.split(".");
                                var theHostSplitLength = theHostSplit.length;
                                if (!/^(\\d+\\.)*\\d+$/.test(theHost) && theHostSplitLength > 2 && ("com.cn" != (theHost = theHostSplit[theHostSplitLength-2] + "." + theHostSplit[theHostSplitLength-1]) && "gov.cn" != theHost && "org.cn" != theHost && "net.cn" != theHost && "com.my" != theHost || (theHost = theHostSplit[theHostSplitLength-3] + "." + theHost))) {}
                                return 'acw_sc__v2=' + arg3 + '; expires=' + expiredate.toGMTString() + '; max-age=3600; path=/; domain=' + theHost;
                            }
                            getCookie();
                            """
                            
                            ctx = execjs.compile(js_code)
                            cookie_str = ctx.call('getCookie')
                            
                            # 解析 cookie
                            match = re.search(r'acw_sc__v2=([^;+)', cookie_str)
                            if match:
                                arg3 = match.group(1)
                                self.cookies['acw_sc__v2'] = arg3
                                self.session.cookies.set('acw_sc__v2', arg3)
                                 
                                time.sleep(2)
                                response3 = self._request(url)
                                 
                                if response3.status_code == 200 and 'acw_sc__v2' not in response3.text:
                                    if self.debug:
                                        print("[DEBUG] 通过 execjs 成功绕过保护")
                                    return True
                        except Exception as e:
                            if self.debug:
                                print(f"[DEBUG] execjs 执行失败: {e}")
                except Exception as e:
                    if self.debug:
                        print(f"[DEBUG] 使用 execjs 异常: {e}")
                
                # 尝试其他方法：模拟浏览器等待
                if self.debug:
                    print("[DEBUG] 尝试模拟浏览器等待...")
                
                time.sleep(5)
                
                # 再次请求
                response3 = self._request(url)
                
                if response3.status_code == 200 and 'acw_sc__v2' not in response3.text:
                    if self.debug:
                        print("[DEBUG] 通过等待绕过保护")
                    return True
             
            # 如果状态码是 200 且没有挑战，直接成功
            if response.status_code == 200:
                return True
             
            return False
             
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] 绕过 Cloudflare 失败: {e}")
            return False
    
    def parse_share_url(self, url: str) -> Tuple[str, Optional[str]]:
        """
        解析分享链接
         
        Args:
            url: 分享链接
             
        Returns:
            (文件ID, 密码)
        """
        if self.debug:
            print(f"[DEBUG] 解析分享URL: {url}")
         
        # 提取文件ID
        pattern = r'(?:lanzou[a-z?\.com|woozooo\.com)/(?:i|s|b)?([a-zA-Z0-9+)'
        match = re.search(pattern, url)
         
        if not match:
            if self.debug:
                print("[DEBUG] 正则匹配失败，尝试从路径中提取")
             
            # 尝试从路径中提取
            path = urlparse(url).path
            file_id = path.strip('/').split('/')[-1]
            if len(file_id) >= 6:
                if self.debug:
                    print(f"[DEBUG] 从路径提取文件ID: {file_id}")
                return file_id, None
            else:
                raise ValueError(f"无法从URL中提取文件ID: {url}")
         
        file_id = match.group(1)
         
        if self.debug:
            print(f"[DEBUG] 正则提取文件ID: {file_id}")
         
        # 提取密码
        password = None
        if '?pwd=' in url or '?password=' in url or '?passwd=' in url:
            query = urlparse(url).query
            params = parse_qs(query)
            for key in ['pwd', 'password', 'passwd']:
                if key in params:
                    password = params[key][0]
                    if self.debug:
                        print(f"[DEBUG] 从URL提取密码: {password}")
                    break
         
        return file_id, password
    
    def get_file_info(self, share_url: str) -> Dict:
        """
        获取文件信息 - 新版方法
        """
        if self.debug:
            print(f"[DEBUG] 开始获取文件信息: {share_url}")
         
        file_id, password = self.parse_share_url(share_url)
        info = {'id': file_id, 'password': password}
         
        if self.debug:
            print(f"[DEBUG] 文件ID: {file_id}, 密码: {password or '无'}")
         
        # 先尝试绕过 Cloudflare
        if not self.bypass_cloudflare(share_url):
            raise Exception("无法绕过 Cloudflare 保护，请稍后重试")
         
        # 获取页面内容
        headers = {
            'Referer': 'https://www.lanzou.com/',
            'Origin': 'https://www.lanzou.com',
        }
         
        response = self._request(share_url, headers=headers)
         
        if response.status_code != 200:
            raise Exception(f"无法访问分享页面: {share_url}")
         
        soup = BeautifulSoup(response.text, 'html.parser')
         
        # 检查是否需要密码
        password_indicators = ['输入密码', 'pwdload', '请输入提取码', '提取码', 'password', '输入访问码']
        needs_password = any(indicator in response.text for indicator in password_indicators)
         
        if needs_password:
            if self.debug:
                print("[DEBUG] 检测到需要密码")
             
            if not password:
                password = input(f"文件 {file_id} 需要密码，请输入: ")
                info['password'] = password
             
            # 尝试提交密码
            # 查找密码表单
            form = soup.find('form', {'id': 'pwdload'})
            if form:
                action = form.get('action', '')
                if not action.startswith('http'):
                    # 构建完整URL
                    base_url = urlparse(share_url)
                    action = f"{base_url.scheme}://{base_url.netloc}{action}"
                
                # 提取表单字段
                form_data = {}
                for input_tag in form.find_all('input'):
                    name = input_tag.get('name')
                    value = input_tag.get('value', '')
                    if name and name != 'pwd':
                        form_data[name] = value
                
                form_data['pwd'] = password
                
                if self.debug:
                    print(f"[DEBUG] 提交密码表单到: {action}")
                    print(f"[DEBUG] 表单数据: {form_data}")
                
                response = self._request(action, method='POST', data=form_data, headers=headers)
                
                if response.status_code != 200:
                    if self.debug:
                        print(f"[DEBUG] 密码验证失败，响应: {response.text[:200]}")
                    raise Exception("密码错误或验证失败")
                else:
                    if self.debug:
                        print("[DEBUG] 密码验证成功")
                     
                    # 更新soup
                    soup = BeautifulSoup(response.text, 'html.parser')
         
        # 保存原始页面内容用于分析
        page_content = response.text
         
        # 从页面中提取所有隐藏的表单字段
        form_fields = {}
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all('input')
            for input_tag in inputs:
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                if name:
                    form_fields[name] = value
         
        if self.debug and form_fields:
            print(f"[DEBUG] 找到的表单字段: {form_fields}")
         
        # 从页面中提取 sign 参数
        sign = None
        # 查找 sign input
        sign_input = soup.find('input', {'name': 'sign'})
        if sign_input:
            sign = sign_input.get('value')
        else:
            # 尝试从 JavaScript 中提取 sign
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'sign' in script.string:
                    # 尝试匹配 sign: 'xxx' 或 sign = 'xxx'
                    sign_match = re.search(r"sign\s*[:=\s*['\"]([^'\"+)['\"", script.string)
                    if sign_match:
                        sign = sign_match.group(1)
                        break
             
            if not sign:
                # 如果没有找到，使用文件ID
                sign = file_id
         
        # 尝试从页面中提取 ajaxdata
        ajax_data = None
        # 查找包含 ajaxdata 的脚本
        for script in soup.find_all('script'):
            if script.string and 'ajaxdata' in script.string:
                # 尝试匹配 ajaxdata = 'xxx'
                ajax_match = re.search(r"ajaxdata\s*=\s*['\"]([^'\"+)['\"", script.string)
                if ajax_match:
                    ajax_data = ajax_match.group(1)
                    break
         
        info['sign'] = sign
        info['ajax_data'] = ajax_data
        info['form_fields'] = form_fields
        info['page_content'] = page_content
         
        # 提取文件信息
        if self.debug:
            print(f"[DEBUG] 页面标题: {soup.title.string if soup.title else '无'}")
            print(f"[DEBUG] 提取到的 sign: {sign}")
            print(f"[DEBUG] 提取到的 ajax_data: {ajax_data}")
         
        # 提取文件名
        title_tag = soup.find('title')
        if title_tag:
            filename = title_tag.text.strip()
            if ' - 蓝奏云' in filename:
                filename = filename.replace(' - 蓝奏云', '')
            elif ' - 蓝奏网盘' in filename:
                filename = filename.replace(' - 蓝奏网盘', '')
            info['filename'] = filename
             
            if self.debug:
                print(f"[DEBUG] 提取文件名: {filename}")
        else:
            # 尝试从其他位置提取文件名
            filename_selectors = [
                ('meta', {'property': 'og:title'}),
                ('meta', {'name': 'description'}),
                ('div', {'class': 'md'}),
                ('h3', {}),
                ('h4', {}),
                ('span', {'class': 'file-name'}),
            ]
             
            for tag_name, attrs in filename_selectors:
                element = soup.find(tag_name, attrs)
                if element and element.get_text().strip():
                    filename = element.get_text().strip()
                    info['filename'] = filename
                    if self.debug:
                        print(f"[DEBUG] 从{tag_name}提取文件名: {filename}")
                    break
             
            if 'filename' not in info:
                # 使用文件ID作为文件名
                info['filename'] = f'file_{file_id}'
                if self.debug:
                    print(f"[DEBUG] 未找到文件名，使用默认: {info['filename']}")
         
        # 提取文件大小
        size_patterns = [
            r'文件大小[：:\s*([\d\.+\s*[BKMGT?)',
            r'size[：:\s*([\d\.+\s*[BKMGT?)',
            r'文件大小\s*</span>\s*<span[^>*>([^<+)</span>',
            r'大小\s*</span>\s*<span[^>*>([^<+)</span>',
        ]
         
        for pattern in size_patterns:
            size_match = re.search(pattern, response.text)
            if size_match:
                info['size'] = size_match.group(1).strip()
                if self.debug:
                    print(f"[DEBUG] 提取文件大小: {info['size']}")
                break
        else:
            info['size'] = '未知'
            if self.debug:
                print("[DEBUG] 未找到文件大小信息")
         
        # 保存页面内容用于调试
        if self.debug:
            debug_dir = "debug_pages"
            os.makedirs(debug_dir, exist_ok=True)
            debug_file = os.path.join(debug_dir, f"{file_id}_page_final.html")
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"[DEBUG] 最终页面已保存到: {debug_file}")
             
            # 也保存清理后的HTML用于分析
            debug_file_clean = os.path.join(debug_dir, f"{file_id}_clean_final.html")
            with open(debug_file_clean, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f"[DEBUG] 格式化最终页面已保存到: {debug_file_clean}")
         
        return info
    
    def get_direct_url(self, file_info: Dict) -> str:
        """
        获取直接下载链接 - 新版方法
        """
        if self.debug:
            print(f"[DEBUG] 开始获取直接下载链接")
            print(f"[DEBUG] 文件信息: {file_info}")
         
        file_id = file_info['id']
        sign = file_info.get('sign', file_id)
        ajax_data = file_info.get('ajax_data')
         
        # 如果页面中没有提供ajaxdata，我们需要分析页面内容来获取
        if not ajax_data:
            # 从页面内容中提取ajaxdata
            page_content = file_info.get('page_content', '')
            if page_content:
                # 尝试从页面中提取ajaxdata
                ajax_patterns = [
                    r'ajaxdata\s*=\s*["\']([^"\'+)["\'',
                    r'data\s*:\s*["\']([^"\'+)["\'',
                ]
                
                for pattern in ajax_patterns:
                    match = re.search(pattern, page_content)
                    if match:
                        ajax_data = match.group(1)
                        break
         
        # 尝试使用不同的API端点
        endpoints = [
            f"https://wwa.lanzoue.com/ajaxm.php",
            f"https://wwa.lanzoui.com/ajaxm.php",
        ]
         
        # 尝试不同的请求数据组合
        data_templates = []
         
        # 模板1: 使用 sign 和 ves
        data_templates.append({
            'action': 'downprocess',
            'sign': sign,
            'ves': '1',
        })
         
        # 模板2: 如果页面中有ajaxdata，尝试使用
        if ajax_data:
            data_templates.append({
                'action': 'downprocess',
                'sign': sign,
                'ves': '1',
                'websign': ajax_data,
            })
             
            # 模板3: 只使用ajaxdata作为sign
            data_templates.append({
                'action': 'downprocess',
                'sign': ajax_data,
                'ves': '1',
            })
         
        # 模板4: 使用页面中的表单字段
        form_fields = file_info.get('form_fields', {})
        if form_fields:
            data_templates.append(form_fields)
         
        headers = {
            'Referer': f'https://wwa.lanzoue.com/{file_id}',
            'Origin': 'https://wwa.lanzoue.com',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
         
        for endpoint in endpoints:
            for data_template in data_templates:
                try:
                    if self.debug:
                        print(f"[DEBUG] 尝试API请求: {endpoint}")
                        print(f"[DEBUG] 请求数据: {data_template}")
                     
                    response = self._request(endpoint, method='POST', data=data_template, headers=headers)
                     
                    if response.status_code != 200:
                        if self.debug:
                            print(f"[DEBUG] API请求失败: {response.status_code}")
                        continue
                     
                    # 解析响应
                    try:
                        result = response.json()
                         
                        if self.debug:
                            print(f"[DEBUG] API响应: {result}")
                         
                        if result.get('zt') == 1:
                            dom = result.get('dom', '').replace('\\', '')
                            url = result.get('url', '')
                            
                            if dom and url:
                                download_url = f"{dom}/file/{url}"
                                if self.debug:
                                    print(f"[DEBUG] 从API获取下载链接: {download_url}")
                                return download_url
                            else:
                                continue  # 尝试下一个数据模板
                        else:
                            error_msg = result.get('inf', '未知错误')
                            if self.debug:
                                print(f"[DEBUG] API返回错误: {error_msg}")
                            continue  # 尝试下一个数据模板
                            
                    except json.JSONDecodeError:
                        if self.debug:
                            print(f"[DEBUG] 响应不是JSON: {response.text[:200]}")
                        continue  # 尝试下一个数据模板
                         
                except Exception as e:
                    if self.debug:
                        print(f"[DEBUG] API请求异常: {e}")
                    continue  # 尝试下一个端点或数据模板
         
        # 如果所有方法都失败，尝试从页面中直接提取下载链接
        return self._extract_direct_url_from_page(file_info)
    
    def _extract_direct_url_from_page(self, file_info: Dict) -> str:
        """
        从页面中直接提取下载链接
        """
        if self.debug:
            print("[DEBUG] 尝试从页面中提取下载链接")
         
        file_id = file_info['id']
        page_content = file_info.get('page_content', '')
         
        if not page_content:
            raise Exception("没有页面内容可用于分析")
         
        # 尝试从页面中提取直接下载链接
        # 蓝奏云通常会将下载链接放在JavaScript中
         
        # 模式1: 查找包含文件ID和域名的URL
        patterns = [
            r'https?://[^/+/file/[^\'"+',
            r'https?://[^/+/tp/[^\'"+',
            r'https?://[^/+/\?[^\'"+',
            r'downprocess[^}+dom["\':\s*["\']([^"\'+)["\'][^}+url["\':\s*["\']([^"\'+)["\'',
            r'\"dom\"\s*:\s*\"([^\"+)\"[^}+"url\"\s*:\s*\"([^\"+)\"',
        ]
         
        for pattern in patterns:
            matches = re.findall(pattern, page_content)
            for match in matches:
                if isinstance(match, tuple) and len(match) == 2:
                    dom, url = match
                    download_url = f"{dom}/file/{url}"
                    if self.debug:
                        print(f"[DEBUG] 从页面提取下载链接: {download_url}")
                    return download_url
                elif isinstance(match, str):
                    download_url = match
                    if '/file/' in download_url or '/tp/' in download_url:
                        if self.debug:
                            print(f"[DEBUG] 从页面提取下载链接: {download_url}")
                        return download_url
         
        # 如果页面中没有直接链接，尝试使用备用方法
        # 重新请求页面，查看是否有跳转
        share_url = f"https://wwa.lanzoue.com/{file_id}"
         
        # 设置特殊的headers模拟浏览器点击下载按钮
        headers = {
            'Referer': share_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
         
        # 尝试直接访问一个可能的下载端点
        download_endpoints = [
            f"https://wwa.lanzoue.com/tp/{file_id}",
            f"https://wwa.lanzoui.com/tp/{file_id}",
            f"https://developer-oss.lanrar.com/file/{file_id}",
        ]
         
        for endpoint in download_endpoints:
            try:
                if self.debug:
                    print(f"[DEBUG] 尝试直接访问下载端点: {endpoint}")
                
                response = self._request(endpoint, headers=headers, allow_redirects=False)
                
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location')
                    if location:
                        if self.debug:
                            print(f"[DEBUG] 从重定向获取下载链接: {location}")
                        return location
                
                if response.status_code == 200:
                    # 检查响应内容是否包含下载链接
                    content = response.text
                    url_patterns = [
                        r'https?://[^"\'>+',
                        r'location\.href\s*=\s*["\']([^"\'+)["\'',
                        r'window\.open\(["\']([^"\'+)["\'',
                    ]
                     
                    for pattern in url_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            if '/file/' in match or 'http' in match:
                                if self.debug:
                                    print(f"[DEBUG] 从响应内容提取下载链接: {match}")
                                return match
            except Exception as e:
                if self.debug:
                    print(f"[DEBUG] 访问端点 {endpoint} 失败: {e}")
                continue
         
        # 如果所有方法都失败
        raise Exception("无法获取下载链接，页面可能已过期或需要重新加载")
    
    def download_file(self, url: str, output_path: Optional[str] = None,
                     chunk_size: int = 8192, resume: bool = True) -> str:
        """
        下载文件
        """
        if self.debug:
            print(f"[DEBUG] 开始下载流程")
            print(f"[DEBUG] 输入URL: {url}")
            print(f"[DEBUG] 输出路径: {output_path}")
            print(f"[DEBUG] 分块大小: {chunk_size}")
            print(f"[DEBUG] 断点续传: {resume}")
         
        # 获取文件信息
        print("正在解析文件信息...")
        try:
            file_info = self.get_file_info(url)
        except Exception as e:
            print(f"获取文件信息失败: {e}")
            if self.debug:
                traceback.print_exc()
            raise
         
        print(f"文件信息:")
        for key, value in file_info.items():
            if key not in ['ajax_data', 'form_fields', 'page_content']:  # 不显示敏感数据
                print(f"  {key}: {value}")
         
        # 获取直接下载链接
        print("正在获取下载链接...")
        try:
            direct_url = self.get_direct_url(file_info)
            print(f"下载链接已获取")
            if self.debug:
                print(f"[DEBUG] 下载链接: {direct_url}")
        except Exception as e:
            print(f"获取下载链接失败: {e}")
            if self.debug:
                traceback.print_exc()
             
            debug_dir = "debug_pages"
            if os.path.exists(debug_dir):
                print(f"调试HTML文件目录 '{debug_dir}'")
             
            raise
         
        # 确定输出路径
        if not output_path:
            filename = file_info.get('filename', f'file_{file_info["id"]}')
            output_path = filename
        elif os.path.isdir(output_path):
            filename = file_info.get('filename', f'file_{file_info["id"]}')
            output_path = os.path.join(output_path, filename)
         
        if self.debug:
            print(f"[DEBUG] 最终输出路径: {output_path}")
         
        # 检查文件是否已存在
        if os.path.exists(output_path) and resume:
            file_size = os.path.getsize(output_path)
            if self.debug:
                print(f"[DEBUG] 文件已存在，大小: {file_size} 字节")
             
            headers = {'Range': f'bytes={file_size}-'}
            mode = 'ab'
        else:
            file_size = 0
            headers = {}
            mode = 'wb'
            if self.debug and os.path.exists(output_path):
                print(f"[DEBUG] 文件已存在，但断点续传未启用，将覆盖")
         
        # 设置请求头
        headers.update({
            'User-Agent': self.headers['User-Agent'],
            'Referer': f'https://wwa.lanzoue.com/{file_info["id"]}',
            'Accept-Encoding': 'identity',
        })
         
        if self.debug:
            print(f"[DEBUG] 下载请求头: {headers}")
         
        # 发送请求
        try:
            if self.debug:
                print(f"[DEBUG] 发送下载请求到: {direct_url}")
             
            response = self.session.get(
                direct_url,
                headers=headers,
                stream=True,
                timeout=self.timeout,
                cookies=self.cookies
            )
             
            if self.debug:
                print(f"[DEBUG] 下载响应状态码: {response.status_code}")
                print(f"[DEBUG] 下载响应头: {dict(response.headers)}")
             
            if response.status_code not in [200, 206]:
                if self.debug:
                    print(f"[DEBUG] 下载失败，响应内容: {response.text[:500]}")
                raise Exception(f"下载失败: HTTP {response.status_code}")
             
            # 获取文件总大小
            content_length = response.headers.get('content-length')
            if content_length:
                content_length = int(content_length)
                total_size = content_length + file_size
                if self.debug:
                    print(f"[DEBUG] 服务器返回的文件大小: {content_length} 字节")
                    print(f"[DEBUG] 断点续传已下载: {file_size} 字节")
                    print(f"[DEBUG] 总下载大小: {total_size} 字节")
            else:
                total_size = 0
                if self.debug:
                    print("[DEBUG] 服务器未返回content-length")
             
            # 下载文件
            print(f"开始下载: {os.path.basename(output_path)}")
             
            with open(output_path, mode) as f:
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    initial=file_size,
                    desc=os.path.basename(output_path)
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
             
            final_size = os.path.getsize(output_path)
            if self.debug:
                print(f"[DEBUG] 下载完成，文件最终大小: {final_size} 字节")
             
            print(f"下载完成: {output_path}")
            return output_path
             
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] 下载过程异常: {e}")
                traceback.print_exc()
             
            # 检查文件是否部分下载
            if os.path.exists(output_path):
                partial_size = os.path.getsize(output_path)
                print(f"下载中断，已下载 {partial_size} 字节")
             
            raise
def main():
    parser = argparse.ArgumentParser(description='蓝奏云下载工具 - 反爬虫版本')
    parser.add_argument('url', help='分享链接')
    parser.add_argument('-o', '--output', help='输出路径（文件或目录）')
    parser.add_argument('-t', '--timeout', type=int, default=30, help='请求超时时间（秒）')
    parser.add_argument('-r', '--resume', action='store_true', help='断点续传')
    parser.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
    parser.add_argument('-p', '--password', help='文件密码（如果需要）')
    
    args = parser.parse_args()
    
    if not args.url:
        parser.print_help()
        return
    
    try:
        if args.debug:
            print(f"[DEBUG] 命令行参数: {args}")
         
        # 创建下载器
        downloader = LanzouDownloader(timeout=args.timeout, debug=args.debug)
         
        # 如果提供了密码，将其添加到URL中
        url = args.url
        if args.password:
            if '?' in url:
                url += f'&pwd={args.password}'
            else:
                url += f'?pwd={args.password}'
         
        # 下载文件
        downloader.download_file(
            url=url,
            output_path=args.output,
            resume=args.resume
        )
    
    except KeyboardInterrupt:
        print("\n用户中断下载")
    except Exception as e:
        print(f"错误: {e}")
        if args.debug:
            traceback.print_exc()
if __name__ == '__main__':
    main()