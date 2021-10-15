import os
import random
import numpy as np
import PIL.Image as Image
FRAME = [[0,1,1,0,0,0,0,1,1,0],
         [1,1,1,1,0,0,1,1,1,1],
         [1,1,1,1,1,1,1,1,1,1],
         [1,1,1,1,1,1,1,1,1,1],
         [0,1,1,1,1,1,1,1,1,0],
         [0,0,1,1,1,1,1,1,0,0],
         [0,0,0,1,1,1,1,0,0,0],
         [0,0,0,0,1,1,0,0,0,0]]
# 定义相关参数
SIZE = 50 # 每张图片的尺寸为50*50
N = 2     # 每个点位上放置2*2张图片
# 计算相关参数
width = np.shape(FRAME)[1]*N*SIZE  # 照片墙宽度
height = np.shape(FRAME)[0]*N*SIZE # 照片墙高度
n_img = np.sum(FRAME)*(N**2)       # 照片墙需要的照片数
print(n_img,width,height)#208 1000 800 
li=os.listdir('./周杰伦')
filenames = random.sample(li, n_img if len(li) > n_img else len(li))
# filenames = random.sample(os.listdir('./刘亦菲'),n_img) # 随机选取n_img张照片
filenames = ['./周杰伦/'+f for f in filenames]
# 绘制爱心墙
img_bg = Image.new('RGB',(width,height)) # 设置照片墙背景
i = 0
for y in range(np.shape(FRAME)[0]):
    for x in range(np.shape(FRAME)[1]):
         if FRAME[y][x] == 1: # 如果需要填充
             pos_x = x*N*SIZE # 填充起始X坐标位置
             pos_y = y*N*SIZE # 填充起始Y坐标位置
             for yy in range(N):
                 for xx in range(N):
                     img = Image.open(filenames[i])
                     img = img.resize((SIZE,SIZE),Image.ANTIALIAS)
                     img_bg.paste(img,(pos_x+xx*SIZE,pos_y+yy*SIZE))
                     i += 1
# 保存图片
img_bg.save('love.jpg')
