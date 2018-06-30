# -*- coding: utf-8 -*-

import glob
import cv2

def face_detect(path, extension):
    """画像から顔認識する関数"""
    img_file_lists = glob.glob(path + "*." + extension)
    sideface_cascade = cv2.CascadeClassifier("/Users/okayamashoya/Downloads/face_mov/haarcascades/haarcascade_frontalface_default.xml")
    for img_file_list in img_file_lists:
        img = cv2.imread(img_file_list, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = sideface_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        f_name = os.path.splitext(os.path.basename(img_file_list))[0]
        if len(faces) > 0:
            cv2.imwrite(path + "detect/" + f_name + extension, img)


if __name__ == "__main__":
    pass
