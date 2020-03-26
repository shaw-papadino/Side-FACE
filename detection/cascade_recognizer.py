import cv2
from recognizer import Recognizer

class CascadeRecognizer(Recognizer):
    def __init__(self,cascade, scale=1.1,minN=3,minS=250,maxS=350):
        self.cascade = cv2.CascadeClassifier(cascade)
        self.scaleFactor = scale
        self.minNeighbors = minN
        self.minSize = (minS,minS)
        self.maxSize = (maxS,maxS)
        self.count = 0
        self.areas = []

    def recognize(self,grayimg):
        ans = self.cascade.detectMultiScale(
            grayimg,
            scaleFactor=self.scaleFactor,
            minNeighbors=self.minNeighbors,
            minSize=self.minSize,
            maxSize=self.maxSize,
        )
        if len(ans):
            return ans
        else:
            return []

    def areas_buffer(self,areas):
        self.count = 0
        self.areas = areas

    def get_areas(self):
        if self.count > 6:
            self.areas = []
            return []
        self.count += 1
        return self.areas
