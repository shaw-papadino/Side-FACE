import cv2
from recognizer import Recognizer


class FeatureRecognizer(Recognizer):
    def __init__(self,mode="AKAZE"):
        self.mode = mode
        self.kp = 0
        self.des = 0

    
    def norm_matchpoint(self,currkp, matchpoint):
        """
        matchpointを正規化
        """
        norm_result = (2 * len(matchpoint)) / (len(self.kp) + len(currkp))
        return norm_result

    def detect_keypoint(self,grayimg):
        """
        keypoint: corners, edges in image
        descriptor: a feature vector containing the keypoints’ essential characteristics
        """

        akaze = cv2.AKAZE_create()
        kp, des = akaze.detectAndCompute(grayimg, None)

        return kp, des

    def match_keypoint(self, args):
        """
        knnアルゴリズムを用いて2つの画像の対応座標を返す
        """
        (currkp, currdes) = args
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(self.des, currdes, k=2)

        ratio = 0.5
        matching_list = []
        previmg_points = []
        currimg_points = []
        if matches:
            if len(matches[0]) > 1:
                for m, n in matches:
                    if m.distance < ratio * n.distance:
                        matching_list.append([m])
                        previmg_points.append(list(map(int, self.kp[m.queryIdx].pt)))
                        # currimg_points.append(list(map(int, currkp[m.trainIdx].pt)))

        return previmg_points, matching_list

    def recognize(self, *args):
        if self.mode == "AKAZE" and len(args) == 2:
            return self.match_keypoint(args)
        else:
            return [],[]

    def feature_buffer(self, kp, des):
        self.kp = kp
        self.des = des
        # self.count = 0

    # def get_feature():
    #     if self.count > 6:
    #         self.feature = []
    #         return False
    #     self.count += 1
    #     return self.kp, self.des
