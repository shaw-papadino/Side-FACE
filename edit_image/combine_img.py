import shutil
import random
import glob

def combine_img(path):
    filepathP = path + "/P_Test"
    filepathN = path + "/N_Test"
    fileListP = sorted(glob.glob(filepathP + "/*.jpg"))
    fileListN = sorted(glob.glob(filepathN + "/*.jpg"))

    random.seed(r)

    for i in fileListP :
        if not os.path.exists(path + "/Testimg"):
                os.makedirs(path + "/Testimg")

        shutil.move(i, path + "/Testimg")

    for i in fileListN :

        shutil.move(i, path + "/Testimg")
