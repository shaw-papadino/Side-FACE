# -*- coding: utf-8 -*-

import cv2
import glob
import collections
import os
import shutil
import time
import random


path = "/Users/okayamashoya/NeoTrainingAssistant/static/img_dst/"
#テストデータ "20180424113542/", 学習データ "201804280930/"
path_test = path + "201804280930/"
#path_test = path + "20180424113542/"
#/Users/okayamashoya/Pictures/20180602/side
#1層目の検出器 "201804280930/"
path_1 = path + "201804280930/"
#2層目の検出器
path_2 = path + "201805071842/"
#カスケード
cascade_path = 'cascade/lbp_in_out_aki_tsuji/cascade.xml'
#画像入れ込み
path_dir = path + "img_croppy/"
#パラメータ
#実際_認識
P_P = 0
P_N = 0
N_N = 0
N_P = 0
Dis = 0
noise = 0

#検出器読み込み
sideface_cascade = cv2.CascadeClassifier(path_1 + cascade_path)
second_cascade = cv2.CascadeClassifier(path_2 + cascade_path)

#Positive数読み込み
P_s= sum(1 for line in open(path_test + 'positive_in_out_aki_tsuji.dat'))
#Negative数読み込み
N_s = sum(1 for line in open(path_test + 'negative_in_out_aki_tsuji.dat'))
#全画像読み込み
file_lists = glob.glob(path_test + "img/*.jpg")
random.seed(0)
file_lists_r = random.sample(file_lists, 1000)

#Positiveリスト読み込み
P_file = open(path_test + 'positive_in_out_aki_tsuji.dat', 'r')
#Negativeリスト読み込み
N_file = open(path_test + 'negative_in_out_aki_tsuji.dat', "r")

#1行ずつリストにする
P_f = P_file.readlines()
N_f = N_file.readlines()

noise_dir = "noise0612"

P_N_dir = "P_N_0623/"
P_P_dir = "P_P_0623/"
N_P_dir = "N_P_0623/"
for dir0 in [P_P_dir, N_P_dir]:
    filepath = path_dir + dir0
    if not os.path.exists(filepath):
            os.mkdir(filepath)




def remove(filepath):
    files = os.listdir(filepath)
    if len(files) > 0 :
        os.remove(filepath + "/*.jpg")
    
def write(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    cv2.imwrite(filepath + f_remove , img)
def write1(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    cv2.imwrite(filepath + f_remove , img1)

def write2(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    cv2.imwrite(filepath + f_remove , img2)

def write3(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    cv2.imwrite(filepath + f_remove , img3)
    
def sideface_core1():
    
    for file_list in file_lists:
        global img
        img = cv2.imread(file_list, cv2.IMREAD_COLOR)
        global yAxis
        yAxis = cv2.flip(img, 1)
        # グレースケール変換
        gray = cv2.cvtColor(yAxis, cv2.COLOR_BGR2GRAY)
        

        #横顔を検知
        faces = sideface_cascade.detectMultiScale(gray, 1.1, 3)

        #消す
        #global f_remove
        #f_remove = file_list.replace(path_test + "img/", '')
        f_name = os.path.splitext(os.path.basename(file_list))[0]
            
##          #ポジティブリストに入っているか
        l_in = [s for s in P_f if f_name in s]
        #画像切り取り
        global img1

        
        if len(l_in) != 0:
            #横顔と認識していないものを切り取る
##                if img.shape[0] < 400:
##                    global noise
##                    noise += 1
##                    write(path_dir + noise_dir)
            global P_P

            fa_p = 0
            fa_n = 0
            for (x, y, w, h) in faces:
                img1 = img[y:y + h,x: x + w]
                if w * h > 400 * 400:
                    
                    cv2.imwrite(path_dir + P_P_dir + f_name + str(fa_p) + "L" + ".jpg", img1)
                    fa_p += 1
                else:
                    cv2.imwrite(path_dir + P_P_dir + f_name + str(fa_n) + "l" +  ".jpg", img1)
                    fa_n += 1
                    

            if fa_p > 0 :
                P_P += 1
            else:
                global P_N
                P_N += 1
                     
                
                    

        else:
            l_in = [s for s in N_f if f_name in s]
            if len(l_in) != 0:
                global N_P
                fa_p2 = 0
                fa_n2 = 0
                for (x, y, w,h ) in faces:
                    img1 = img[y:y + h,x: x + w]
                    if w * h > 400 * 400:

                        cv2.imwrite(path_dir + N_P_dir + f_name + str(fa_p2) + "L" + ".jpg", img1)
                        fa_p2 += 1
                    else:
                        cv2.imwrite(path_dir + N_P_dir + f_name + str(fa_n2) + "l" + ".jpg", img1)
                        fa_n2 += 1
                        

                if fa_p2 > 0 :
                    N_P += 1
                else:
                    global N_N
                    N_N += 1
                
                    

            else:
                global Dis
                Dis += 1
                    
##
##            for rect in faces:
##                cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]),(0, 0, 255), thickness=2)


    
##    else:
##        print("o")
##        minmum_cascade = cv2.CascadeClassifier(path_2 + 'cascade/lbp/cascade.xml')
##        file_lists_p = glob.glob(path + "img_croppy/"+ P_P_dir +"/*.jpg")
##        for file_list_p in file_lists_p:
##            img_p = cv2.imread(file_list_p, cv2.IMREAD_COLOR)
##            grayp = cv2.cvtColor(img_p, cv2.COLOR_BGR2GRAY)
##            minmum = minmum_cascade.detectMultiScale(grayp, 1.1, 3)
##            f_remove = file_list_p.replace(path_dir + P_P_dir , '')
##            if len(minmum) > 0:
##                P_P -= 1
##                global noise
##                noise += 1
##                shutil.move(path_dir + P_P_dir + f_remove, path_dir + noise_dir + "/")

##else:
##    minmum_cascade = cv2.CascadeClassifier(path_min + 'cascade/lbp/cascade.xml')
##    file_list_n = glob.glob(path_min + "img_croppy/N_P/*.jpg")
##    file_list_p = glob.glob(path_min + "img_croppy/P_P/*.jpg")
##    for file_lists_n in file_list_n:
##
##        img_n = cv2.imread(file_lists_n, cv2.IMREAD_COLOR)
##        graym = cv2.cvtColor(img_n, cv2.COLOR_BGR2GRAY)
##        minmum = minmum_cascade.detectMultiScale(graym, 1.1, 3)
##        f_remove = file_lists_n.replace(path_min + 'img_croppy/N_P/', '')
##        if len(minmum) > 0:
##            N_P -= 1
##            noise += 1
##            shutil.move(path_min + "img_croppy/N_P/" + f_remove, path_min + "img_croppy/noise/")
##            #cv2.imwrite(path_min + "img_croppy/noise/" + f_remove , img)
##    else:
##        for file_lists_p in file_list_p:
##            img_p = cv2.imread(file_lists_p, cv2.IMREAD_COLOR)
##            grayp = cv2.cvtColor(img_p, cv2.COLOR_BGR2GRAY)
##            minmum = minmum_cascade.detectMultiScale(graym, 1.1, 3)
##            f_remove = file_lists_n.replace(path_min + 'img_croppy/P_P/', '')
##            minmum = minmum_cascade.detectMultiScale(graym, 1.1, 3)
##            if len(minmum) > 0:
##                P_P -= 1
##                noise += 1
##                shutil.move(path_min + "img_croppy/P_P/" + f_remove, path_min + "img_croppy/noise/")

if __name__ == "__main__":
    sideface_core1()
    
    print("All : {0} ".format(len(file_lists)))
    print("P_s : {0} ".format(P_s))
    print("N_s : {0} ".format(N_s))
    print("P_P : {0} ".format(P_P))
    print("P_N : {0}".format(P_N))
    print("N_N : {0}".format(N_N))
    print("N_P : {0}".format(N_P))
    #print("noise : {0}".format(noise))
    print("Dis: {0}".format(Dis))


# 画像表示
#cv2.imshow('img',img)
