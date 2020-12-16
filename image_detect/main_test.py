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

#输入探针在CCD上的坐标
print("请输入探针在CCD上的x坐标")
x1 = int(input())
print("请输入探针在CCD上的y坐标")
y1 = int(input())

# 获取NOVA软件中的针尖位置坐标
print("请输入针尖在NOVA上的X坐标!")
X1 = int(input())
print("请输入针尖在NOVA上的Y坐标!")
Y1 = int(input())
print(X1, Y1)

#显示探针光学图像并调节曝光时间(10ms)
pyautogui.moveTo(119, 1056, duration=1)
pyautogui.click()
pyautogui.moveTo(106, 246, duration=1)
pyautogui.click()
pyautogui.press('Delete')
pyautogui.press('Delete')
pyautogui.press('Delete')
pyautogui.typewrite('10')
time.sleep(2)
pyautogui.press('Enter')
time.sleep(5)


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


    #选择最小距离的点
    for j in points:
        d = (j[0]-x1)*(j[0]-x1) + (j[1]-y1)*(j[1]-y1)
        distances.append(d)
    if len(distances) == 0:
        print('颗粒识别图像为空')
        return
    k = distances.index(min(distances))
    print(points[k])

    #显示处理后图片
    image = cv2.resize(image, (683, 680))
    cv2.imshow("Image", image)
    pyautogui.moveTo(260, 1057, duration=1)
    pyautogui.click()
    cv2.waitKey(5000)

    #打印可用点的坐标
    print(points)
    p1 = points[k]
    #返回一个坐标点的值
    return p1

#处理点的坐标
def handle_loaction():
    # 获取量子点的坐标
    c = get_point()
    x2 =int(c[0])
    y2 =int(c[1])
    print(x2, y2)

    #最小化pycharm
    # pyautogui.moveTo(1808, 8, duration=1)
    # pyautogui.click()
    # time.sleep(2)

    # 打开NOVA软件
    pyautogui.moveTo(67, 1058, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    # 点击SCANNING按钮
    pyautogui.moveTo(515, 103, duration=2)
    pyautogui.click()
    print("已点击scanning按钮!")

    #点击area按钮
    pyautogui.moveTo(453, 234, duration=2)
    pyautogui.click()
    print("已点击scanning按钮!")

    # 点击MoveProbe按钮
    pyautogui.moveTo(370, 267, duration=2)
    pyautogui.click()
    print("已点击MoveProbe按钮!")

    # LX,LY为最终到达点的坐标
    # 点击十字按钮开始拖动
    #a,b表示针尖在电脑屏幕中的像素点坐标
    a = 535 + 5.77 * X1
    b = 962 - 5.77 * Y1

    #A,B表示NOVA软件当中量子点在电脑屏幕中的像素坐标
    A = 535 + 5.77 * X1 + 5.77 * 0.083 * (x2 - x1)
    B = 962 - 5.77 * Y1 + 5.77 * 0.083 * (y2 - y1)

    #移动探针之前将FB关闭
    pyautogui.moveTo(476, 171, duration=2)
    pyautogui.click()
    print("已关闭FB按钮!")

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
    pyautogui.moveTo(903, 643, duration=2)
    pyautogui.dragTo(A, B, 5, button='left')
    time.sleep(1)


    #将扫描区域调为5um
    pyautogui.moveTo(1787, 319, duration=2)
    pyautogui.click()
    pyautogui.press('BackSpace')
    pyautogui.press('BackSpace')
    pyautogui.press('BackSpace')
    pyautogui.press('BackSpace')
    pyautogui.press('BackSpace')
    pyautogui.press('BackSpace')
    pyautogui.press('BackSpace')
    pyautogui.typewrite('5.000')
    pyautogui.press('Enter')
    print("已调节完毕扫描区域!")
    time.sleep(1)


    #将FB打开准备扫描
    pyautogui.moveTo(463, 168, duration=2)
    pyautogui.click()
    print("已重新打开FB按钮!")

    #点击run进行扫描
    pyautogui.moveTo(43, 215, duration=1)
    pyautogui.click()
    print("已点击Run按钮开始扫描!")

    #回到CCD页面，调节曝光时间（400ms）
    pyautogui.moveTo(119, 1056, duration=1)
    pyautogui.click()
    pyautogui.moveTo(106, 246, duration=1)
    pyautogui.click()
    pyautogui.press('Delete')
    pyautogui.press('Delete')
    pyautogui.press('Delete')
    pyautogui.typewrite('600')
    time.sleep(2)
    pyautogui.press('Enter')
    time.sleep(5)

    #等待探针扫描结束
    time.sleep(185)

    #扫描结束，回到NOVA
    pyautogui.moveTo(67, 1058, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    #抬起探针
    pyautogui.moveTo(397, 107, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(227, 213, duration=0.5)
    pyautogui.click()
    time.sleep(2)
    pyautogui.click()

    #回到CCD
    pyautogui.moveTo(119, 1056, duration=1)
    pyautogui.click()
    #曝光时间调到10ms
    pyautogui.moveTo(106, 246, duration=1)
    pyautogui.click()
    pyautogui.press('Delete')
    pyautogui.press('Delete')
    pyautogui.press('Delete')
    pyautogui.typewrite('10')
    time.sleep(2)
    pyautogui.press('Enter')
    time.sleep(5)
    #曝光时间调到400ms
    pyautogui.moveTo(106, 246, duration=1)
    pyautogui.click()
    pyautogui.press('Delete')
    pyautogui.press('Delete')
    pyautogui.press('Delete')
    pyautogui.typewrite('600')
    time.sleep(2)
    pyautogui.press('Enter')
    time.sleep(5)

if __name__ == '__main__':
    handle_loaction()