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

#设定红色阈值，HSV空间  
redLower = np.array([170, 100, 100])  
redUpper = np.array([179, 255, 255])  
#初始化追踪点的列表  
mybuffer = 16  
pts = deque(maxlen=mybuffer)  
counter = 0  
#打开摄像头  
camera = cv2.VideoCapture(0)  
#等待两秒  
time.sleep(3)
e1=cv2.getTickCount()
#遍历每一帧，检测红色瓶盖  
while True:  
    #读取帧  
    (ret, frame) = camera.read()  
    #判断是否成功打开摄像头  
    if not ret:  
        print ('No Camera') 
        break
    #e1=cv2.getTickCount()
    #frame = imutils.resize(frame, width=600)  
    #转到HSV空间  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    #根据阈值构建掩膜  
    mask = cv2.inRange(hsv, redLower, redUpper)  
    #腐蚀操作  
    mask = cv2.erode(mask, None, iterations=2)  
    #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点  
    mask = cv2.dilate(mask, None, iterations=2)
    res  =cv2.bitwise_and(frame ,frame,mask=mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  
    #初始化瓶盖圆形轮廓质心
    center = None  #
    #print(cnts)
    #如果存在轮廓
    
    if len(cnts) > 0:  
        #找到面积最大的轮廓  
        c = max(cnts, key = cv2.contourArea)  
        #确定面积最大的轮廓的外接圆  
        ((x, y), radius) = cv2.minEnclosingCircle(c)  
		#计算轮廓的矩  
        M = cv2.moments(c)  
        #计算质心  
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))  
        #只有当半径大于10时，才执行画图  
        if radius > 10:   
            #把质心添加到pts中，并且是添加到列表左侧
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 2)  
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #print(center[0])
            #pts.appendleft(center)
            arr[4]=0x01#找到目标标志，小车前进
            if center[0]<210:
                #左转
                arr[5]=0x01
                arr[6]=0x5d+1
                print('L')
            elif center[0]>420:
                #右转
                arr[5]=0x04
                arr[6]=0x60+1
                print('R')
            else :
                #前进
                arr[5]=0x02
                arr[6]=0x5e+1
                print('up')
                
            
            
    else :
    
        arr[4]=0x03#没有找到目标 转圈
        arr[5]=0x01
        arr[6]=0x5d+3
        print('Stop')
    SendData(ser,arr)         
    cv2.imshow('Frame', frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #键盘检测，检测到esc键退出  
    k = cv2.waitKey(1)&0xFF
    e2=cv2.getTickCount()
    ss=(e2-e1)/cv2.getTickFrequency()
    #cv2.imwrite('/home/pi/Desktop/Pic/MID1/'+str(counter)+'.jpeg',frame)
    counter += 1
    """
    if ss>=4:
        arr=[0xaa,0xaf,0x03,0x00,0x00,0x00,0x5c] #a[4] 1前进 2后退 3转圈
        SendData(ser,arr)
        break
     """   
    if k == 27:
        arr=[0xaa,0xaf,0x03,0x00,0x00,0x00,0x5c] #a[4] 1前进 2后退 3转圈
        SendData(ser,arr)
        break
    #e2=cv2.getTickCount()
    #time=(e1-e2)/cv2.getTickFrequency()
    #print(time)
    #rint(cv2.useOptimized())  #确认已经优化
#摄像头释放  
camera.release()
#销毁所有窗口  
cv2.destroyAllWindows()  

