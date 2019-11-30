import random
import shutil
import glob
import os
import re
import sys

# ROOT_PATH = "./201804280930/"
def add_positivedat(path, datfile):
    """
    Image Augmentationで追加された画像(元のファイル名に記号追加したファイル名)を
    ポジティブリストに追加する
    """

    # ポジティブリスト読み込み
    pList = path + datfile + "positive.dat"
    pOpen = open(pList, "r")
    pListLines = pOpen.readlines()

    # 画像読み込み
    imgList = sorted(glob.glob(path + "positiveImage20191007/*.jpg"))

    for i in imgList:
        # 画像ファイル名取得
        isp = os.path.splitext(os.path.basename(i))[0]

        for p in pListLines:
            # ポジティブリストに記載されている画像ファイル名取得
            p = p.split()
            pp = p[0].replace("img/", "")

            # print(pp)
            pattern = ".*?(\d*?)_(\d*?)[hl].*"
            patternp = ".*?(\d*?)_(\d*?).jpg?"

            ire = re.search(pattern, isp)
            pre = re.search(patternp, pp)

            if ire is None:
                continue
            # print("ire:{}".format(ire.groups()))
            # print(pre.groups())
            if ire.groups()[1] == pre.groups()[1]:
                # ポジティブリストに追加
                with open(pList, mode="a") as f:
                    f.write(
                        "img/"
                        + isp
                        + ".jpg "
                        + p[1]
                        + " "
                        + p[2]
                        + " "
                        + p[3]
                        + " "
                        + p[4]
                        + " "
                        + p[5]
                        + "\n"
                    )
                break

            else:
                pass


if __name__ == "__main__":
    args = sys.argv
    path = args[1]
    datfile = args[2]
    add_positivedat(path, datfile)
