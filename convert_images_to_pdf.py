# -*- coding: utf-8 -*-
 
import os
import subprocess
import sys
 
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
 
# https://www.52pojie.cn/thread-1838187-1-1.html
def pause_exit():
    subprocess.run("pause", shell=True)
    exit()
 
 
def get_images(img_folder):
    """遍历目录，获取目录下所有的图片"""
    img_format = (".jpg", ".png", ".bmp")
    images = []
    for file_name in os.listdir(img_folder):
        if file_name.lower().endswith(img_format):
            images.append(os.path.join(img_folder, file_name))
    return sorted(images)
 
 
def get_image_size(img_file, page_width, page_height):
    """设置每个图片的大小"""
    with Image.open(img_file) as img:
        img_width, img_height = img.size
        if img_height > page_height * 0.95 or img_width > page_width * 0.95:
            height_scale = (page_height * 0.95) / img_height
            width_scale = (page_width * 0.95) / img_width
            scale = min(height_scale, width_scale)
            img_width *= scale
            img_height *= scale
    return img_width, img_height
 
 
def create_pdf(pdf_file, images, page_width, page_height):
    """创建 pdf 文件，并添加图片"""
    c = canvas.Canvas(pdf_file, pagesize=letter)
 
    total_images = len(images)
    for i, img_path in enumerate(images):
        img_width, img_height = get_image_size(img_path, page_width, page_height)
        x = (page_width - img_width) / 2
        y = (page_height - img_height) / 2
        c.drawImage(img_path, x, y, img_width, img_height)
        c.showPage()
 
        progress_bar(i + 1, total_images)
 
    c.save()
 
 
def create_pdf_from_path(img_folder, pdf_file=None):
    """遍历给定路径，将路径下的图片添加进pdf，并将pdf保存在指定路径下"""
    images = get_images(img_folder)
    if images:
        if not pdf_file:
            pdf_name = os.path.basename(img_folder) + ".pdf"
            pdf_file = os.path.join(img_folder, pdf_name)
        page_width, page_height = letter
        create_pdf(pdf_file, images, page_width, page_height)
        return pdf_file
    else:
        print(f"{img_folder} 下没有图片，当前支持的图片格式为 jpg、png 和 bmp")
        pause_exit()
 
 
def progress_bar(current, total, bar_length=60):
    """进度条"""
    filled_length = int(bar_length * current // total)
    bar = "+" * filled_length + "-" * (bar_length - filled_length)
    percent = current / total * 100
    sys.stdout.write(f"\r处理进度：|{bar}| {percent:.2f}%")
    sys.stdout.flush()
 
 
if __name__ == "__main__":
    subprocess.run("title 目录内图片转PDF", shell=True)
 
    try:
        (*rest,) = sys.argv[1:]
        if not rest:
            img_folder = os.getcwd()  # 使用当前文件夹作为 img_folder
            pdf_file = None
        else:
            img_folder, *pdf_file = rest
            pdf_file = pdf_file[0] if pdf_file else None
    except ValueError:
        print("请提供图片文件夹路径作为参数")
        pause_exit()
 
    if not os.path.exists(img_folder):
        print(f"{img_folder} 路径不存在！")
        pause_exit()
    elif not os.path.isdir(img_folder):
        print(f"{img_folder} 不是一个文件夹！")
        pause_exit()
    else:
        pdf_file = create_pdf_from_path(img_folder, pdf_file)
 
        if pdf_file:
            subprocess.run(["explorer", pdf_file])
        else:
            pause_exit()