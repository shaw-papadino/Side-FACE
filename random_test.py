import random
import glob
import shutil
import os


path = "/Users/okayamashoya/NeoTrainingAssistant/static/img_dst/"
mv_img = path + "3800/img/"
file_lists = glob.glob(path + "3800/test/" + "*.jpg")
random.seed(0)
file_r = random.sample(file_lists, k=500)

for i in file_r:
    if not os.path.exists(i):
        pass
    else:
        shutil.move(i,  mv_img)
