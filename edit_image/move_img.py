import shutil
import random
import glob

def move_img(path):
    filepathP = path + "/P_Test"
    filepathN = path + "/N_Test"
    fileListP = sorted(glob.glob(filepathP + "/*.jpg"))
    fileListN = sorted(glob.glob(filepathN + "/*.jpg"))

    fileListRandomP = random.sample(fileListP, round(len(fileListP) * 0.5))
    fileListRandomN = random.sample(fileListN, round(len(fileListN) * 0.5))

    for i in fileListRandomP:

        shutil.move(i, path + "/P_Train")

    for i in fileListRandomN:

        shutil.move(i, path + "/N_Train")
