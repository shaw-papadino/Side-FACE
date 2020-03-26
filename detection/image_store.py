"""
画像を様々な形で保存をする
"""
import os
import cv2
import datetime
from image_check import Checker

class ImageStore():
    def __init__(self,path, mode="Image"):
        self.mode = mode
        self.Check = Checker()
        strtime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.path = path + "/" + strtime
        if self.Check.store_path(self.path):
            pass
        else:
            os.mkdir(self.path)

    def store(self, img):
        try:
            if self.mode == "Image":
                strtime = datetime.datetime.now().strftime("%H-%M-%S-%f")[:-3]
                flg = cv2.imwrite(self.path + "/" + strtime + ".jpg", img)
                if not flg:
                    raise Exception("Could not write image")
            elif self.mode == "Movie":
                self.out.write(img)
        except Exception as e:
            print(e)
    def movie_settings(self, w, h, fps=30):

        self.W = self.Check.img_size(w)
        self.H = self.Check.img_size(h)
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")

        self.out = cv2.VideoWriter(self.path, fourcc, fps, (self.W, self.H))

        return True

