import glob
import os
import re

path = "./201804280930"



def create_positivedat(path, r):
    pList = path + "positivemizumashi.dat"
    pList = open(pList, "r")
    pList = pList.readlines()

    imgList = sorted(glob.glob(path + "M05_" + str(r) + "/P_Train/*.jpg"))

    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]

        for p in pList:
            psp = p.split()
            pp = psp[0].replace("img/", "")
            print(isp)
            # print(pp)

            patternp = ".*?(\d*?_\d*?[hl]?[\d.\d*]*).jpg?"
            # pattern = ".*?(\d+_\d+[hl]*?[\d.\d*]*)"
            # ire = re.search(pattern, isp)
            pre = re.search(patternp, pp)

            # print("ire{0}".format(ire[1]))
            print(pre[1])
            if isp == pre[1]:
                print("un")
                with open(path + "M05_" + str(r) + "/positive.dat", mode='a') as f:
                    f.write(p)
            else:
                pass

def create_negativedat(path, r):
    nList = path + "negative_2c.dat"
    nList = open(nList, "r")
    nList = nList.readlines()

    imgList = sorted(glob.glob(path + "M05_" + str(r) + "/N_Train/*.jpg"))

    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]
        for n in nList:
            nn = n.replace("img/", "").replace(".jpg", "").replace("\n", "")

            print(nn)
            print(isp)
            if isp == nn:
                print("un")
                with open(path + "M05_" + str(r) + "/negative.dat", mode='a') as f:
                    f.write(n + '\n')
                break
            else:
                pass

if __name__ == "__main__":

    path = "./201804280930/"

    for r in range(2,10):
        # create_positivedat(path, r)
        create_negativedat(path, r)
