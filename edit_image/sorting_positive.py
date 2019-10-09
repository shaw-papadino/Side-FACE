import glob
import os
import sys
import shutil

def sorting_imagefile(path, datfile):

    fileList = sorted(glob.glob(path + "20191007_trimed/*.jpg"))

    pList = path + datfile + "positive.dat"
    pOpen = open(pList, "r")
    pList = pOpen.readlines()
    nList = path + datfile + "negative.dat"
    nOpen = open(nList, "r")
    nList = nOpen.readlines()

    for file in fileList:
        fileName = os.path.splitext(os.path.basename(file))[0]
        for p in pList:
            p = p.replace("img/", "").replace(".jpg", "")
            p = p.split(" ")

            if fileName == p[0]:
                if not os.path.exists(path + "positiveImage/"):
                    os.makedirs(path + "positiveImage/")
                shutil.copy(file, path + "positiveImage/")

        for n in nList:
            n = n.replace("img/", "").replace(".jpg", "").replace("\n", "")
            if fileName == n:
                if not os.path.exists(path + "negativeImage/"):
                    os.makedirs(path + "negativeImage/")
                shutil.copy(file, path + "negativeImage/")

if __name__ == "__main__":

    args = sys.argv
    path = args[1]
    datfile = args[2]
    

    sorting_imagefile(path, datfile)
