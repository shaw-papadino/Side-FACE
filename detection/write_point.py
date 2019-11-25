

def write_point(image_name, points):
    datfile = "positive.dat"
    with open(datfile, mode="a") as f:
        f.write("img/" + image_name + ".jpg 1 " + str(points[0]) + " " + str(points[1]) + " " + str(points[2]) + " " + str(points[3]) + "\n")
