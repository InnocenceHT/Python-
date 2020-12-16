import tkinter as tk
from tkinter import filedialog, dialog
from PIL import Image, ImageTk
import os
import sys
import clr
import time
# import System
import pyautogui

# assembly_path= r"C:\Program Files\Thorlabs\Kinesis"
# sys.path.append(assembly_path)

# clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
# clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
# clr.AddReference("Thorlabs.MotionControl.Tools.Common")
# clr.AddReference("Thorlabs.MotionControl.Tools.Logging")
# clr.AddReference("Thorlabs.MotionControl.KCube.DCServoCLI ")
# from Thorlabs.MotionControl.DeviceManagerCLI import *
# from Thorlabs.MotionControl.GenericMotorCLI import *
# from Thorlabs.MotionControl.KCube.DCServoCLI import *
# from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import *
# from Thorlabs.MotionControl.GenericMotorCLI.AdvancedMotor import *
# from Thorlabs.MotionControl.GenericMotorCLI.KCubeMotor import *
# from Thorlabs.MotionControl.GenericMotorCLI.Settings import *
import pyautogui
import time
time.sleep(3)


# 打开Nova软件
pyautogui.moveTo(75, 1060, duration=1)
pyautogui.click()
time.sleep(1)

def open_file(file_name):
    # 点击litho按钮
    pyautogui.moveTo(550, 68, duration=1)
    pyautogui.click()
    time.sleep(0.5)

    # 打开文件1.bmp
    pyautogui.moveTo(590, 94, duration=1)
    pyautogui.click()
    time.sleep(1)
    # 按下删除
    pyautogui.press("BackSpace")
    # 导入文件
    time.sleep(1)
    pyautogui.typewrite(file_name)
    pyautogui.moveTo(1280, 864, duration=1)
    pyautogui.click()
    time.sleep(1)

    # 设置扫描范围
    pyautogui.moveTo(216, 150, duration=1)
    pyautogui.click()
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    time.sleep(1)
    pyautogui.typewrite("100")
    pyautogui.moveTo(279, 148, duration=1)
    pyautogui.click()
    time.sleep(1)
    # 设置扫描时间
    pyautogui.moveTo(166, 124, duration=1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(148, 167, duration=1)
    pyautogui.click()
    time.sleep(1)
    # 确定扫描时间
    pyautogui.moveTo(215, 120, duration=1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.press("BackSpace")
    pyautogui.typewrite("300000")
    # 开始扫描
    pyautogui.moveTo(38, 116, duration=1)
    pyautogui.click()
    time.sleep(1)
    # 抬起探针
    
#x方向位移台的移动
def x_stage_moveto(x):
    print("开始移动位移台！")
    DeviceManagerCLI.BuildDeviceList()
    # serialNo = DeviceManagerCLI.GetDeviceList(KCubeDCServo.DevicePrefix)
    # print(serialNo)
    # serialNo='27252847'
    device_x = KCubeDCServo.CreateKCubeDCServo('27256658')
    # print(device)
    device_x.Connect('27256658')
    device_x.WaitForSettingsInitialized(10000)
    motorconfiguration = device_x.LoadMotorConfiguration('27256658')
    motorconfiguration.DeviceSettingsName = 'MTS50/M-Z8'
    motorconfiguration.UpdateCurrentConfiguration()
    motorDeviceSettings = device_x.MotorDeviceSettings
    device_x.SetSettings(motorDeviceSettings, False)
    device_x.StartPolling(250)
    device_x.EnableDevice()


    device_x.MoveTo(System.Decimal(x), 60000)


def y_stage_moveto(y):
    print("y方向位移台开始移动！")
    DeviceManagerCLI.BuildDeviceList()
    serialNo = DeviceManagerCLI.GetDeviceList(KCubeDCServo.DevicePrefix)
    device_y = KCubeDCServo.CreateKCubeDCServo('27503144')
    device_y.Connect('27503144')
    device_y.WaitForSettingsInitialized(10000)
    motorconfiguration = device_y.LoadMotorConfiguration('27503144')
    motorconfiguration.DeviceSettingsName = 'MTS50/M-Z8'
    motorconfiguration.UpdateCurrentConfiguration()
    motorDeviceSettings = device_y.MotorDeviceSettings
    device_y.SetSettings(motorDeviceSettings, False)
    device_y.StartPolling(250)
    device_y.EnableDevice()

    #移动至相应位置
    device_y.MoveTo(System.Decimal(y), 60000)
    print("位移台移动已完成")

#Tkinter控制界面
def window():
    root = tk.Tk()
    left_frame = tk.Frame(root)
    left_frame.pack(side='left')
    right_frame = tk.Frame(root)
    right_frame.pack(side='right')
    canvas = tk.Canvas(right_frame, width=540, height=360)
    canvas.pack()
    image_button = tk.Button(left_frame, text='选择图片', command=choose_image)
    image_button.grid(row=0, column=0)
    control_button = tk.Button(left_frame, text='开始运动', command=start_move)
    control_button.grid(row=1, column=0)
    stop_button = tk.Button(left_frame, text='停止运动', command=stop_move)
    stop_button.grid(row=2, column=0)
    root.mainloop()


if __name__ == '__main__':
    # open_file("1.bmp")#第一张图片
    # x_stage_moveto(0.1)
    # open_file("2.bmp")#第二张图片
    # y_stage_moveto(0.1)
    # open_file("4.bmp")#第三张图片
    # x_stage_moveto(0.0)
    # open_file("3.bmp")#第四张图片
    for i in [1,2,3]:
        print(i)