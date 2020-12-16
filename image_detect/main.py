#导入常用的包
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

def get_point():
    #图片导入
    ap = argparse.ArgumentParser()
    image = cv2.imread('D:/2 success.jpg')

    #转化为灰度图并减少高频噪声
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]#显示模糊图像的最亮区域
    #去除剩余图像的噪声
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

    #设置存储点坐标的数组
    points = []

    for (i, c) in enumerate(cnts):
        #标记图片中的亮点
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)

        # 确定取点的坐标范围
        # xInArea = cX < 1000 and cX > 435
        # yInArea = cY < 1300 and cY > 795
        xInArea = cX < 2048 and cX > 0
        yInArea = cY < 2040 and cY > 0
        if xInArea and yInArea:
            points.append([int(cX), int(cY)])
        # print(cX, cY)
        # 将点框出
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 2)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    #显示处理后图片
    image = cv2.resize(image, (1024, 1020))
    cv2.imshow("Image", image)
    cv2.waitKey(0)

    #打印可用点的坐标
    # print(points)
    p1 = points[1]
    #返回一个坐标点的值
    return p1

#处理点的坐标
def handle_loaction():
    b = get_point()
    x = b[0]
    y = b[1]
    print(x, y)


if __name__ == '__main__':
    handle_loaction()