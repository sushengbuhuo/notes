import re
import json
import requests
import os
import threading
import subprocess
from typing import Dict, List, Optional
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
#https://www.52pojie.cn/thread-2071186-1-1.html
class BilibiliDownloader:
        def __init__(self, video_url: str = ""):
                self.video_url = video_url
                self.session = requests.Session()
                self.play_info = None
                self.video_title = "bilibili_video"

                self.session.headers.update({
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': 'https://www.bilibili.com/'
                })

        def extract_play_info(self, html_content: str) -> Optional[Dict]:
                """从HTML中提取视频播放信息"""
                patterns = [
                        r'window\.__playinfo__\s*=\s*({[\s\S]*?})\s*;',
                        r'<script>window\.__playinfo__\s*=\s*({[\s\S]*?})</script>'
                ]

                for pattern in patterns:
                        match = re.search(pattern, html_content)
                        if match:
                                try:
                                        return json.loads(match.group(1))
                                except json.JSONDecodeError:
                                        fixed_json = self.fix_json(match.group(1))
                                        try:
                                                return json.loads(fixed_json)
                                        except:
                                                continue
                return None

        def extract_video_title(self, html_content: str) -> str:
                """从HTML中提取视频标题"""
                patterns = [
                        r'<title[^>]*>(.*?)</title>',
                        r'"title":"([^"]+)"',
                        r'<h1[^>]*title="([^"]+)"'
                ]

                for pattern in patterns:
                        match = re.search(pattern, html_content)
                        if match:
                                title = match.group(1)
                                # 清理标题
                                title = re.sub(r'[<>:"/\\|?*]', '_', title)
                                title = re.sub(r'\s+', ' ', title).strip()
                                if title and title != 'bilibili_video':
                                        return title[:100]  # 限制长度
                return "bilibili_video"

        def fix_json(self, json_str: str) -> str:
                """修复JSON格式"""
                return (json_str
                                .replace("'", '"')
                                .replace(r'([a-zA-Z_$][a-zA-Z0-9_$]*):', r'"\1":')
                                .replace(r',\s*}', '}')
                                .replace(r',\s*]', ']'))

        def get_video_info(self) -> bool:
                """获取视频信息"""
                try:
                        response = self.session.get(self.video_url)
                        response.raise_for_status()

                        self.play_info = self.extract_play_info(response.text)
                        self.video_title = self.extract_video_title(response.text)
                        return self.play_info is not None

                except Exception as e:
                        print(f"获取视频信息失败: {e}")
                        return False

        def get_video_streams(self) -> List[Dict]:
                """获取视频流列表"""
                if not self.play_info or 'data' not in self.play_info:
                        return []
                return self.play_info['data'].get('dash', {}).get('video', [])

        def get_audio_streams(self) -> List[Dict]:
                """获取音频流列表"""
                if not self.play_info or 'data' not in self.play_info:
                        return []
                return self.play_info['data'].get('dash', {}).get('audio', [])

        def select_highest_quality_video(self) -> Optional[Dict]:
                """选择最高质量的视频流"""
                videos = self.get_video_streams()
                if not videos:
                        return None

                # 按id降序排列，选择最高的
                videos_sorted = sorted(videos, key=lambda x: x.get('id', 0), reverse=True)
                return videos_sorted[0]

        def select_highest_quality_audio(self) -> Optional[Dict]:
                """选择最高质量的音频流"""
                audios = self.get_audio_streams()
                if not audios:
                        return None

                # 按带宽降序排列
                audios_sorted = sorted(audios, key=lambda x: x.get('bandwidth', 0), reverse=True)
                return audios_sorted[0]

        def download_stream(self, url: str, filename: str, progress_callback=None, chunk_size: int = 8192) -> bool:
                """下载音视频流"""
                try:
                        headers = {
                                'Referer': 'https://www.bilibili.com/',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }

                        response = self.session.get(url, headers=headers, stream=True)
                        response.raise_for_status()

                        total_size = int(response.headers.get('content-length', 0))
                        downloaded = 0

                        with open(filename, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=chunk_size):
                                        if chunk:
                                                f.write(chunk)
                                                downloaded += len(chunk)
                                                if progress_callback and total_size > 0:
                                                        progress_callback(downloaded, total_size)

                        return True

                except Exception as e:
                        print(f"下载失败: {e}")
                        return False

        def check_ffmpeg(self) -> bool:
                """检查FFmpeg是否可用"""
                try:
                        # 先检查当前目录
                        if os.path.exists("ffmpeg.exe"):
                                return True

                        # 检查系统PATH
                        result = subprocess.run(["ffmpeg", "-version"], 
                                                                    capture_output=True, text=True, encoding='utf-8', errors='ignore')
                        return result.returncode == 0
                except:
                        return False

        def merge_video_audio(self, video_file: str, audio_file: str, output_file: str) -> bool:
                """使用FFmpeg合并音视频"""
                try:
                        if self.check_ffmpeg():
                                ffmpeg_cmd = "ffmpeg"
                                if os.path.exists("ffmpeg.exe"):
                                        ffmpeg_cmd = "ffmpeg.exe"

                                cmd = [
                                        ffmpeg_cmd, 
                                        '-i', video_file,
                                        '-i', audio_file,
                                        '-c', 'copy',
                                        '-y',  # 覆盖输出文件
                                        output_file
                                ]

                                # 修复编码问题：指定UTF-8编码并忽略错误
                                result = subprocess.run(cmd, capture_output=True, text=True, 
                                                                            encoding='utf-8', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
                                return result.returncode == 0
                        else:
                                print("FFmpeg未找到，无法合并")
                                return False

                except Exception as e:
                        print(f"合并失败: {e}")
                        return False

        def download_highest_quality(self, progress_callback=None, status_callback=None) -> bool:
                """下载最高质量的视频和音频并自动合并"""
                if not self.get_video_info():
                        if status_callback:
                                status_callback("❌ 无法获取视频信息，请检查URL")
                        return False

                videos = self.get_video_streams()
                audios = self.get_audio_streams()

                if not videos or not audios:
                        if status_callback:
                                status_callback("❌ 未找到可下载的音视频流")
                        return False

                # 选择最高质量
                best_video = self.select_highest_quality_video()
                best_audio = self.select_highest_quality_audio()

                if not best_video or not best_audio:
                        if status_callback:
                                status_callback("❌ 无法选择最高质量的流")
                        return False

                video_url = best_video.get('baseUrl') or best_video.get('base_url')
                audio_url = best_audio.get('baseUrl') or best_audio.get('base_url')

                if not video_url or not audio_url:
                        if status_callback:
                                status_callback("❌ 无效的音视频URL")
                        return False

                # 生成文件名
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', self.video_title)
                video_file = f"{safe_title}_video_temp.mp4"
                audio_file = f"{safe_title}_audio_temp.m4a"
                output_file = f"{safe_title}_merged.mp4"

                if status_callback:
                        status_callback(f"📹 开始下载视频流 ({best_video.get('id', 'N/A')}P)")

                # 下载视频
                if not self.download_stream(video_url, video_file, progress_callback):
                        if status_callback:
                                status_callback("❌ 视频下载失败")
                        return False

                if status_callback:
                        status_callback("🎵 开始下载音频流")

                # 下载音频
                if not self.download_stream(audio_url, audio_file, progress_callback):
                        if status_callback:
                                status_callback("❌ 音频下载失败")
                        return False

                # 检查FFmpeg并合并
                if self.check_ffmpeg():
                        if status_callback:
                                status_callback("🔄 开始合并音视频...")

                        if self.merge_video_audio(video_file, audio_file, output_file):
                                # 删除临时文件
                                try:
                                        os.remove(video_file)
                                        os.remove(audio_file)
                                except:
                                        pass

                                if status_callback:
                                        status_callback(f"✅ 下载完成: {output_file}")
                                return True
                        else:
                                if status_callback:
                                        status_callback("❌ 合并失败，但音视频文件已保存")
                                return False
                else:
                        if status_callback:
                                status_callback("⚠️ FFmpeg未找到，音视频文件已分别保存")
                        return True

class BilibiliDownloaderGUI:
        def __init__(self):
                self.root = tk.Tk()
                self.root.title("B站视频简易下载器")
                self.root.geometry("600x500")
                self.root.resizable(True, True)

                self.downloader = None
                self.is_downloading = False

                self.setup_ui()

        def setup_ui(self):
                """设置用户界面"""
                # 主框架
                main_frame = ttk.Frame(self.root, padding="10")
                main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

                # 配置网格权重
                self.root.columnconfigure(0, weight=1)
                self.root.rowconfigure(0, weight=1)
                main_frame.columnconfigure(1, weight=1)
                main_frame.rowconfigure(4, weight=1)

                # 标题
                title_label = ttk.Label(main_frame, text="B站视频下载器简易下载器", 
                                                             font=("Arial", 16, "bold"))
                title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

                # URL输入
                ttk.Label(main_frame, text="视频URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
                self.url_entry = ttk.Entry(main_frame, width=60)
                self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

                # 进度条
                self.progress_var = tk.DoubleVar()
                self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
                self.progress_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

                # 按钮框架
                button_frame = ttk.Frame(main_frame)
                button_frame.grid(row=3, column=0, columnspan=2, pady=10)
                button_frame.columnconfigure(0, weight=1)

                # 包含按钮的子框架，用于居中对齐
                buttons_container = ttk.Frame(button_frame)
                buttons_container.grid(row=0, column=0)

                self.download_button = ttk.Button(buttons_container, text="开始下载", command=self.start_download)
                self.download_button.pack(side=tk.LEFT, padx=(0, 10))

                ttk.Button(buttons_container, text="清空", command=self.clear_all).pack(side=tk.LEFT)

                # 状态显示
                self.status_var = tk.StringVar(value="就绪")
                status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                                                foreground="blue")
                status_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)

                # 日志框
                ttk.Label(main_frame, text="下载日志:").grid(row=5, column=0, sticky=tk.W, pady=(10, 0))
                self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=70)
                self.log_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

                # FFmpeg状态
                self.check_ffmpeg_status()

        def check_ffmpeg_status(self):
                """检查FFmpeg状态"""
                temp_downloader = BilibiliDownloader()
                if temp_downloader.check_ffmpeg():
                        self.log("✅ FFmpeg可用，下载后将自动合并")
                else:
                        self.log("⚠️ FFmpeg未找到，请下载FFmpeg并放在程序目录或系统PATH中")
                        self.log("  下载地址: https://ffmpeg.org/download.html")

        def log(self, message: str):
                """添加日志"""
                timestamp = time.strftime("%H:%M:%S")
                self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
                self.log_text.see(tk.END)
                self.root.update_idletasks()

        def update_progress(self, downloaded: int, total: int):
                """更新进度条"""
                if total > 0:
                        percentage = (downloaded / total) * 100
                        self.progress_var.set(percentage)
                        self.status_var.set(f"下载进度: {percentage:.1f}% ({downloaded}/{total} bytes)")
                self.root.update_idletasks()

        def update_status(self, message: str):
                """更新状态"""
                self.status_var.set(message)
                self.log(message)
                self.root.update_idletasks()

        def start_download(self):
                """开始下载"""
                if self.is_downloading:
                        return

                url = self.url_entry.get().strip()
                if not url:
                        messagebox.showerror("错误", "请输入B站视频URL")
                        return

                if not url.startswith(('https://www.bilibili.com/video/', 
                                                         'https://www.bilibili.com/bangumi/play/')):
                        messagebox.showwarning("警告", "请输入有效的B站视频URL")
                        return

                # 在新线程中下载
                self.is_downloading = True
                self.download_button.config(state="disabled")
                self.progress_var.set(0)

                def download_thread():
                        try:
                                self.downloader = BilibiliDownloader(url)

                                self.update_status("🔍 正在获取视频信息...")

                                success = self.downloader.download_highest_quality(
                                        progress_callback=self.update_progress,
                                        status_callback=self.update_status
                                )

                                if success:
                                        self.update_status("✅ 任务完成！")
                                else:
                                        self.update_status("❌ 下载失败")

                        except Exception as e:
                                self.update_status(f"❌ 发生错误: {str(e)}")
                        finally:
                                self.is_downloading = False
                                self.root.after(0, lambda: self.download_button.config(state="normal"))

                threading.Thread(target=download_thread, daemon=True).start()

        def clear_all(self):
                """清空所有输入和日志"""
                self.url_entry.delete(0, tk.END)
                self.log_text.delete(1.0, tk.END)
                self.progress_var.set(0)
                self.status_var.set("就绪")
                self.check_ffmpeg_status()   
def main():
        """主函数"""      
        app = BilibiliDownloaderGUI()
        app.root.mainloop()
if __name__ == "__main__":
        main()