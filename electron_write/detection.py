#导入常用的包
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import pyautogui
import time

def get_point():
    image = cv2.imread('D:/2 success.jpg')

    # 转化为灰度图并减少高频噪声
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]#显示模糊图像的最亮区域
    # 去除剩余图像的噪声
    thresh = cv2.erode(thresh, None, iterations=1)
    thresh = cv2.dilate(thresh, None, iterations=1)

    labels = measure.label(thresh, connectivity=2, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")
    # loop over the unique components
    for label in np.unique(labels):
        # 如果是空标签，忽略
        if label == 0:
            continue

        #否则统计亮点的像素值
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)

        #设定取的点的像素阈值
        if numPixels > 2:
            mask = cv2.add(mask, labelMask)

    #在图片上绘制红圈
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts)[0]

    #设置存储点坐标的数组
    points = []
    distances = []
    for (i, c) in enumerate(cnts):
        #标记图片中的亮点
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)

        #确定取点的坐标范围
        xInArea = 1460 >= cX >= 480
        yInArea = 1160 >= cY >= 240
        print(cX, cY)
        if xInArea and yInArea:
          points.append([int(cX), int(cY)])
        #将点框出
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    #显示处理后图片
    image = cv2.resize(image, (1024, 1020))
    cv2.imshow("Image", image)
    cv2.imwrite('D:/detection.jpg', image)
    cv2.waitKey(0)

    #打印可用点的坐标
    print(points)

if __name__ == '__main__':
    get_point()