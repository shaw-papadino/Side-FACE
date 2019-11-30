import glob
import os
import re

path = "./201804280930"


def create_positivedat(path, datfile):
    """
    交差検証用のポジティブリスト作成
    """
    pList = path + datfile
    pList = open(pList, "r")
    pList = pList.readlines()

    imgList = sorted(glob.glob(path + "P_Train/*.jpg"))

    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]

        for p in pList:
            psp = p.split()
            pp = psp[0].replace("img/", "")
            print(isp)
            # print(pp)

            # patternp = ".*?(\d*?_\d*?[hl]?[\d.\d*]*).jpg?"
            patternp = ".*?(\d*?_\d*?).jpg?"
            # pattern = ".*?(\d+_\d+[hl]*?[\d.\d*]*)"
            # ire = re.search(pattern, isp)
            pre = re.search(patternp, pp)

            # print("ire{0}".format(ire[1]))
            if isp == pre.group():
                with open(path + "/positive.dat", mode="a") as f:
                    f.write(p)
            else:
                pass


def create_negativedat(path, datfile):
    """
    交差検証用のネガティブリスト作成
    """

    nList = path + datfile
    nList = open(nList, "r")
    nList = nList.readlines()

    imgList = sorted(glob.glob(path + "N_Train/*.jpg"))

    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]
        for n in nList:
            nn = n.replace("img/", "").replace(".jpg", "").replace("\n", "")

            if isp == nn:
                with open(path + "/negative.dat", mode="a") as f:
                    f.write(n + "\n")
                break
            else:
                pass


def create_datfile(path, positivedat, negativedat):

    print("--- writing positivedat ---")
    create_positivedat(path, positivedat)
    print("--- finish writing ---")

    print("--- writing negativedat ---")
    create_negativedat(path, negativedat)
    print("--- finish writing ---")


if __name__ == "__main__":

    path = "./201804280930/"

    for r in range(2, 10):
        # create_positivedat(path, r)
        create_negativedat(path, r)
