# -*- coding: utf-8 -*-
import cv2
import os

def face_square_clips(cascade, file_img, msize):
      """顔切り取る関数"""
      img = cv2.imread(file_img, cv2.IMREAD_COLOR)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(msize,msize), maxSize=(msize+50,msize+50))
      f_name = os.path.splitext(os.path.basename(file_img))[0]
      if len(faces):
          for (x, y, w, h) in faces:
              img1 = img[y:y + h,x: x + w]
              return True, img1, f_name
      else:
          return False, img, f_name


if __name__ == "__main__":
    pass
