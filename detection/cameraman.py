"""
撮影・現像をするクラス
"""
import cv2

class CameraMan():
    def __init__(self, cam_W, cam_H, usbcam=0, vidfps=30):
        self.cam = cv2.VideoCapture(usbcam)
        self.cam.set(cv2.CAP_PROP_FPS, vidfps)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, cam_W)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_H)

    def capture(self):
        ret, img = self.cam.read()
        return ret, img
    
    # def get_image(self):
    #     return self.img
