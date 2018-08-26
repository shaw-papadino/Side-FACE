import random
import shutil
import glob
import os


def copyAllImg(path, r):
    filepathP = path + "/positiveImage"
    filepathN = path + "/negativeImage"
    shutil.copytree(filepathP , path + "05_" + str(r) + "/P_Test")
    shutil.copytree(filepathN , path + "05_" + str(r) + "/N_Test")

def moveTrainImg(path, r):
    filepathP = path + "05_" + str(r) + "/P_Test"
    filepathN = path + "05_" + str(r) + "/N_Test"
    fileListP = sorted(glob.glob(filepathP + "/*.jpg"))
    fileListN = sorted(glob.glob(filepathN + "/*.jpg"))

    fileListRandomP = random.sample(fileListP, round(len(fileListP) * 0.5))
    fileListRandomN = random.sample(fileListN, round(len(fileListN) * 0.5))

    for i in fileListRandomP:

        os.move(i, path + "05_" + str(r) + "/P_Train")

    for i in fileListRandomN:

        os.move(i, path + "05_" + str(r) + "/N_Train")

def joinTestImg(path, r):
    filepathP = path + "05_" + str(r) + "/P_Test"
    filepathN = path + "05_" + str(r) + "/N_Test"
    fileListP = sorted(glob.glob(filepathP + "/*.jpg"))
    fileListN = sorted(glob.glob(filepathN + "/*.jpg"))

    random.seed(r)

    for i in fileListP :
        if not os.path.exists(path + "05_" + str(r) + "/Testimg"):
                os.makedirs(path + "05_" + str(r) + "/Testimg")

        shutil.move(i, path + "05_" + str(r) + "/Testimg")

    for i in fileListN :

        shutil.move(i, path + "05_" + str(r) + "/Testimg")

def selctingImage(path):

    for r in range(1,10):
        copyAllImg(path, r)
        moveTrainImg(path, r)
        joinTestImg(path, r)


if __name__ == "__main__":

    path = "./201804280930/"
    selctingImage(path)
