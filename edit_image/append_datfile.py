import sys
import glob
import os
import re

def append_datfile(path, datfile):

    pList = path + datfile + "positive.dat"
    pList = open(pList, "r")
    pList = pList.readlines()

    imgList = sorted(glob.glob(path + "20191007_trimed/*.jpg"))

    flg = False
    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]
        
        if isp == "image_03680":
            flg = True
        

        if flg == False :
            continue
        else :
            pass

        file_flg = False
        for p in pList:
            psp = p.split()
            pp = psp[0].replace("img/", "")
            positive_name = psp[0].replace("img/", "").replace(".jpg", "")
            # print(isp)
            # print(positive_name)

            # patternp = ".*?(\d*?_\d*?[hl]?[\d.\d*]*).jpg?"
            # pattern = ".*?(\d+_\d+[hl]*?[\d.\d*]*)"
            # ire = re.search(pattern, isp)
            # pre = re.search(patternp, pp)

            
            if isp == positive_name:
                file_flg = True
                break
        if file_flg :
            pass
        else :
            # print("img/" + isp + ".jpg")
            with open(path + datfile + "negative.dat", mode='a') as f:
                f.write("img/" + isp + ".jpg\n")

if __name__=="__main__":
    args = sys.argv
    path = args[1]
    datfile = args[2]
    append_datfile(path, datfile)
