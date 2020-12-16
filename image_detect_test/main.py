#导入常用的包
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import pyautogui
import time

lp = 0.13 #CCD单个像素点的大小

# 手动输入针尖在CCD上的坐标
print("请输入探针在CCD上的x坐标")
x1 = int(input())
print("请输入探针在CCD上的y坐标")
y1 = int(input())
print(x1, y1)


def get_point():
    #图片导入
    ap = argparse.ArgumentParser()
    image = cv2.imread('E:/LYK/Images/particle_1_1.jpg')

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

        #确定取点的坐标范围
        xInArea = cX < 1000 and cX > 435
        yInArea = cY < 1300 and cY > 795
        if xInArea and yInArea :
          points.append([int(cX), int(cY)])
        # print(cX, cY)
        #将点框出
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    #显示处理后图片
    image = cv2.resize(image, (1024, 1020))
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)

    #打印可用点的坐标
    print(points)
    p1 = points[1]
    #返回一个坐标点的值
    return p1

#处理点的坐标
def handle_loaction():


    # 获取量子点的坐标
    c = get_point()
    x2 =int(c[0])
    y2 =int(c[1])
    print(x2, y2)


    # 获取NOVA软件中的针尖位置坐标
    print("请输入针尖在NOVA上的X坐标!")
    X1 = int(input())
    print("请输入针尖在NOVA上的Y坐标!")
    Y1 = int(input())
    print(X1, Y1)

    #最小化pycharm
    pyautogui.moveTo(1808, 8, duration=1)
    pyautogui.click()
    time.sleep(2)

    # 打开NOVA软件
    pyautogui.moveTo(44, 35, duration=0.5)
    pyautogui.doubleClick()
    time.sleep(15)

    #AFM操作标准流程







    # 点击SCANNING按钮
    pyautogui.moveTo(515, 103, duration=2)
    pyautogui.click()
    print("已点击scanning按钮!")
    # 点击probe按钮
    pyautogui.moveTo(369, 269, duration=2)
    pyautogui.click()
    print("已点击probe按钮!")

    # LX,LY为最终到达点的坐标
    # 点击十字按钮开始拖动
    #a,b表示针尖在电脑屏幕中的像素点坐标
    a = 545 + 5.57 * X1
    b = 940 - 5.57 * Y1

    #A,B表示NOVA软件当中量子点在电脑屏幕中的像素坐标
    A = 545 + 5.57 * X1 + 5.57 * 0.13 * (x2 - x1)
    B = 940 - 5.57 * Y1 + 5.57 * 0.13 * (y2 - y1)
    #移动针尖到目标点
    pyautogui.moveTo(a, b, duration=2)
    pyautogui.dragTo(A, B, 5, button='left')
    print("已将针尖移动至目标点!")
    time.sleep(2)

    #点击区域选择按钮
    pyautogui.moveTo(398, 273, duration=2)
    pyautogui.click()
    print("已点击区域选择按钮!")


    #设置下次扫描的区域
    pyautogui.moveTo(901, 630, duration=2)
    pyautogui.dragTo(A, B, 2, button='left')
    time.sleep(1)

    #点击run进行扫描
    pyautogui.moveTo(35, 216, duration=1)
    pyautogui.click()
    print("已点击Run按钮开始扫描!")



if __name__ == '__main__':
    # get_point()
    handle_loaction()