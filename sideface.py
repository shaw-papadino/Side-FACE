# -*- coding: utf-8 -*-

import cv2
import glob
import collections
import os
import shutil
import threading
import logging
import time

global_lock = threading.Lock()
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

path = "/Users/okayamashoya/NeoTrainingAssistant/static/img_dst/"
#テストデータ "20180424113542/", 学習データ "201804280930/"
path_test = path + "20180424113542/"

#1層目の検出器
path_1 = path + "201804280930/"
#2層目の検出器
path_2 = path + "201805071842/"
#カスケード
cascade_path = 'cascade/lbp/cascade.xml'
#画像入れ込み
path_dir = path + "img_croppy/"
#パラメータ
#実際_認識
P_P = 0
P_N = 0
N_N = 0
N_P = 0
Dis_P = 0
Dis_N = 0
noise = 0

#検出器読み込み
sideface_cascade = cv2.CascadeClassifier(path_1 + cascade_path)
second_cascade = cv2.CascadeClassifier(path_2 + cascade_path)

#Positive数読み込み
P_s= sum(1 for line in open(path_test + 'positive.dat'))
#Negative数読み込み
N_s = sum(1 for line in open(path_test + 'negative.dat'))
#全画像読み込み
file_lists = glob.glob(path_test + "img/*.jpg")

#Positiveリスト読み込み
P_file = open(path_test + 'positive.dat', 'r')
#Negativeリスト読み込み
N_file = open(path_test + 'negative.dat', "r")

#1行ずつリストにする
P_f = P_file.readlines()
N_f = N_file.readlines()

noise_dir = "noise"
P_P_dir = "P_P"
P_N_dir = "P_N"
N_P_dir = "N_P"
def remove(filepath):
    files = os.listdir(filepath)
    if len(files) > 0 :
        os.remove(filepath + "/*.jpg")
        
def write(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    cv2.imwrite(filepath + f_remove , img)

def sideface_core1():
    global global_lock
    logging.debug('Starting')
    for file_list in file_lists:
        global img
        img = cv2.imread(file_list, cv2.IMREAD_COLOR)
        # グレースケール変換
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #横顔を検知
        faces = sideface_cascade.detectMultiScale(gray, 1.1, 3)

        #消す
        global f_remove
        f_remove = file_list.replace(path_test + 'img', '')

        global_lock.acquire()
        if len(faces) > 0:
            #ポジティブリストに入っているか
            l_in = [s for s in P_f if f_remove in s]
            #画像切り取り
            img = img[faces[0][1]:faces[0][1]+faces[0][3], faces[0][0]:faces[0][0]+faces[0][2]]

            
            if len(l_in) != 0:
                #横顔と認識していないものを切り取る
                if img.shape[0] < 400:
                    global noise
                    noise += 1
                    write(path_dir + noise_dir)
                    global_lock.release()

                else:
                    global P_P
                    P_P += 1
                    write(path_dir + P_P_dir)
                    global_lock.release()

            else:
                l_in = [s for s in N_f if f_remove in s]
                if len(l_in) != 0:
                    # グレースケール変換
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    #笑っていない横顔を検出
                    second = second_cascade.detectMultiScale(gray, 1.1, 3)

                    #横顔と認識していないものを切り取る
                    if img.shape[0] < 400:
                        noise += 1
                        write(path_dir + noise_dir)
                        global_lock.release()

                    elif len(second) > 0:
                        global N_N
                        N_N += 1
                        global_lock.release()
                    else:
                        global N_P
                        N_P += 1
                        write(path_dir + N_P_dir)
                        global_lock.release()

                else:
                    global Dis_P
                    Dis_P += 1
                    global_lock.release()

            for rect in faces:
                cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]),(0, 0, 255), thickness=2)


        else:
            l_in = [s for s in N_f if f_remove in s]
            if len(l_in) != 0:
                N_N += 1
                global_lock.release()
            else:
                l_in = [s for s in P_f if f_remove in s]
                if len(l_in) != 0:
                    global P_N
                    P_N += 1
                    write(path_dir + P_N_dir)
                    global_lock.release()

                else:
                    global Dis_N
                    Dis_N += 1
                    global_lock.release()

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
    thread_1 = threading.Thread(target=sideface_core1)
    

    thread_1.start()
    
    thread_1.join()
    
    print("All : {0} ".format(len(file_lists)))
    print("P_s : {0} ".format(P_s))
    print("N_s : {0} ".format(N_s))
    print("P_P : {0} ".format(P_P))
    print("P_N : {0}".format(P_N))
    print("N_N : {0}".format(N_N))
    print("N_P : {0}".format(N_P))
    print("noise : {0}".format(noise))
    print("Dis_P : {0}".format(Dis_P))
    print("Dis_N : {0}".format(Dis_N))


# 画像表示
#cv2.imshow('img',img)
