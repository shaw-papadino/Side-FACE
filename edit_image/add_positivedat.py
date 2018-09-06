import random
import shutil
import glob
import os
import re
path = "./20180825/"

def add_positivedat(path):

    pList = path + "positive.dat"
    pOpen = open(pList, "r")
    pListLines = pOpen.readlines()

    imgList = sorted(glob.glob(path + "img/*.jpg"))

    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]


        for p in pListLines:
            p = p.split()
            pp = p[0].replace("img/", "")

            pattern = ".*?(\d*?_\d*?)[hl].*"
            patternp = ".*?(\d*?_\d*?).jpg?"

            ire = re.search(pattern, isp)
            pre = re.search(patternp, pp)

            if ire[1] == pre[1]:
                print("un")
                with open(pList, mode='a') as f:
                    f.write("img/" + isp + ".jpg " + p[1] + " " + p[2] + " " + p[3] + " " + p[4] + " " + p[5] +  '\n')
            else:
                pass

if __name__ == "__main__":

    add_positivedat(path)
