import os
import sqlite3
import shutil
import win32crypt
from datetime import datetime, timedelta
import json
import base64
from Crypto.Cipher import AES
# pip install pycryptodome
def get_master_key():
    # 从本地状态文件获取主密钥 https://www.52pojie.cn/thread-2069673-1-1.html
    local_state_path = os.path.join(
        os.environ['USERPROFILE'],
        r'AppData\Local\Microsoft\Edge\User Data\Local State'
    )
     
    try:
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
         
        # 提取并解码主密钥
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        # 移除DPAPI前缀
        encrypted_key = encrypted_key[5:]
        # 使用CryptUnprotectData解密主密钥
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        print(f"获取主密钥失败: {str(e)}")
        return None
 
def decrypt_password(encrypted_password, master_key):
    # 检查是否使用新的加密方式
    if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
        try:
            # 提取IV和密文
            iv = encrypted_password[3:15]
            ciphertext = encrypted_password[15:]
             
            # 创建AES解密器
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            # 解密
            decrypted = cipher.decrypt(ciphertext)
            # 移除填充并解码
            password = decrypted[:-16].decode('utf-8', errors='replace')
            print(f"decrypted_password:{password}")
            return password
        except Exception as e:
            print(f"AES解密失败: {str(e)}")
            raise
    else:
        # 尝试使用旧的解密方式
        try:
            return win32crypt.CryptUnprotectData(
                encrypted_password, None, None, None, 0
            )[1].decode('utf-8')
        except Exception as e:
            print(f"旧方式解密失败: {str(e)}")
            raise
 
def decrypt_edge_passwords():
    # Edge数据目录
    edge_data_dir = os.path.join(
        os.environ['USERPROFILE'],
        r'AppData\Local\Microsoft\Edge\User Data\Default'
    )
    login_data_file = os.path.join(edge_data_dir, 'Login Data')
     
    # 创建临时副本（因为Edge可能正在使用原文件）
    temp_file = os.path.join(edge_data_dir, 'LoginDataTemp')
    shutil.copy2(login_data_file, temp_file)
     
    results = []
     
    # 获取主密钥
    master_key = get_master_key()
     
    try:
        conn = sqlite3.connect(temp_file)
        cursor = conn.cursor()
         
        # 查询所有登录信息
        cursor.execute("""
            SELECT 
                origin_url, 
                username_value, 
                password_value, 
                date_created,
                date_last_used
            FROM logins 
            WHERE username_value != '' 
            AND password_value IS NOT NULL
            ORDER BY date_last_used DESC
        """)
         
        for row in cursor.fetchall():
            url, username, encrypted_password, date_created, date_last_used = row
            # print(f"处理: {url} - {username}")
            try:
                # 解密密码
                if master_key:
                    password = decrypt_password(encrypted_password, master_key)
                else:
                    # 尝试使用旧方式作为备选
                    password = win32crypt.CryptUnprotectData(
                        encrypted_password, None, None, None, 0
                    )[1].decode('utf-8')
                 
                # 转换时间戳
                if date_created:
                    created_time = datetime(1601, 1, 1) + timedelta(microseconds=date_created)
                else:
                    created_time = "未知"
                 
                if date_last_used:
                    last_used_time = datetime(1601, 1, 1) + timedelta(microseconds=date_last_used)
                else:
                    last_used_time = "未知"
                 
                results.append({
                    'url': url,
                    'username': username,
                    'password': password,
                    'created_time': str(created_time),
                    'last_used_time': str(last_used_time)
                })
                 
            except Exception as e:
                print(f"解密失败 [{url}]: {str(e)}")
                continue
                 
    except Exception as e:
        print(f"数据库错误: {e}")
    finally:
        conn.close()
        # 删除临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
     
    return results
 
# 使用示例
if __name__ == "__main__":
    passwords = decrypt_edge_passwords()
     
    print(f"找到 {len(passwords)} 个保存的密码:")
    print("=" * 80)
     
    for i, item in enumerate(passwords, 1):
        print(f"{i}. 网站: {item['url']}")
        print(f"   用户名: {item['username']}")
        print(f"   密码: {item['password']}")
        print(f"   创建时间: {item['created_time']}")
        print(f"   最后使用: {item['last_used_time']}")
        print("-" * 40)