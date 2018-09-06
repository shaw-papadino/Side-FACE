import shutil

def copy_all_img(path):
    filepathP = path + "/positiveImage"
    filepathN = path + "/negativeImage"
    shutil.copytree(filepathP , path + "05_" + str(r) + "/P_Test")
    shutil.copytree(filepathN , path + "05_" + str(r) + "/N_Test")
