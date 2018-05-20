# -*- coding: utf-8 -*-

import time
import cv2
import picamera
import datetime
import os

filepath = "/home/pi/"
side_path = filepath + "sideye/"
fisheye_path = filepath + "fisheye/"
CAM_WIDTH = 1000
CAM_HEIGHT = 750

cam = picamera.PiCamera()
cam.vflip = True
cam.resolution = (CAM_WIDTH, CAM_HEIGHT)

cap = cv2.VideoCapture(0) #引数はカメラのデバイス番号

if cap.isOpened() == False:
    print("Not connected!")
cap.set(3, 320)
cap.set(4, 240)

if not os.path.exists(side_path):
    os.mkdir(side_path)
if not os.path.exists(fisheye_path):
    os.mkdir(fisheye_path)

start = time.time()
try:
    while True:
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        img_path = now + ".jpg"

        ret, imgcv = cap.read()
        xAxis = cv2.flip(imgcv, 0)
    	if ret == False:
    	    continue

        cv2.imwrite(fisheye_path + img_path , xAxis)
    	time.sleep(1)
        cam.capture(side_path + img_path)

        print("smile!")
        time.sleep(0.1)
except KeboardInterrupt:
    capture.release()
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
