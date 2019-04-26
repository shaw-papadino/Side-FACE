import glob
import os
import argparse

def create_negativedat(path, out_filename):

    imgList = sorted(glob.glob(path + /*.jpg"))

    for i in imgList:
        isp = os.path.splitext(os.path.basename(i))[0]
        # print(isp)

        with open("./" + out_filename + ".dat", mode='a') as f:
            f.write("img/" + isp + ".jpg " + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train sidesmile estimation')

    parser.add_argument('--inputdir', '-i', type=str,
                        help='input dir')
    parser.add_argument('--outputname', '-o', type=str, default="negative",
                        help='output filename')
    parser.add_argument('--max_epoch', '-e', type=int, default=50,
                        help='Number of epoch to train')
    parser.add_argument('--cross_validation', '-c', type=int, default=1,
                        help='Number of cross_validation to train')
    args = parser.parse_args()

    args = parse_args()

    path = args.inputdir
    out_filename = args.outputname
    create_negativedat(path, out_filename)
