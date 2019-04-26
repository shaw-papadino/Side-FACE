import glob
import os
import sys
import shutil
from selctingImage import selctingImage

def sorting_positive(path, fileList, pList):#, nList):

    for file in fileList:
        fileName = os.path.splitext(os.path.basename(file))[0]
        for p in pList:
            p = p.replace("img/", "").replace(".jpg", "")
            p = p.split(" ")
            # print("p{0}".format(p[0]))
            # print(fileName)
            if fileName == p[0]:
                if not os.path.exists(path + "positive_side/"):
                    os.makedirs(path + "positive_side/")
                shutil.copy(file, path + "positive_side/")
            else:
                if not os.path.exists(path + "negative_side/"):
                    os.makedirs(path + "negative_side/")
                shutil.copy(file, path + "negative_side/")

        # for n in nList:
        #
        #     n = n.replace("img/", "").replace(".jpg", "").replace("\n", "")
        #
        #     if fileName == n:
        #         shutil.copy(file, path + "negativeImageM/")


if __name__ == "__main__":

    path = "./201804280930/"
    fileList = sorted(glob.glob(path + "img/*.jpg"))
    pList = path + "positivemizumashi.dat"
    pOpen = open(pList, "r")
    pList = pOpen.readlines()
    # nList = path + "negative_2c.dat"
    # nOpen = open(nList, "r")
    # nList = nOpen.readlines()

    sortingPositive(path, fileList,  pList)#, nList)
    selctingImage(path)
