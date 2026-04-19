import os
import shutil
import zipfile
import tempfile
import threading
import subprocess
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import olefile
 
gif_settings = {
    "fps": 8,
    "width": 480
}
# 解析 PPTX 压缩包结构，提取 media/embeddings 目录下的图片、音频、视频；通过 FFmpeg 修复非标视频、转 GIF，拖放操作。
def get_embed_video_names_from_pptx(pptx_path: str) -> dict:
    video_names = {}
     
    try:
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            rels_files = [f for f in zf.namelist() if 'slides/_rels' in f and f.endswith('.rels')]
             
            for rels_file in rels_files:
                try:
                    content = zf.read(rels_file).decode('utf-8')
                     
                    video_patterns = [
                        r'Target="(\.\./embeddings/[^"]+)"',
                        r'Target="(\.\./media/[^"]+)"'
                    ]
                     
                    for pattern in video_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            filename = os.path.basename(match)
                            if filename not in video_names:
                                name_without_ext = os.path.splitext(filename)[0]
                                video_names[filename] = name_without_ext
                except:
                    continue
    except:
        pass
     
    return video_names
 
def parse_ole_video_data(bin_data: bytes) -> bytes:
    if not bin_data or len(bin_data) < 100:
        return b""
     
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as tmp:
            tmp.write(bin_data)
            tmp_path = tmp.name
         
        if olefile.isOleFile(tmp_path):
            ole = olefile.OleFileIO(tmp_path)
             
            video_streams = []
            for stream_name in ole.listdir():
                full_name = '/'.join(stream_name)
                if len(stream_name) >= 1:
                    try:
                        stream_data = ole.openstream(stream_name).read()
                        if stream_data and len(stream_data) > 1000:
                            video_streams.append((len(stream_data), stream_data, full_name))
                    except:
                        continue
             
            ole.close()
             
            if video_streams:
                video_streams.sort(reverse=True)
                _, best_data, _ = video_streams[0]
                os.unlink(tmp_path)
                 
                video_data = extract_clean_video(best_data)
                if video_data:
                    return video_data
    except Exception as e:
        pass
    finally:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass
     
    return extract_clean_video(bin_data)
 
def extract_clean_video(data: bytes) -> bytes:
    if not data:
        return b""
     
    patterns = [
        b'ftyp', b'moov', b'mdat', b'free', b'skip', b'wide',
        b'RIFF', b'ASF', b'\x00\x00\x01\xBA', b'FLV',
        b'\x1a\x45\xdf\xa3'
    ]
     
    positions = []
    for pattern in patterns:
        pos = data.find(pattern)
        if pos != -1 and pos < len(data) - 100:
            positions.append(pos)
     
    if positions:
        best_pos = min(positions)
        return data[best_pos:]
     
    return data[len(data)//2:] if len(data) > 1000 else b""
 
def get_video_ext_by_data(video_data: bytes) -> str:
    if not video_data or len(video_data) < 4:
        return '.bin'
     
    if video_data[:4] in [b'ftyp', b'moov', b'mdat', b'free', b'skip', b'wide']:
        return '.mp4'
    elif video_data[:4] == b'RIFF' and len(video_data) > 12:
        if video_data[8:12] == b'AVI ':
            return '.avi'
    elif video_data[:4] == b'ASF':
        return '.wmv'
    elif len(video_data) > 3 and video_data[:3] == b'FLV':
        return '.flv'
    elif len(video_data) > 4 and video_data[0:4] == b'\x1a\x45\xdf\xa3':
        return '.mkv'
     
    for pattern in [b'avc1', b'h264', b'avc3', b'hev1', b'hvc1']:
        if pattern in video_data[:2000]:
            return '.mp4'
     
    return '.mp4'
 
def run_ffmpeg(cmd, timeout=180):
    try:
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            encoding='utf-8',
            errors='replace',
            timeout=timeout,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
        )
        return result
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        return None
 
def video_to_gif_ffmpeg(video_path: str, gif_path: str, fps: int = 8, width: int = 480):
    ffmpeg_exe = "ffmpeg" if os.name != "nt" else "ffmpeg.exe"
     
    try:
        subprocess.run([ffmpeg_exe, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    except:
        return False
 
    probe_cmd = [ffmpeg_exe, "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height,r_frame_rate", "-of", "csv=p=0", video_path]
    probe_result = run_ffmpeg(probe_cmd, timeout=30)
     
    if probe_result and probe_result.returncode == 0 and probe_result.stdout.strip():
        try:
            parts = probe_result.stdout.strip().split(',')
            orig_width, orig_height = int(parts[0]), int(parts[1])
        except:
            orig_width, orig_height = 640, 480
    else:
        orig_width, orig_height = 640, 480
 
    height = int(width * orig_height / orig_width)
    width = width if width % 2 == 0 else width - 1
    height = height if height % 2 == 0 else height - 1
 
    ffmpeg_cmd = [
        ffmpeg_exe,
        "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-hwaccel", "auto",
        "-i", video_path,
        "-vf", f"fps={fps},scale={width}:{height}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "-loop", "0",
        gif_path
    ]
 
    result = run_ffmpeg(ffmpeg_cmd, timeout=180)
     
    if result and result.returncode == 0 and os.path.exists(gif_path) and os.path.getsize(gif_path) > 100:
        return True
     
    return False
 
def fix_video_with_ffmpeg(input_path: str, output_path: str) -> bool:
    ffmpeg_exe = "ffmpeg" if os.name != "nt" else "ffmpeg.exe"
     
    fix_cmd = [
        ffmpeg_exe,
        "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-fflags", "+genpts+discardcorrupt",
        "-err_detect", "ignore",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        "-f", "mp4",
        output_path
    ]
     
    result = run_ffmpeg(fix_cmd, timeout=300)
     
    if result and result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        return True
     
    return False
 
def sanitize_filename(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()
 
def extract_from_pptx(pptx_path: str, output_root: str, progress_bar: ttk.Progressbar, root: tk.Tk, settings: dict):
    dirs = {
        "image": os.path.join(output_root, "图片"),
        "audio": os.path.join(output_root, "音频"),
        "video": os.path.join(output_root, "视频"),
        "gif": os.path.join(output_root, "GIF")
    }
    for d in dirs.values():
        os.makedirs(d, exist_ok=True)
 
    embed_names = get_embed_video_names_from_pptx(pptx_path)
     
    std_count = 0
    success_count = 0
    gif_success_count = 0
    processed = 0
    fix_success_count = 0
 
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
 
            media_src = os.path.join(temp_dir, "ppt", "media")
            if os.path.isdir(media_src):
                files = os.listdir(media_src)
                std_count = len(files)
                for f in files:
                    src = os.path.join(media_src, f)
                    ext = os.path.splitext(f)[1].lower()
                    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
                        dst = os.path.join(dirs["image"], f)
                    elif ext in ['.mp3', '.wav', '.aac', '.ogg', '.wma', '.flac']:
                        dst = os.path.join(dirs["audio"], f)
                    else:
                        dst = os.path.join(dirs["image"], f)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
 
            embed_src = os.path.join(temp_dir, "ppt", "embeddings")
            bin_files = []
            if os.path.isdir(embed_src):
                for f in os.listdir(embed_src):
                    if os.path.isfile(os.path.join(embed_src, f)):
                        bin_files.append(f)
             
            total = len(bin_files)
            root.after(0, lambda: progress_bar.config(maximum=total if total > 0 else 1, value=0))
 
            used_names = set()
 
            for idx, filename in enumerate(bin_files, 1):
                bin_path = os.path.join(embed_src, filename)
                if not os.path.isfile(bin_path):
                    processed += 1
                    root.after(0, lambda v=processed: progress_bar.config(value=v))
                    continue
 
                try:
                    with open(bin_path, 'rb') as f:
                        bin_data = f.read()
                except:
                    processed += 1
                    root.after(0, lambda v=processed: progress_bar.config(value=v))
                    continue
                 
                video_data = parse_ole_video_data(bin_data)
 
                if video_data and len(video_data) > 1000:
                    ext = get_video_ext_by_data(video_data)
                     
                    base_name = embed_names.get(filename, f"视频_{idx}")
                    base_name = sanitize_filename(base_name)
                     
                    if base_name in used_names:
                        base_name = f"{base_name}_{idx}"
                    used_names.add(base_name)
                     
                    video_name = f"{base_name}{ext}"
                    video_path = os.path.join(dirs["video"], video_name)
                     
                    try:
                        with open(video_path, 'wb') as f:
                            f.write(video_data)
                        success_count += 1
                    except:
                        base_name = f"视频_{idx}"
                        video_name = f"{base_name}{ext}"
                        video_path = os.path.join(dirs["video"], video_name)
                        with open(video_path, 'wb') as f:
                            f.write(video_data)
                        success_count += 1
 
                    fixed_video_path = os.path.join(dirs["video"], f"{base_name}.mp4")
                    if fix_video_with_ffmpeg(video_path, fixed_video_path):
                        if os.path.exists(video_path) and video_path != fixed_video_path:
                            os.remove(video_path)
                        video_path = fixed_video_path
                        fix_success_count += 1
 
                    gif_name = f"{base_name}.gif"
                    gif_path = os.path.join(dirs["gif"], gif_name)
                    if video_to_gif_ffmpeg(video_path, gif_path, fps=settings.get("fps", 8), width=settings.get("width", 480)):
                        gif_success_count += 1
 
                processed += 1
                root.after(0, lambda v=processed: progress_bar.config(value=v))
 
        msg = (f"处理完成！\n文件已保存至：\n{output_root}\n\n"
               f"图片：{std_count}个\n"
               f"视频：{success_count}个\n"
               f"GIF：{gif_success_count}个")
        root.after(0, lambda: messagebox.showinfo("完成", msg))
 
    except zipfile.BadZipFile:
        root.after(0, lambda: messagebox.showerror("错误", "无效的PPTX文件"))
    except Exception as e:
        import traceback
        traceback.print_exc()
        root.after(0, lambda: messagebox.showerror("失败", f"处理异常：{str(e)}"))
    finally:
        root.after(0, lambda: progress_bar.config(value=0))
 
def on_drop(event, progress_bar: ttk.Progressbar, root: tk.Tk, settings: dict):
    raw_path = event.data.strip()
    if raw_path.startswith('{') and raw_path.endswith('}'):
        raw_path = raw_path[1:-1]
    if raw_path.startswith('file:///'):
        raw_path = raw_path[8:]
    elif raw_path.startswith('file://'):
        raw_path = raw_path[7:]
    file_path = os.path.normpath(raw_path)
 
    if not os.path.isfile(file_path):
        messagebox.showerror("错误", "请拖入有效文件！")
        return
    if os.path.splitext(file_path)[1].lower() != ".pptx":
        messagebox.showerror("错误", "仅支持PPTX格式文件！")
        return
 
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(os.path.dirname(file_path), f"{base_name}_提取结果")
 
    task_thread = threading.Thread(
        target=extract_from_pptx,
        args=(file_path, output_dir, progress_bar, root, settings),
        daemon=True
    )
    task_thread.start()
 
def create_settings_window(parent):
    settings_win = tk.Toplevel(parent)
    settings_win.title("GIF参数设置")
    settings_win.geometry("300x200")
    settings_win.resizable(False, False)
    settings_win.transient(parent)
    settings_win.grab_set()
     
    style = ttk.Style(settings_win)
    style.configure("Title.TLabel", font=("微软雅黑", 11, "bold"))
    style.configure("Normal.TLabel", font=("微软雅黑", 10))
    style.configure("Normal.TEntry", font=("微软雅黑", 10))
     
    ttk.Label(settings_win, text="GIF参数设置", style="Title.TLabel").pack(pady=(20, 15))
     
    frame = ttk.Frame(settings_win)
    frame.pack(pady=10)
     
    ttk.Label(frame, text="帧率 (FPS):", style="Normal.TLabel").grid(row=0, column=0, sticky="w", pady=8, padx=10)
    fps_var = tk.StringVar(value=str(gif_settings["fps"]))
    fps_spin = ttk.Spinbox(frame, from_=1, to=30, textvariable=fps_var, width=10, font=("微软雅黑", 10))
    fps_spin.grid(row=0, column=1, pady=8, padx=10)
     
    ttk.Label(frame, text="宽度 (像素):", style="Normal.TLabel").grid(row=1, column=0, sticky="w", pady=8, padx=10)
    width_var = tk.StringVar(value=str(gif_settings["width"]))
    width_spin = ttk.Spinbox(frame, from_=100, to=1920, increment=10, textvariable=width_var, width=10, font=("微软雅黑", 10))
    width_spin.grid(row=1, column=1, pady=8, padx=10)
     
    ttk.Label(frame, text="(高度自动计算)", style="Normal.TLabel").grid(row=2, column=1, sticky="w", padx=10)
     
    def save_settings():
        try:
            fps = int(fps_var.get())
            width = int(width_var.get())
            if fps < 1 or fps > 30:
                messagebox.showwarning("警告", "帧率应在1-30之间")
                return
            if width < 100 or width > 1920:
                messagebox.showwarning("警告", "宽度应在100-1920之间")
                return
            gif_settings["fps"] = fps
            gif_settings["width"] = width
            settings_win.destroy()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
     
    btn_frame = ttk.Frame(settings_win)
    btn_frame.pack(pady=20)
    ttk.Button(btn_frame, text="保存", command=save_settings, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="取消", command=settings_win.destroy, width=10).pack(side=tk.LEFT, padx=5)
 
def main():
    root = TkinterDnD.Tk()
    root.title("PPTX资源提取工具")
    root.geometry("500x320")
    root.resizable(False, False)
     
    style = ttk.Style(root)
    style.configure("Title.TLabel", font=("微软雅黑", 14, "bold"))
    style.configure("Sub.TLabel", font=("微软雅黑", 10))
    style.configure("Drop.TLabel", font=("微软雅黑", 20, "bold"))
    style.configure("Accent.TButton", font=("微软雅黑", 10))
     
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
     
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 15))
     
    title_label = ttk.Label(header_frame, text="PPTX资源提取工具", style="Title.TLabel")
    title_label.pack(side=tk.LEFT)
     
    settings_btn = ttk.Button(header_frame, text="&#9881; GIF设置", command=lambda: create_settings_window(root), style="Accent.TButton")
    settings_btn.pack(side=tk.RIGHT)
     
    drop_frame = ttk.LabelFrame(main_frame, text="拖放区域", padding="15")
    drop_frame.pack(fill=tk.BOTH, expand=True, pady=10)
     
    drop_label = ttk.Label(
        drop_frame,
        text="+",
        font=("微软雅黑", 48),
        foreground="#888888"
    )
    drop_label.pack(expand=True)
     
    drop_sub_label = ttk.Label(
        drop_frame,
        text="将PPTX文件拖放到此处",
        style="Sub.TLabel",
        foreground="#666666"
    )
    drop_sub_label.pack(pady=(0, 10))
     
    progress_bar = ttk.Progressbar(main_frame, mode='determinate')
    progress_bar.pack(fill=tk.X, pady=(10, 0))
     
    status_label = ttk.Label(main_frame, text="就绪", style="Sub.TLabel", foreground="#888888")
    status_label.pack(pady=(5, 0))
     
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', lambda e: on_drop(e, progress_bar, root, gif_settings))
     
    def set_status(text):
        status_label.config(text=text)
     
    root.mainloop()
 
if __name__ == "__main__":
    main()