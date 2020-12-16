from PIL import Image
import os

pic_path = 'F:/image_cut/source_image/'  # 需要修改的图片路径
save_path = 'F:/image_cut/gray_image/'  # 保存图片路径
pic_name = os.listdir(pic_path)  # 获取原路径下的图片

for i in range(len(pic_name)):
    name = pic_name.pop()
    print(name)
    img = Image.open(pic_path + name).convert('L')  # 转换图片
    img.save(save_path + name)  # 保存