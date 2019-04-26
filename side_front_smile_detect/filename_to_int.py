

def filename_to_int(filename):
    f = filename.replace("img/", "").replace(".jpg", "")
    f = f.split(" ")
    f = int(f[0].replace("image_", ""))

    return f

if __name__ == "__main__":
    print("check me!")
