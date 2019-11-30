import glob
import os
import sys
import shutil

from filename_to_int import filename_to_int


def compare_side_front(frontfileList, fList, sidefileList, sList):

    for f in fList:
        print(f)
        """
        fint = filename_to_int(f)
        fint = fint + 3

        for s in sList:
            sint = filename_to_int(s)

            if f == s:

                shutil.copy(f,"/Users/okayamashoya/Downloads/20190202_compare/TP")
            else:
                shutil.copy(f,"/Users/okayamashoya/Downloads/20190202_compare/TN")
    for s in sList:
        sint = filename_to_int(s)


        for f in fList:
            fint = filename_to_int(f)
            fint = fint + 3

            if f == s:
                pass
            else:
                shutil.copy(f,"/Users/okayamashoya/Downloads/20190202_compare/FP")
    """


if __name__ == "__main__":
    path = "./frontpic_ver2/"
    frontfileList = sorted(glob.glob(path + "*.jpg"))
    fList = "/Users/okayamashoya/NeoTrainingAssistant/static/img_dst/20190112224732/positive_front_ver2.dat"
    fOpen = open(fList, "r")
    fList = fOpen.readlines()
    path = "./sidepic_ver2/"
    sidefileList = sorted(glob.glob(path + "*.jpg"))
    sList = "/Users/okayamashoya/NeoTrainingAssistant/static/img_dst/20190202160142/positive_side_ver1.dat"
    sOpen = open(sList, "r")
    sList = sOpen.readlines()

    compare_side_front(frontfileList, fList, sidefileList, sList)
