# coding:utf-8 
  
# 为一张图片生成对应的字符集图片 
  
from PIL import Image 
import argparse 
  
# 命令行输入参数处理 
#parser = argparse.ArgumentParser() 
# parser.add_argument('file')   # 输入文件 
# parser.add_argument('-o', '--output')  # 输出文件 
# parser.add_argument('--width', type=int, default=80) # 输出字符画宽 
# parser.add_argument('--height', type=int, default=80) # 输出字符画高 
  
# 获取参数 
# args = parser.parse_args() 
  
IMG = 'jay.jpg'
WIDTH = 80
HEIGHT = 80 
OUTPUT = 'jay.txt'
  
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ") 
  
  
# 将256灰度映射到70个字符上  https://github.com/DWCTOD/AI_study/blob/master/%E5%90%88%E6%A0%BC%E7%9A%84CV%E5%B7%A5%E7%A8%8B%E5%B8%88/%E5%AE%9E%E6%88%98%E7%AF%87/opencv/%EF%BC%88%E4%B8%89%EF%BC%89%E7%94%A8%E5%AD%97%E7%AC%A6%E6%96%B9%E5%BC%8F%E8%A1%A8%E7%A4%BA%E5%9B%BE%E7%89%87%EF%BC%8C%E8%BF%99%E7%A7%8D%E6%96%B9%E5%BC%8F%E7%AE%80%E7%9B%B4%E6%98%AF%E9%AD%94%E9%AC%BC/pic2word.py
def get_char(r, b, g, alpha=256): 
  if alpha == 0: 
    return ' '
  length = len(ascii_char) 
  gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b) 
  
  unit = (256.0+1)/length 
  print(unit)
  return ascii_char[int(gray/unit)] 
  
if __name__ == '__main__': 
  
  im = Image.open(IMG) 
  im = im.resize((WIDTH, HEIGHT), Image.NEAREST) 
  
  txt = "" 
  
  for i in range(HEIGHT): 
    for j in range(WIDTH): 
      txt += get_char(*im.getpixel((j, i))) 
    txt += '\n'
  
  print(txt) 
  
  # 字符画输出到文件 
  if OUTPUT: 
    with open(OUTPUT,'w') as f: 
      f.write(txt) 
  else: 
    with open("output.txt", 'w') as f: 
      f.write(txt)