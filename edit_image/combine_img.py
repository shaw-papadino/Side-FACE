import shutil
import random
import glob
import datetime
import os

def combine_img(path, org_dir_name_1, org_dir_name_2, new_dir_name):
    """
    複数ディレクトリ内の画像を一つのディレクトリに移動する
    """
    filepathP = path + org_dir_name_1
    filepathN = path + org_dir_name_2
    fileListP = sorted(glob.glob(filepathP + "/*.jpg"))
    fileListN = sorted(glob.glob(filepathN + "/*.jpg"))

    now = datetime.datetime.now()
    time_seed = now.timestamp()
    random.seed(time_seed)

    for (p,n) in zip(fileListP, fileListN) :
        if not os.path.exists(path + new_dir_name):
                os.makedirs(path + new_dir_name)

        shutil.move(p, path + new_dir_name)
        shutil.move(n, path + new_dir_name)

