from copy_all_img import copy_all_img
from move_img import move_img
from combine_img import combine_img



def selctingImage(path):

    for r in range(1,11):
        path = path + r + "/"
        copy_all_img(path)
        move_img(path)
        combineTestImg(path)


if __name__ == "__main__":

    path = "./201804280930/"
    selctingImage(path)
