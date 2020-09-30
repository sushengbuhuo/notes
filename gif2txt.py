import imageio as igo
import cv2
#gif转文字
pics = igo.mimread('love.gif')
#print(pics.shape)
string = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:oa+>!:+."
A=[]
for img in pics:
    u,v,_=img.shape
    c=img*0+255
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    for i in range(0,u,24):
        for j in range(0,v,15):
            pix = gray[i,j]
            b,g,r,_=img[i,j]
            zifu = string[int(((len(string)-1)*pix)/256)]
            cv2.putText(c,zifu,(j,i),
                    cv2.FONT_HERSHEY_COMPLEX,0.3,
                    (int(b),2*int(g),int(r),1))
    A.append(c)
igo.mimsave('love2.gif',A,'GIF',duration=0.1)

#视频转字符画https://www.zhihu.com/question/31282157/answer/337036171
import os
import time
from PIL import Image

folder = "./"
file_type = 'bmp'
file_list = os.listdir(folder)


class Images(object):
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def to_ascii(f_path):
        img = Image.open(f_path).convert('L')
        pix = img.load()
        width, height = img.size
        pic_str = ''
        for h in range(height):
            for w in range(width):
                if int(pix[w, h] < 128):
                    pic_str += '#'
                else:
                    pic_str += ' '
        return pic_str

    def play(self, f_list, f_type):
        pic_string = ''
        for file in f_list:
            if file.split('.')[1] == f_type:
                img_str = self.to_ascii(self.file_path + file)
                time.sleep(0.01)
                os.system("cls")
                print(img_str)
                pic_string += img_str


if __name__ == '__main__':
    Images.play(Images(folder), file_list, file_type)