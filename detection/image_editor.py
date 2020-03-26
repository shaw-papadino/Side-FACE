import cv2

class ImageEditor():
    def __init__(self):
        self.color = (255, 128, 0)
        self.thickness = 1

    def get_gray_image(self, img):
        grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return grayimg

    def get_areas(self,object_areas):
        for (x, y, w, h) in object_areas:
            return x, y, w, h

    def get_crop_image(self, img, object_areas):
        if isinstance(object_areas, tuple):
            return False
        x, y, w, h = self.get_areas(object_areas)
        return img[y : y + h, x : x + w]

    def overlay_on_crop_image(self, img, object_areas):

        img_cp = img.copy()

        x, y, w, h = get_areas(object_areas)
        box_top = y
        box_left = x
        box_right = x + w
        box_bottom = y + h

        cv2.rectangle(
                img_cp, 
                (box_left, box_top), 
                (box_right, box_bottom), 
                self.color, self.thickness
                )

        return img_cp
