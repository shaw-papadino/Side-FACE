
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2

class WebcamVideoStream(WebcamVideoStream):

    def __init__(self, src, vidfps, camera_width, camera_height):
        super(WebcamVideoStream, self).__init__(src)
        self.stream.set(cv2.CAP_PROP_FPS, vidfps)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
