import glob
import os
import sys
import shutil
import datetime
def matching_side_front_img(path, fileList, pList, writeFileName):#, nList):
    f = open(path + writeFileName, mode='a')
    for imagefile in fileList:
        fileName = os.path.splitext(os.path.basename(imagefile))[0]
        fileName = int(fileName.replace("image_", ""))

        for p in pList:
            p = p.replace("img/", "").replace(".jpg", "")
            p = p.split(" ")
            p = int(p[0].replace("image_", ""))
            # p = round(((p - 51) / 8) * 9.38) + 26

            if fileName == p:
                f.write(imagefile + ", 0\n")
                break
                # shutil.copy(file,path)
            else:
                pass
            # shutil.copy(imagefile,"/Users/okayamashoya/Downloads/frontpic_negative")
        f.write(imagefile + ", 1\n")
    f.close()
        # for n in nList:
        #
        #     n = n.replace("img/", "").replace(".jpg", "").replace("\n", "")
        #
        #     if fileName == n:
        #         shutil.copy(file, path + "negativeImageM/")


if __name__ == "__main__":

    path = "./frontpictest/"
    dayName = str(datetime.datetime.now())
    fileName = dayName + ".txt"
    fileList = sorted(glob.glob(path + "img/*.jpg"))
    pList = path + "positive_front_ver1.dat"
    pOpen = open(pList, "r")
    pList = pOpen.readlines()
    # nList = path + "negative_2c.dat"
    # nOpen = open(nList, "r")
    # nList = nOpen.readlines()

    matching_side_front_img(path, fileList,  pList, fileName)#, nList)
