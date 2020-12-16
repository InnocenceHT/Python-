#导入常用的包
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2

#对图片进行预处理，去除噪声点
ap = argparse.ArgumentParser()
image = cv2.imread('D:/test_image/2 success.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
# thresh = cv2.erode(thresh, None, iterations=2)
# thresh = cv2.dilate(thresh, None, iterations=4)
# img = cv2.imread('D:/test_image/2 success.jpg')

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(thresh, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(thresh, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        dst = cv2.resize(thresh, (1024, 1020))
        cv2.resizeWindow('image', 1024, 1020)
        cv2.imshow("image", dst)
        # cv2.imshow("image", thresh)
        print(x, y)

while True:
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    dst = cv2.resize(thresh, (1024, 1020))
    cv2.resizeWindow('image', 1024, 1020)
    cv2.imshow("image", dst)

    if cv2.waitKey(0)&0xFF==27:
        break
cv2.destroyAllWindows()
cv2.imshow("原图", thresh)
cv2.waitKey(0)