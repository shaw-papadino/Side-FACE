import shutil
import random
import glob
import datetime
import os

def move_img(path):
    """
    ランダムに画像を分ける
    """
    filepathP = path + "Positive"
    filepathN = path + "Negative"
    fileListP = sorted(glob.glob(filepathP + "/*.jpg"))
    fileListN = sorted(glob.glob(filepathN + "/*.jpg"))

    now = datetime.datetime.now()
    time_seed = now.timestamp()
    random.seed(time_seed)

    fileListRandomP = random.sample(fileListP, round(len(fileListP) * 0.5))
    fileListRandomN = random.sample(fileListN, round(len(fileListN) * 0.5))

    if not os.path.exists(path + "P_Train/"):
        os.makedirs(path + "P_Train/")
    if not os.path.exists(path + "N_Train/"):
        os.makedirs(path + "N_Train/")

    for (p,n) in zip(fileListRandomP, fileListRandomN):

        shutil.move(p, path + "P_Train/")
        shutil.move(n, path + "N_Train/")
