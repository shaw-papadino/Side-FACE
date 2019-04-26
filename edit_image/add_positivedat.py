import random
import shutil
import glob
import os
import re

def add_positivedat(path, file):

    filelist = text2lists(path + file)
    # pList = path + "positive_front_ver2.dat"
    # pOpen = open(pList, "r")
    # pListLines = pOpen.readlines()

    imgList = sorted(glob.glob(path + "contp/*.jpg")) + sorted(glob.glob(path + "gammap/*.jpg")) + sorted(glob.glob(path + "blurp/*.jpg"))

    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]



        for p in filelist:
            p = p.split()
            pp = p[0].replace("img/", "")

            pattern = ".*(\w*_\d*)[lh].*"
            # pattern = ".*?(\d*?_\d*?)[hl].*"
            patternp = ".*(\w*_\d*)\.jpg"
            # patternp = ".*?(\d*?_\d*?).jpg?"

            ire = re.search(pattern, isp)
            pre = re.search(patternp, pp)

            # print(ire.group(1))
            # print(pre.group(1))
            if ire.group(1) == pre.group(1):
                print("un")
                with open(pList, mode='a') as f:
                    f.write("img/" + isp + ".jpg " + p[1] + " " + p[2] + " " + p[3] + " " + p[4] + " " + p[5] + '\n')
            else:
                pass

if __name__ == "__main__":
    path = "../20190113/"
    file = "positive_front_ver2.dat"
    add_positivedat(path, file)
