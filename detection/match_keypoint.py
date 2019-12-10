import cv2
import numpy as np
import argparse

def norm_matchpoint(prevkp, nextkp, matchpoint):
    """
    matchpointを正規化
    """
    # print("matchpoint:{}, prevkp:{}, kp:{}".format(matchpoint, prevkp, nextkp))
    norm_result = (2 * matchpoint) / (prevkp + nextkp)
    return norm_result

def detect_keypoint(image):
    """
    akazeアルゴリズムを用いてkeypoints, descriptors を返す
    keypoint: corners, edges in image
    descriptor: a feature vector containing the keypoints’ essential characteristics
    """

    akaze = cv2.AKAZE_create()
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kp, des = akaze.detectAndCompute(grayimg, None)

    return kp, des


def match_keypoint(prevkp, nextkp, prevdes, nextdes):
    """
    knnアルゴリズムを用いて2つの画像の対応座標を返す
    """

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(prevdes, nextdes, k=2)

    ratio = 0.5
    matching_list = []
    distance_list = []
    previmg_points = []
    nextimg_points = []
    if matches:
        if len(matches[0]) > 1:
            for m, n in matches:

                distance_list.append(m.distance)

                if m.distance < ratio * n.distance:
                    matching_list.append([m])
                    previmg_points.append(list(map(int, prevkp[m.queryIdx].pt)))
                    # nextimg_points.append(list(map(int, nextkp[m.trainIdx].pt)))
        else:
            pass
    else:
        pass

    return previmg_points, nextimg_points, matching_list  # マッチした座標のリスト, draw用にmatching_list


def draw_match_keypoint(previmg, nextimg, prevkp, nextkp, matching_list):
    """
    matchしたkeypointと距離を重畳したimageを返す
    """

    if matching_list != []:
        drawimage = cv2.drawMatchesKnn(
            previmg, prevkp, nextimg, nextkp, matching_list, None, flags=4
        )
    else:
        return nextimg

    return drawimage


def main(path1, path2):

    prev_image = cv2.imread(path1)
    prev_keypoint, prev_distance = detect_keypoint(prev_image)

    next_image = cv2.imread(path2)
    next_keypoint, next_distance = detect_keypoint(next_image)

    previmg_points, nextimg_points, matching_list = match_keypoint(
        prev_keypoint, next_keypoint, prev_distance, next_distance
    )

    drawimage = draw_match_keypoint(
        prev_image, next_image, prev_keypoint, next_keypoint, matching_list
    )

    cv2.imshow("match image", drawimage)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--path1", "-p1", default="", help="Path of the detection image.")
    parser.add_argument("--path2", "-p2", default="", help="Path of the detection image.")

    args = parser.parse_args()

    main(args.path1, args.path2)
