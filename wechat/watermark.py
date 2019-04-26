from PIL import Image,ImageDraw,ImageFont
image = Image.open('python.png')
# 打开等待加水印的图片
watermark = Image.open('mp.png')
# 打开水印图片https://www.qingwei.tech/programe-develops/python/1154.html
factor = 1
# 如果觉得水印图片太大，可以缩放，这里缩放比例为50%
watermark = watermark.resize(
    tuple(map(lambda x: int(x * factor), watermark.size)))
# 缩放图片
layer=Image.new('RGBA',image.size)
# 生成一个新的layer
layer.paste(watermark,(image.size[0]-watermark.size[0],
    image.size[1]-watermark.size[1]))
# 把水印打到新的layer上去，后面参数是水印位置，此处是右下角    
marked_img=Image.composite(layer,image,layer)
# 添加水印
# marked_img.show()# 打开生成的图片（缓存图片）
marked_img.save('python2.png')
#保存图片


image = Image.open('python.png')
# 打开要加水印的图片
text=input('输入文字:\n')
# 提示要打水印的文字
font=ImageFont.truetype('C:\Windows\Fonts\simhei.ttf',64)
# 获得一个字体，你也可以自己下载相应字体，第二个值是字体大小
layer=image.convert('RGBA')
# 将图片转换为RGBA图片
text_overlay=Image.new('RGBA',layer.size)
# 依照目标图片大小生成一张新的图片 参数[模式,尺寸,颜色(默认为0)]
image_draw=ImageDraw.Draw(text_overlay)
# 画图
text_size_x,text_size_y=image_draw.textsize(text,font=font)
# 获得字体大小,textsize(text, font=None)
text_xy=(layer.size[0]-text_size_x,layer.size[1]-text_size_y)
# 设置文本位置 此处是右下角显示
image_draw.text(text_xy, text, font=font, fill=(0, 0, 0, 85))
# 设置文字，位置,字体,颜色和透明度
marked_img=Image.alpha_composite(layer,text_overlay)
# 将水印打到原图片上生成新的图片
marked_img.save('wechat_wen.png')
# 保存图片
marked_img.show()
# 显示图片（这里是生成一个临时文件，必须关闭图片 这段py代码才算结束）