# -*- coding: utf-8 -*-
import cv2
import os

def face_square_clips(cascade, file_img, msize):
      """顔切り取る関数"""
      img = cv2.imread(file_img, cv2.IMREAD_COLOR)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(msize,msize), maxSize=(msize+300,msize+300))
      f_name = os.path.splitext(os.path.basename(file_img))[0]
      if len(faces) == 0:
          return False, img, f_name

      else:
          for (x, y, w, h) in faces:
              img1 = img[y:y + h,x: x + w]
              return True, img1, f_name


if __name__ == "__main__":
    import sys
    cascade = sys.argv[1]
    cascade = cv2.CascadeClassifier(cascade)
    img = sys.argv[2]
    size = int(sys.argv[3])
    flg, img_r, filename = face_square_clips(cascade, img, size)

    print(flg)
