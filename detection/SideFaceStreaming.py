import argparse
import time
import traceback
from imutils.video import FPS


from streaming import Streaming
from cameraman import CameraMan
from image_store import ImageStore
from image_editor import ImageEditor
from feature_recognizer import FeatureRecognizer
from cascade_recognizer import CascadeRecognizer
from csv_store import CsvStore

class SideFaceStreaming(Streaming):
    def __init__(self, path, w, h, mode="Image", cascade=""):
        self.CAM = CameraMan(w, h)
        self.IE = ImageEditor()
        self.mode = mode
        if not mode == "norecord":
            self.IS = ImageStore(path,mode)
        if mode == "Movie":
            self.IS.movie_settings(w,h)
        self.CS = CsvStore(path)
        self.fps = FPS()
        self.cascade_path = cascade
    def stream(self):

        AKA = FeatureRecognizer("AKAZE")
        CAS = CascadeRecognizer(self.cascade_path)

        store_list = []
        starttime = time.perf_counter()
        self.fps.start()
        while True:
            ret, img = self.CAM.capture()
            if not ret:
                continue
            store_list.append(time.perf_counter()-starttime)
            grayimg = self.IE.get_gray_image(img)
            areas = CAS.recognize(grayimg)
            if len(areas):
                CAS.areas_buffer(areas)
            else:
                areas = CAS.get_areas()

            if len(areas):
                crop_img = self.IE.get_crop_image(img,areas)
                store_list.append(areas)
                grayimg = self.IE.get_gray_image(crop_img)
                kp, des = AKA.detect_keypoint(grayimg)
                if kp and AKA.kp:
                    match_point ,_ = AKA.recognize(kp, des)
                    store_list.append(match_point)
                    #正規化
                    norm_point = AKA.norm_matchpoint(kp, match_point)
                    store_list.append(norm_point)
                else:
                    store_list.extend([[],0])
                
                AKA.feature_buffer(kp, des)
            else:
                store_list.extend([["null", "null", "null", "null"],[],0])

            

            if not self.mode == "norecord":
                self.IS.store(img)

            self.CS.store(store_list)
            store_list = []
            self.fps.update()

    def main(self):
        try:
            self.stream()
        except :
            traceback.print_exc()
        finally:
            self.fps.stop()
            try:
                fps_ave = self.fps.fps()
            except ZeroDivisionError as e:
                print("{0}".format(e))
            
            frame_list = list(range(self.fps._numFrames))
            self.CS.write(frame_list, round(fps_ave,2))

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="../models/cascade_sideface.xml", help="Path of the detection model.")# cascade_1125_1_shuf_half.xml
    parser.add_argument("--usbcam", type=int, default=0, help="USB Camera number.")
    parser.add_argument("--storepath", help="if you want to record.")
    parser.add_argument(
        "--StoreType","-s",
        default="Image",
        help="Choose Movie or Image or norecord file you want to store.",
    )

    args = parser.parse_args()
    cascade = args.model
    mode = args.StoreType
    path = args.storepath
    w = 600
    h = 480
    SFS = SideFaceStreaming(path, w, h, mode, cascade)
    SFS.main()

