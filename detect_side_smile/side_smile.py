# -*- coding: utf-8 -*-

import cv2
import glob
import os
import sys
from datetime import datetime
from face_square_clips import face_square_clips
from dir_exists import dir_exists
class Detection:
    """横側からの笑顔を検出する"""

    def __init__(self, path = "./201804280930/",cascade = "cascade/0629_neo/cascade.xml", m_size = 450):#"cascade/0629_neo/cascade.xml"
        self.path_img = path
        self.file_lists = sorted(glob.glob(self.path_img + "img_nama/*.jpg"))
        self.p_list = self.path_img + "positive_1_addshort.dat"#通常はpositive_1.dat
        self.n_list = self.path_img + "negative_2.dat"
        self.cascade = cv2.CascadeClassifier(path + cascade)
        # 0
        # self.filepath_list = dir_exists(path, str(datetime.now().time()) + str(m_size))

        # Positive数読み込み
        self.P_s= sum(1 for line in open(self.p_list))
        self.P_f = open(self.p_list, 'r')
        self.P_l = self.P_f.readlines()

        # Negative数読み込み
        self.N_s = sum(1 for line in open(self.n_list))
        self.N_f = open(self.n_list, "r")
        self.N_l = self.N_f.readlines()
        self.m_size = m_size

    def check_detection_sideface(self):
        """検出が正しいのか確認を行う関数"""
        P_P = 0
        P_N = 0
        N_P = 0
        N_N = 0
        exc = 0
        for file_list in self.file_lists:
            flg, img, img_file_name = face_square_clips(self.cascade, file_list, self.m_size)
            P_in = 0
            N_in = 0
            for s in self.P_l:
                s = s.replace("img/", "").replace(".jpg", "")
                s = s.split(" ")
                if img_file_name == s[0]:
                    P_in += 1


            #print(P_in)
            if P_in != 0:
                if flg == True:
                    P_P += 1
                    cv2.imwrite(self.filepath_list[0] + "/" + img_file_name + ".jpg", img)
                else:
                    P_N += 1
                    cv2.imwrite(self.filepath_list[1] + "/" + img_file_name + ".jpg", img)
            else:

                for s in self.N_l:

                    s = s.replace("img/", "").replace(".jpg", "").replace("\n", "")
                    #s = s.split(" ")
                    #print("'s{0}'".format(s))
                    #print(img_file_name)
                    if img_file_name == s:
                        #print("o")
                        N_in += 1
                #print(N_in)

                if N_in != 0:
                    if flg == True:
                        N_P += 1
                        #img = cv2.imread(file_list, cv2.IMREAD_COLOR)
                        cv2.imwrite(self.filepath_list[2] + "/" + img_file_name + ".jpg", img)
                    else:
                        N_N += 1
                else:
                    exc += 1
        result_d = {"ALL": len(self.file_lists), "P_s": self.P_s, "N_s": self.N_s, "P_P": P_P, "P_N": P_N, "N_P": N_P, "N_N": N_N, "EXC": exc, "Size": self.m_size}
        for key, value in result_d.items():
            print("key:", key, "-- value:", str(value))


if __name__ == "__main__":
    arg = sys.argv

    if len(arg) == 1 :
        sideface = Detection()
        sideface.check_detection_sideface()

    else:
        if len(arg) == 3:
            if arg[1] == "flont":
                frontalface = Detection(arg[2], "./haarcascades/haarcascade_frontalface_default.xml")
                frontalface.check_detection_sideface()
            elif arg[1] == "flontsmile":
                frontalsmile = Detection(arg[2], "./haarcascades/haarcascades_smile.xml")
                frontalsmile.check_detection_sideface()
