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
    # 拍照软件保存图像
    # pyautogui.moveTo(119, 1056, duration=1)
    # pyautogui.click()
    # pyautogui.moveTo(57, 70, duration=1)
    # pyautogui.click()
    # time.sleep(2)

    # 图片导入
    # ap = argparse.ArgumentParser("E:/LYK/Images/particle_1_1.jpg")

    image = cv2.imread('E:/LYK/Images/particle_1_1.jpg')

    # 转化为灰度图并减少高频噪声
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]#显示模糊图像的最亮区域
    # 去除剩余图像的噪声
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    labels = measure.label(thresh, neighbors=8, background=0)
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
        if numPixels > 3:
            mask = cv2.add(mask, labelMask)

    #在图片上绘制红圈
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts)[0]

    # print("请输入探针在CCD上的x坐标")
    # x1 = int(input())
    # print("请输入探针在CCD上的y坐标")
    # y1 = int(input())

    #设置存储点坐标的数组
    points = []
    distances = []
    for (i, c) in enumerate(cnts):
        #标记图片中的亮点
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)

        #确定取点的坐标范围
        xInArea = cX <= 1460 and cX >= 480
        yInArea = cY <= 1160 and cY >= 240
        print(cX, cY)
        if xInArea and yInArea:
          points.append([int(cX), int(cY)])
        #将点框出
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)


    # #选择最小距离的点
    # for j in points:
    #     d = (j[0]-x1)*(j[0]-x1) + (j[1]-y1)*(j[1]-y1)
    #     distances.append(d)
    # if len(distances) == 0:
    #     print('颗粒识别图像为空')
    #     return
    # k = distances.index(min(distances))
    # print(points[k])

    #显示处理后图片
    image = cv2.resize(image, (683, 680))
    cv2.imshow("Image", image)
    cv2.imwrite('E:/LYK/Images/detection.jpg', image)
    cv2.waitKey(0)

    #打印可用点的坐标
    print(points)

if __name__ == '__main__':
    get_point()