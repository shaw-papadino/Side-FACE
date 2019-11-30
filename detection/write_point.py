def write_point(image_name, points):
    datfile = "positive.dat"
    shift = 50
    if points[0] < 50:
        x = 0
    else:
        x = points[0] - shift

    if points[1] < 50:
        y = 0
    else:
        y = points[1] - shift

    width = points[2] + shift
    height = points[3] + shift

    with open(datfile, mode="a") as f:
        f.write(
            "img/"
            + image_name
            + ".jpg 1 "
            + str(x)
            + " "
            + str(y)
            + " "
            + str(width)
            + " "
            + str(height)
            + "\n"
        )
