import os
from math import sqrt
from PIL import Image
path = os.getcwd() + '\\刘亦菲\\'
def joint_avatar(path):	
	pathList = []
	for item in os.listdir(path):
		if item.endswith('.jpg'):
			imgPath = os.path.join(path,item)
			pathList.append(imgPath)
	total = len(pathList)
	line = int(sqrt(total))
	NewImage = Image.new('RGB', (128*line,128*line))
	x = y = 0
	for item in pathList:
	    try:
	        img = Image.open(item)
	        img = img.resize((128,128),Image.ANTIALIAS)
	        NewImage.paste(img, (x * 128 , y * 128))
	        x += 1
	    except IOError:
	        print("图片读取失败:%s" % (item))
	        x -= 1
	    if x == line:
	        x = 0
	        y += 1
	    if (x+line*y) == line*line:
	        break
	NewImage.save("pictures.jpg")
joint_avatar(path)