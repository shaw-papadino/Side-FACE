import glob
import os
import sys
import shutil

def sorting_imagefile(path, datfile):

    fileList = sorted(glob.glob(path + "/*.jpg"))

    pList = datfile + "/positive.dat"
    pOpen = open(pList, "r")
    pList = pOpen.readlines()
    nList = datfile + "/negative.dat"
    nOpen = open(nList, "r")
    nList = nOpen.readlines()

    print(fileList)
    for file in fileList:
        fileName = os.path.splitext(os.path.basename(file))[0]
        for pimg in pList:
            p = pimg.replace("img/", "").replace(".jpg", "")
            p = p.split(" ")

            if fileName == p[0]:
                if not os.path.exists("../data/positiveImage/"):
                    os.makedirs("../data/positiveImage/")
                shutil.copy(file, "../data/positiveImage/")

        for nimg in nList:
            n = nimg.replace("img/", "").replace(".jpg", "").replace("\n", "")
            if fileName == n:
                if not os.path.exists("../data/negativeImage/"):
                    os.makedirs("../data/negativeImage/")
                shutil.copy(file, "../data/negativeImage/")

if __name__ == "__main__":

    args = sys.argv
    path = args[1]
    datfile = args[2]
    print(path)

    sorting_imagefile(path, datfile)
