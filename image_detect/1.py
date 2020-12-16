from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

# 图片灰度化
# image = cv2.imread("C:/Users/w/Desktop/12.14组会图形/1.jpg")
image = cv2.imread("D:/2 success.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# 改变图片尺寸
image = cv2.resize(blurred, (1024, 1020))

# 设置亮点阈值
thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]

#清除小的噪点（腐蚀膨胀）
# thresh = cv2.erode(thresh, None, iterations=1)#iteration的值越高，模糊程度(腐蚀程度)就越高 呈正相关关系
# thresh = cv2.dilate(thresh, None, iterations=1)

#连接组件分析
labels = measure.label(thresh, neighbors=8, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")
for label in np.unique(labels):
  if label == 0:
    continue

  labelMask = np.zeros(thresh.shape, dtype="uint8")
  labelMask[labels == label] = 255
  numPixels = cv2.countNonZero(labelMask)

  if numPixels > 300:
    mask = cv2.add(mask, labelMask)

cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = contours.sort_contours(cnts)[0]


# loop over the contours
for (i, c) in enumerate(cnts):
  # draw the bright spot on the image
  (x, y, w, h) = cv2.boundingRect(c)
  ((cX, cY), radius) = cv2.minEnclosingCircle(c)
  cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
  cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

# cv2.imshow("Image", thresh)
# cv2.waitKey(0)
