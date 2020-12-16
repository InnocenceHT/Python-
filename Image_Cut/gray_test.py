import cv2
from PIL import Image
import numpy as np

imagepath = r'F:/image_cut/source_image/face.jpg'
image = cv2.imread(imagepath)

# gray=cv2.cvtColor(image,cv2,COLOR_BGR2GRAY)
cv2.imshow("Image Title", image)

# gray=Image.open('head.jpg').convert('L')
a = np.array(Image.open("F:/image_cut/source_image/face.jpg").convert('L')).astype('float')

depth = 10.
grad = np.gradient(a)
grad_x, grad_y = grad

grad_x = grad_x * depth / 100.
grad_y = grad_y * depth / 100.
A = np.sqrt(grad_y ** 2 + grad_y ** 2 + 1)
uni_x = grad_x / A
uni_y = grad_y / A
uni_z = 1. / A

vec_el = np.pi / 2.2
vec_az = np.pi / 4
dx = np.cos(vec_el) * np.cos(vec_az)
dy = np.cos(vec_el) * np.sin(vec_az)
dz = np.sin(vec_el)

b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)
b = b.clip(0, 225)

im = Image.fromarray(b.astype('uint8'))
im.save('F:/image_cut/gray_image/gray.jpg')
im.show()
# cv2.imshow("gray ",gray)
cv2.waitKey(5)