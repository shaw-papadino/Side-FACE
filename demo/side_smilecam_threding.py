# -*- coding: utf-8 -*-

import time
import cv2
# import picamera
import datetime
import os

from timeit import default_timer as timer
from threading import (Event, Thread)
# import getch

# event = Event()
# now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
# mov_path = now + ".avi"
# h_path = now + ".h264"
# filepath = "/home/pi/"
# side_path = filepath + "sideye/"
# fisheye_path = filepath + "fisheye/"
# CAM_WIDTH = 1000
# CAM_HEIGHT = 750

# if not os.path.exists(side_path):
# 	os.mkdir(side_path)
# if not os.path.exists(fisheye_path):
# 	os.mkdir(fisheye_path)

def side_rec():

	cam = picamera.PiCamera()
	cam.vflip = True
	cam.hflip = True
	cam.resolution = (CAM_WIDTH, CAM_HEIGHT)
	cam.framerate = 25

	event.wait()
	cam.start_recording(side_path + h_path)

def main(fisheye_path, mov_path):

	cap = cv2.VideoCapture(1) #引数はカメラのデバイス番号
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	if cap.isOpened() == False:
		print("Not connected!")
	cap.set(3, 1024)#640480fps5
	cap.set(4, 768)
	mov = cv2.VideoWriter(fisheye_path + mov_path, fourcc, 12, (1024,768))

	ORG_WINDOW_NAME = "org"
	cv2.namedWindow(ORG_WINDOW_NAME)
	accum_time = 0
	curr_fps = 0
	fps = "FPS: ??"
	prev_time = timer()

	frame_count = 1
	# event.set()

	while True:
		#now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		#img_path = now + ".jpg"
		ret, imgcv = cap.read()

		# start = time.time()
		# xAxis =
		yAxis = cv2.flip(cv2.flip(imgcv, 0), 1)
		mov.write(yAxis)
        # time.sleep(0.08)

        # Calculate FP
		curr_time = timer()
		exec_time = curr_time - prev_time
		prev_time = curr_time
		accum_time = accum_time + exec_time
		curr_fps = curr_fps + 1
		if accum_time > 1:
			accum_time = accum_time - 1
			fps = "FPS:" + str(curr_fps)
			curr_fps = 0
        # Draw FPS in CUI
		print(fps)
		cv2.imshow(ORG_WINDOW_NAME, yAxis)
		# 1msec待つ
		if cv2.waitKey(10) & 0xFF == ord('q'):
			break
		# cv2.destroyAllWindows()
	cap.release()
	mov.release()
"""
try:
	now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	mov_path = now + ".avi"
	h_path = now + ".h264"
	mov = cv2.VideoWriter(fisheye_path + mov_path, fourcc, 8, (1000,750))
	cam.start_recording(side_path + h_path)
	print("start")
	while True:
		#now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		#img_path = now + ".jpg"
		ret, imgcv = cap.read()

		start = time.time()
		xAxis = cv2.flip(imgcv, 0)
		yAxis = cv2.flip(xAxis, 1)
		mov.write(yAxis)
		time.sleep(0.08)
except KeyboardInterrupt:
	cap.release()
	mov.release()
	elapsed_time = time.time() - start
	print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
"""

if __name__ == '__main__':

	thread = Thread(target=side_rec)
	thread.start()
	main()
