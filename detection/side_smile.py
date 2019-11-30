# -*- coding: utf-8 -*-

import cv2
import glob
import os
import sys
import time
import argparse
import re
from datetime import datetime
from face_square_clips import face_square_clips
from dir_exists import dir_exists
from write_point import write_point


class Detection:
    """横側からの笑顔を検出する"""

    def __init__(self, path, cascade, m_size, flg):  # "cascade/mizumashi15/cascade.xml"
        self.path = path
        self.path_img = self.path  # + "img/"
        self.file_lists = sorted(glob.glob(self.path_img + "*.jpg"))
        self.cascade = cv2.CascadeClassifier("../models/" + cascade)
        self.datlists = glob.glob(self.path + "*.dat")
        self.m_size = m_size

        if flg:
            # "positivemizumashi.dat" , "negative_2c.dat", 区間内はaddshort
            pattern = r"positiveall"
            for dat in self.datlists:
                match = re.search(pattern, dat)
                if match:
                    self.t_list = dat
                else:
                    self.f_list = dat

            # Positive数読み込み
            self.T_s = sum(1 for line in open(self.t_list))
            self.T_f = open(self.t_list, "r")
            self.T_l = self.T_f.readlines()

            # Negative数読み込み
            self.F_s = sum(1 for line in open(self.f_list))
            self.F_f = open(self.f_list, "r")
            self.F_l = self.F_f.readlines()

            self.filepath_list = dir_exists(self.path, 1)

        else:
            self.filepath_list = dir_exists(self.path, 0)

    def smile_face_clip(self):
        P = 0
        N = 0
        for file_list in self.file_lists:
            flg, img, img_file_name, points = face_square_clips(
                self.cascade, file_list, self.m_size
            )
            if flg == True:
                P += 1
                # cv2.imwrite(self.filepath_list[0] + "/" + img_file_name + ".jpg", img)
                write_point(img_file_name, points)
            else:
                N += 1
                # cv2.imwrite(self.filepath_list[1] + "/" + img_file_name + ".jpg", img)

        return P, N

    def check_detection_sideface(self):
        """検出が正しいのか確認を行う関数"""
        T_P = 0
        F_N = 0
        F_P = 0
        T_N = 0
        exc = 0
        pattern = "image"
        for file_list in self.file_lists:

            match = re.search(pattern, file_list)

            if match:
                continue

            flg, img, img_file_name, points = face_square_clips(
                self.cascade, file_list, self.m_size
            )
            T_in = 0
            F_in = 0

            for s in self.T_l:
                s = s.replace("img/", "").replace(".jpg", "")
                s = s.split(" ")
                if img_file_name == s[0]:
                    T_in = 1
                    break
            # print(file_list)
            if T_in != 0:
                if flg == True:
                    T_P += 1
                    # cv2.imwrite(self.filepath_list[0] + "/" + img_file_name + ".jpg", img)
                else:
                    F_N += 1
                    # cv2.imwrite(self.filepath_list[1] + "/" + img_file_name + ".jpg", img)
            else:

                for s in self.F_l:
                    s = s.replace("img/", "").replace(".jpg", "").replace("\n", "")
                    if img_file_name == s:
                        F_in += 1

                if F_in != 0:
                    if flg == True:
                        F_P += 1
                        cv2.imwrite(self.filepath_list[2] + "/" + img_file_name + ".jpg", img)
                        write_point(img_file_name, points)
                    else:
                        T_N += 1
                        cv2.imwrite(self.filepath_list[3] + "/" + img_file_name + ".jpg", img)
                else:
                    exc += 1
        print(T_P, F_N)
        # result_d = {"ALL": len(self.file_lists),"T_P": T_P, "T_F": T_F, "F_T": F_T, "F_F": F_F, "Size": self.m_size}
        result_d = {
            "ALL": len(self.file_lists),
            "T_s": self.T_s,
            "F_s": self.F_s,
            "T_P": T_P,
            "F_N": F_N,
            "F_P": F_P,
            "T_N": T_N,
            "EXC": exc,
            "Size": self.m_size,
            "Precision": round(T_P / (T_P + F_P), 2),
            "Recall": round(T_P / (T_P + F_N), 2),
        }

        return result_d


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Train sidesmile estimation")
    parser.add_argument("--path", "-p", type=str, default="../data/nofish/", help="input path")
    parser.add_argument(
        "--cascadepath", "-c", type=str, default="side_smile_default_ver1.xml", help="cascade file"
    )
    parser.add_argument(
        "--mindetectsize", "-m", type=int, default=250, help="minmum detect image size"
    )
    parser.add_argument("--evaluation", "-e", type=int, default=1, help="evaluation")
    args = parser.parse_args()

    sideface = Detection(args.path, args.cascadepath, args.mindetectsize, args.evaluation)
    if args.evaluation:
        result = sideface.check_detection_sideface()
        for key, value in result.items():
            print("key:", key, "-- value:", str(value))

    else:
        P, N = sideface.smile_face_clip()
        print(P)
        print(N)
