# -*- coding: utf-8 -*-

import random
import shutil
import glob
import os

def copy_file(img_path, to_copy_path, ToF):
    """正解 or 不正解画像ファイルを任意のディレクトリにコピーする関数"""
    img_list = [ s.replace("\n" , "") for s in [ s.replace("img" , img_path + "img") for s in list(map(lambda x: x.split()[0], open(img_path + ToF, 'r').readlines()))]]
    for img in img_list:
        if not os.path.exists(img):
            pass
        else:
            shutil.copy(img,  to_copy_path)

def copy_random_file(img_path, to_copy_path,　ToF, random_number):
    """正解 or 不正解画像ファイルを任意のディレクトリにランダムでコピーする関数"""
    img_list = [ s.replace("\n" , "") for s in [ s.replace("img" , img_path + "img") for s in open(img_path + ToF, "r").readlines()]]
    random.seed(0)
    imgR_list = random.sample(N_list, k = random_number)

    for img in imgR_list:
        if not os.path.exists(img):
            pass
        else:
            shutil.copy(img,  to_copy_path)
"""
copy_file()
copy_random_file()
"""
