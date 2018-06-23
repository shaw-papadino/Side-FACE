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
cam.hflip = True
cam.resolution = (CAM_WIDTH, CAM_HEIGHT)
cam.framerate = 10
cap = cv2.VideoCapture(0) #引数はカメラのデバイス番号
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#out = cv2.VideoWriter(fisheye_path )
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
	now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	mov_path = now + ".avi"
	h_path = now + ".h264"
	mov = cv2.VideoWriter(fisheye_path + mov_path, fourcc, 10, (320,240))
	cam.start_recording(side_path + h_path)
	#cam.start_recording(side_path + h_path)
	while True:
		#now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		#img_path = now + ".jpg"
		ret, imgcv = cap.read()
		xAxis = cv2.flip(imgcv, 0)
		yAxis = cv2.flip(xAxis, 1)
		mov.write(yAxis)
		#cv2.imwrite(fisheye_path + img_path , xAxis)
		#time.sleep(1)
		#cam.capture(side_path + img_path)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#print("smile!")
		time.sleep(0.1)
except KeyboardInterrupt:
	cap.release()
	mov.release()
	elapsed_time = time.time() - start
	print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
