from PIL import Image
import os

location = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

img_w = img_h = 192  # 宽高都设置为192像素 https://www.cnblogs.com/lwsbc/p/16293701.html

# 计算location二维数组的行的个数、列的个数
rows = len(location)
columns = len(location[0])

# 使用行、列的个数以及每张图片的像素计算出目标画布的大小。
canvas = Image.new("RGB", (img_w*columns, img_h*rows),"white")
source_img_dir = r"C:\Users\suping3\Pictures\jay"
source_imgs = os.listdir(source_img_dir)
# 定义一个下标值，方便从我们的imgs数组里面取出照片。
index = 0

# 通过遍历二维数组中的行、列，从而在相应的位置放上我们的照片。
for row in range(rows):

    for column in range(columns):

        # 若是当前二维数组中的元素为1时，表示该位置不在心形需要的位置上故不做处理。
        if location[row][column] == 1:

            continue

        # 若是当前二维数组中的元素为1时，需要将一张照片放到该位置上
        else:

            try:

                # 获取一张图片并打开为Image对象
                image = Image.open(os.path.join(source_img_dir, source_imgs[index]))

                # 重新设置当前照片的尺寸大小
                image = image.resize((img_w, img_h))

                # 将照片image对象，放在画布的特定位置
                canvas.paste(image, (img_w * column, img_h * row))

                # 递增图片列表中的图片下标
                index += 1

            except:

                continue
canvas.show()
canvas.save('照片墙.png')