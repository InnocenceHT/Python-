from PIL import Image
import sys
from PIL import Image

file_path = "C:/Users/HeTao/Desktop/二值化.bmp"

#图片二值化
from PIL import Image

img = Image.open('C:/Users/HeTao/Desktop/校徽.jpg')

# 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
Img = img.convert('L')
Img.save("test1.jpg")

# 自定义灰度界限，大于这个值为黑色，小于这个值为白色
threshold = 100

table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
# 图片二值化
photo = Img.point(table, '1')
# img = photo.save("C:/Users/HeTao/Desktop/二值化.jpg")

save_path = "C:/Users/HeTao/Desktop/5.bmp"

#将图片填充为正方形
def fill_image(image):
    width, height = image.size
    #选取长和宽中较大值作为新图片的
    new_image_length = width if width > height else height
    #生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    #将之前的图粘贴在新图上，居中
    if width > height:#原图宽大于高，则填充图片的竖直维度
        #(x,y)二元组表示粘贴上图相对下图的起始位置
        new_image.paste(image, (0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image,(int((new_image_length - width) / 2),0))

    return new_image

#切图
def cut_image(image):
    width, height = image.size
    item_width = int(width / 2)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,2):#两重循环，生成9张图片基于原图的位置
        for j in range(0,2):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]
    return image_list

#保存
def save_images(image_list):
    index = 1
    for image in image_list:
        image.save('F:/image_cut/result_image/'+str(index) + '.bmp')
        index += 1

def bit_image():
    I = Image.open('F:/image_cut/source_image/face.jpg')
    # I.show()
    L = I.convert('1')
    # L.save('F:/image_cut/result_image/result.jpg')
    L.save(save_path)
    # L.show()

if __name__ == '__main__':
    # file_path = "F:/image_cut/source_image/face.jpg"
    # save_path = "F:/image_cut/result_image/result.jpg"
    # image = Image.open(file_path)
    image = Image.open(save_path)
    # image = Image.open(img)
    # image.show()
    image = fill_image(image)
    image_list = cut_image(image)
    save_images(image_list)