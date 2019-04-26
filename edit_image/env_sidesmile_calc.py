import os


def text2lists(file):
    of = open(file, "r")
    filelineslist = of.readlines()
    return filelineslist



if __name__ == "__main__":
    file = "/Users/okayamashoya/NeoTrainingAssistant/static/negative_all.dat"
    path = os.path.dirname(file)
    list = text2lists(file)
    for l in list:
        l = l.split()
        file = l[0].replace("img/", "").replace("image_", "").replace(".jpg", "")


        file = int(file) + 1374
        if file >= 10000:
            file = str(file)
        else:
            file = "0" + str(file)

        with open(path + "/negative_all3.dat", mode='a') as f:
            f.write("img/image_" + str(file) + ".jpg\n")
            # f.write("img/image_" + str(file) + ".jpg " + l[1] + " " + l[2] + " " + l[3] + " " + l[4] + " " + l[5] + "\n")
