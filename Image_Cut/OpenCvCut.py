
#图片灰度化
from PIL import Image
import sys
from PIL import Image
def gray_image():
    I = Image.open('F:/image_cut/source_image/face.jpg')
    L = I.convert('1')
    image = L.save("F:/image_cut/result_image/test.jpg")
    L.show()

from PIL import Image
import sys

#将图片填充为正方形
def fill_image(image):
    width, height = image.size
    new_image_length = width if width > height else height
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    #将之前的图粘贴在新图上，居中
    if width > height:#原图宽大于高，则填充图片的竖直维度
        #(x,y)二元组表示粘贴上图相对下图的起始位置
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))
    return new_image

#切图
def cut_image(image):
    width, height = image.size
    item_width = int(width / 3)
    box_list = []
    #双层循环，生成9张图片基于原图的位置
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j*item_width, i*item_width, (j+1)*item_width, (i+1)*item_width)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]
    return image_list

#保存图片
def save_images(image_list):
    index = 1
    for image in image_list:
        image.save('F:/image_cut/result_image/'+str(index) + '.jpg')
        index += 1

if __name__ == '__main__':
    # gray_image()
    # file_path = "F:/image_cut/source_image/face.jpg"
    file_path = "F:/image_cut/result_image/test.jpg"
    image = Image.open(file_path)
    # image.show()
    image = fill_image(image)
    image_list = cut_image(image)
    save_images(image_list)