#encoding:utf-8
from collections import  deque  
import numpy as np  
import time
import serial
import struct
#import imutils  
import cv2

counter = 0

redLower = np.array([170, 100, 100])  
redUpper = np.array([179, 255, 255])

camera = cv2.VideoCapture(0)
Wide=int(camera.get(3))#获取图像的宽
Height=int(camera.get(4))#获取图像的高
print(Wide)
print(int(Wide))
time.sleep(3)
while True:  
    (ret, frame) = camera.read()   
    if not ret:  
        print ('No Camera') 
        break
    cv2.imshow("Orign",frame)
    (B,G,R)=cv2.split(frame)
    """
    cv2.imshow("B",B)
    cv2.imshow("G",G)
    cv2.imshow("R",R)"""
    for y in range(Wide):
        for x in range(Height):
            if R[x,y]>150:
                frame[x,y]=255
            else :
                frame[x,y]=0
    k = cv2.waitKey(1)&0xFF
    cv2.imshow("Result",frame)
    counter += 1  
    if k == 27:  
        break  
#摄像头释放  
camera.release()  
#销毁所有窗口  
cv2.destroyAllWindows()  



