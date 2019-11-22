from copy_all_img import copy_all_img
from move_img import move_img
from combine_img import combine_img
from create_datfile import *
from add_positivedat import add_positivedat
from sorting_positive import sorting_imagefile

import subprocess
import sys
def selctingImage(path, datfile):

    for r in range(1):
        path = path + "/" + str(r) + "/"

        sorting_imagefile(path,  datfile)

        print("画像コピー")
        copy_all_img(path)

        print("半分ずつに分ける")
        move_img(path)
        print("テスト画像合体")
        combine_img(path, "Positive", "Negative", "TestImg")
        
        print("datfileを作成")
        create_datfile(path, positivedat, negativedat)

        # Image Augumentation した画像のデータをdatfileに追記
        # add_positivedat(path)

        print("トレーニング画像を合体")
        combine_img(path, "P_Train", "N_Train", "TrainImg")

        """
        print("識別器作成開始")
        command = ["./create_cascade.sh", path]
        subprocess.Popen(command)
        """

if __name__ == "__main__":

    args = sys.argv
    path = args[1]
    datfile = args[2]
    selctingImage(path, datfile)
