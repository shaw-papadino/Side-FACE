# -*- coding: utf-8 -*-

import cv2
import glob
import collections
import os
import shutil
import time
import random

class Detection:
    """横側からの笑顔を認識する"""

    path = "/Users/okayamashoya/NeoTrainingAssistant/static/img_dst/"
    path_img = path + "201804280930/"

    #1層目の検出器 "201804280930/"
    cascade_1 = path + "201804280930/"
    #2層目の検出器
    cascade_2 = path + "201805071842/"
    #カスケード
    cascade_path = 'cascade/lbp_in_out_aki_tsuji/cascade.xml'
    #検出器読み込み
    sideface_cascade = cv2.CascadeClassifier(path_1 + cascade_path)
    second_cascade = cv2.CascadeClassifier(path_2 + cascade_path)

    p_list = path_img + 'positive_in_out_aki_tsuji.dat'
    n_list = path_img + 'negative_in_out_aki_tsuji.dat'
    #Positive数読み込み
    P_s= sum(1 for line in open(p_list))
    P_file = open(p_list, 'r')
    P_f = P_file.readlines()
    #Negative数読み込み
    N_s = sum(1 for line in open(n_list))
    N_file = open(n_list, "r")
    N_f = N_file.readlines()
    file_lists = glob.glob(path_test + "img/*.jpg")


    #パラメータ
    #実際_認識
    P_P = 0
    P_N = 0
    N_N = 0
    N_P = 0
    Dis = 0
    noise = 0

    #画像入れ込み
    path_dir = path + "img_croppy/"
    noise_dir = "noise0612/"
    P_N_dir = "P_N_0623/"
    P_P_dir = "P_P_0623/"
    N_P_dir = "N_P_0623/"

    def dir_exist(self):
        """ディレクトリ存在確認"""
        for dir0 in [self.P_P_dir, self.N_P_dir]:
            filepath = self.path_dir + dir0
            if not os.path.exists(filepath):
                    os.mkdir(filepath)

    def img_preprocessing(self, file_img):
        """前処理を行う関数"""
        global img
        img = cv2.imread(file_img, cv2.IMREAD_COLOR)
        global yAxis
        yAxis = cv2.flip(img, 1)
        # グレースケール変換
        gray = cv2.cvtColor(yAxis, cv2.COLOR_BGR2GRAY)
        #横顔を検知
        faces = sideface_cascade.detectMultiScale(gray, 1.1, 3)
        #消す
        f_name = os.path.splitext(os.path.basename(file_img))[0]

        return faces, f_name

    def flag_add(self, fa,　type_p_n):
        """顔がある画像を計算する関数"""
        if type_p_n == 0:
            if fa > 0 :
                global P_P
                P_P += 1
            else:
                global P_N
                P_N += 1
        elif type_p_n == 1:
            if fa > 0 :
                global N_P
                N_P += 1
            else:
                global N_N
                N_N += 1
        else:
            pass

    def face_clips(self, faces, f_n):
        for (x, y, w, h) in faces:
            global img1
            img1 = img[y:y + h,x: x + w]
            if type_p_n == 0:
                if w * h > 400 * 400:
                    cv2.imwrite(self.path_dir + self.P_P_dir + f_n + str(fa_p) + "L" + ".jpg", img1)
                    fa_p += 1
                    return fa_p
                else:
                    cv2.imwrite(self.path_dir + self.P_P_dir + f_n + str(fa_n) + "l" +  ".jpg", img1)
                    fa_n += 1
            elif type_p_n == 1:
                if w * h > 400 * 400:
                    cv2.imwrite(self.path_dir + self.N_P_dir + f_n + str(fa_p2) + "L" + ".jpg", img1)
                    fa_p2 += 1
                    return fa_p2
                else:
                    cv2.imwrite(self.path_dir + self.N_P_dir + f_n + str(fa_n2) + "l" + ".jpg", img1)
                    fa_n2 += 1

    def sideface_detect(self):
        """横笑顔検出を行う関数"""
        for file_list in file_lists:
            faces, f_name = img_preprocessing(file_list)
            l_in = [s for s in self.P_f if f_name in s]
            if len(l_in) != 0:
                fa_p = 0
                fa_n = 0
                fa_p = face_clips(faces, f_name)
                flag_add(fa_p,0)
             else:
                 l_in = [s for s in N_f if f_name in s]
                 if len(l_in) != 0:
                     fa_p2 = 0
                     fa_n2 = 0
                     fa_p2 = face_clips(faces)
                     flag_add(fa_p2,1)
                 else:
                     global Dis
                     Dis += 1
    def print_all(self):
        print("All : {0} ".format(len(self.file_lists)))
        print("P_s : {0} ".format(self.P_s))
        print("N_s : {0} ".format(self.N_s))
        print("P_P : {0} ".format(self.P_P))
        print("P_N : {0}".format(self.P_N))
        print("N_N : {0}".format(self.N_N))
        print("N_P : {0}".format(self.N_P))
        print("Dis: {0}".format(self.Dis))


if __name__ == "__main__":
    d = Detection()
    d.dir_exist()
    d.sideface_detect()
    d.print_all()
