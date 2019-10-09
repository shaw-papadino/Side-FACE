import cv2 as cv
import numpy as np
import glob
import os
from add_positivedat import add_positivedat
import sys
def contImg(path):
    """
    Image Augmentation をする
    """

    # ルックアップテーブルの生成
    min_table = 20
    max_table = 205
    diff_table = max_table - min_table

    LUT_HC = np.arange(256, dtype = 'uint8' )
    LUT_LC = np.arange(256, dtype = 'uint8' )

    # ハイコントラストLUT作成
    for i in range(0, min_table):
        LUT_HC[i] = 0
    for i in range(min_table, max_table):
        LUT_HC[i] = 255 * (i - min_table) / diff_table
    for i in range(max_table, 255):
        LUT_HC[i] = 255

    # ローコントラストLUT作成
    for i in range(256):
        LUT_LC[i] = min_table + i * (diff_table) / 255

    imgList = sorted(glob.glob(path + "positiveImage/*.jpg"))
    for img in imgList:
        # print(img)
        j = os.path.splitext(os.path.basename(img))[0]

        # 変換
        src = cv.imread(img, 1)
        high_cont_img = cv.LUT(src, LUT_HC)
        low_cont_img = cv.LUT(src, LUT_LC)

        if not os.path.exists(path + "contp"):
            os.makedirs(path + "contp")
        cv.imwrite(path + "contp/" + j + "h.jpg",high_cont_img)
        cv.imwrite(path + "contp/" + j + "l.jpg",low_cont_img)

def gammaImg(path):

    # ガンマ変換ルックアップテーブル
    gs = [0.8,1.2,1.6]
    LUT_G1 = np.arange(256, dtype = 'uint8' )

    for g in gs:
        for i in range(256):
            LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / g)

        imgList = sorted(glob.glob(path + "contp/*.jpg"))
        for img in imgList:
            j = os.path.splitext(os.path.basename(img))[0]
            # 変換
            src = cv.imread(img, 1)
            gamma_img = cv.LUT(src, LUT_G1)

            if not os.path.exists(path + "gammap"):
                os.makedirs(path + "gammap")
            cv.imwrite(path + "gammap/" + j + str(g) +".jpg",gamma_img)

def blurImg(path):
    xs =  [1,3,5,7,9]

    for x in xs:
        average_square = (x,x)

        imgList = sorted(glob.glob(path + "gammap/*.jpg"))
        for img in imgList:
            j = os.path.splitext(os.path.basename(img))[0]
            src = cv.imread(img, 1)
            blur_img = cv.blur(src, average_square)

            if not os.path.exists(path + "blurp"):
                os.makedirs(path + "blurp")
            cv.imwrite(path + "blurp/" + j + str(x) + ".jpg",blur_img)

if __name__ == "__main__":
    args = sys.argv
    path = args[1]

    contImg(path)
    gammaImg(path)
    blurImg(path)
    # add_positivedat(path)
