#encoding:utf-8
#s 0 5c
#l 1 5d
#u 2 5e
#b 3 5f
#r 4 60
from collections import  deque  
import numpy as np  
import time  
import serial
import struct
#import imutils  
import cv2  
#串口初始化
ser = serial.Serial("/dev/ttyAMA0",115200)
print("uart open:",ser.isOpen())
#协议数组
#帧头 帧头 字长 命令1 命令2 命令3 校验和
arr=[0xaa,0xaf,0x03,0x00,0x00,0x00,0x5c] #a[4] 1前进 2后退 3转圈
def SendData(self, array):
        date=struct.pack("%dB"%(len(array)),*array)
        self.write(date)
#通过串口发送数据
SendData(ser,arr)




