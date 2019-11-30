# You should replace these 3 lines with the output in calibration step
import cv2
import numpy as np

DIM = (1000, 750)
k = np.zeros((3, 3))
d = np.zeros((1, 5))


def undistort(img_path, K, D):
    print(D)
    print(D.size)
    print(D.shape)
    print(d.size)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(k, d, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(
        img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT
    )
    # cv2.imshow("undistorted", undistorted_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return undistored_img


if __name__ == "__main__":
    for p in sys.argv[1:]:
        undistort(p)
