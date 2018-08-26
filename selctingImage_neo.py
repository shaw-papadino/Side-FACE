import random
import shutil
import glob
import os
import pandas as pd

path = "./20180824113711/"
# fileListP = sorted(glob.glob("./a/positiveImage/*.jpg"))
# fileListN = sorted(glob.glob("./a/negativeImage/*.jpg"))

pList = path + "positive.dat"
pOpen = open(pList, "r")
pList = pOpen.readlines()
nList = path + "negative.dat"
nOpen = open(nList, "r")
nList = nOpen.readlines()
x = []
y = []
"""
imgList = sorted(glob.glob(path + "img/*.jpg"))

for i in imgList:
    ii = os.path.splitext(os.path.basename(i))[0]
    for p in pList:
        p = os.path.splitext(os.path.basename(p))[0]

        if ii == p:
            shutil.copy(i, path + "bigsmile")
        else:
            shutil.copy(i, path + "notsmile")
"""

for n in nList:

    n = n.split()[0]
    x.append(n)
    y.append("0")


df = pd.DataFrame({
        'x:img' : x,
        'y:label' : y
        })

df.to_csv(path + 'smile.csv', mode='a', header=False)
