from os import path
from os import walk as walk
from PIL import Image

image_paths, input_paths = [], []
watermark_path = r'D:\experiment\watermark.png'

def add_watermark(image_path, watermark_path, output_path):
    image = Image.open(image_path)
    watermark = Image.open(watermark_path)
    mask = watermark.copy()
    output = image.copy()
    output.paste(watermark, (0, 0), mask)
    output.save(output_path)

for _, _, files in walk('image'):
    for file in files:
        if path.splitext(file)[-1] in ('.png', '.PNG'):
            image_paths.append( ( path.join('image', file), *path.splitext(file) ) )

for image in image_paths:
    input_paths.append( ( image[0], 'image\\{}-watermark{}'.format(image[1], image[2]) ) )

for image, output in input_paths:
    add_watermark(image, watermark_path, output)
    print('{} Completed!'.format(image))