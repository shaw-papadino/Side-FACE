import cv2
import argparse
import sys
import time
from time import sleep
import csv
import datetime

from match_keypoint import *

fpstext = ""
framecount = 0
time1 = 0
time2 = 0
frame = 0
match_points = []
fps_list = []

def make_status_bar(count):
    """
    認識数をステータスバーに表示する
    """

    maxcount = 10
    bar  = count*"@" + (maxcount - count)*" "
    text = "\r| {} | [ {} / {} % ]".format(bar, str(count*10), str(maxcount*10))
    return text

def write_status_bar(count):
    """
    ステータスバーを標準出力に書き込み
    """

    text = make_status_bar(count)
    sys.stdout.write(text)
    sys.stdout.flush()

def crop_image(image, object_areas):
    """
    認識した部分をクロップした画像を返す
    """
    if isinstance(object_areas, tuple):
        return []
    # img[y: y + h, x: x + w]
    for (x, y, w, h) in object_areas:
        return image[y:y+h, x:x+w]

def capture(usbcam, vidfps, camera_width, camera_height, cascade, minsize):

    """csvへの記載をどうするか"""
    global fpstext
    global framecount
    global time1
    global time2
    global frame
    global match_points
    global fps_list 

    cam = cv2.VideoCapture(usbcam)
    cam.set(cv2.CAP_PROP_FPS, vidfps)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    # 幅
    W = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 高さ
    H = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter("../result/" + filename + ".avi",fourcc, vidfps, (W, H))

    prev_areas = ()
    prev_keypoint = []
    prev_description = []
    # nodetect_count = 0

    while True:
        t1 = time.perf_counter()
        
        ret, img = cam.read()
        if not ret:
            continue

        result_areas = detection(img, cascade, minsize)
        if isinstance(result_areas, tuple) and isinstance(prev_areas, tuple):
            pass

        elif isinstance(prev_areas, tuple):
            prev_areas = result_areas

        elif isinstance(result_areas, tuple):
            result_areas = prev_areas
        else:
            prev_areas = result_areas
            
        
        cropimage = crop_image(img, result_areas)

        imdraw = overlay_on_image(img, result_areas, camera_width, fpstext)
        if isinstance(cropimage, list):
            pass
        else:
            keypoint, description = detect_keypoint(cropimage)
            if keypoint == [] and prev_keypoint  == []:
                pass

            elif prev_keypoint  == []:
                prev_keypoint = keypoint
                prev_description = description
            
            elif keypoint  == []:
                keypoint = prev_keypoint
            
            else:
                # matching
                previmg_points, nextimg_points, matching_list = match_keypoint(prev_keypoint, keypoint, prev_description, description)
                print("match:{}".format(len(previmg_points)))
                match_points.append(previmg_points)
                prev_keypoint = keypoint
                prev_description = description

        # cv2.imshow("usb Camera", imdraw)
        out.write(imdraw)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break

        # FPS calculation
        framecount += 1
        if framecount >= 15:
            fps = (time1/15)
            fps_list.append(fps)
            fpstext = "(Playback) {:.1f} FPS".format(fps)
            framecount = 0
            time1 = 0
            time2 = 0

        t2 = time.perf_counter()
        elapsedTime = t2-t1
        time1 += 1/elapsedTime
        time2 += elapsedTime

        frame += 1
        """
        write_status_bar(detectcount)
        if framecount % 9 == 0:
            # print(detectcount)
            detectcounts.append([detectcount])
            detectcount = 0
        """


def detection(img, cascade, minsize): 
    """
    "
    "
    "
    "opencvで作成した識別器を用いて横顔笑顔認識を行う
    "
    "label:横顔笑顔があるか
    "
    "
    """

    cascade = cv2.CascadeClassifier(cascade)
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ans = cascade.detectMultiScale(grayimg, scaleFactor=1.1, minNeighbors=3,\
            minSize=(minsize,minsize), maxSize=(minsize+300,minsize+300))
    
    return ans

def overlay_on_image(frames, object_areas, camera_width, fpstext):
    """
    "
    "
    "
    "認識結果を畳込む
    "
    "imgdraw: 畳込み後の画像
    "
    "
    """

    box_color = (255, 128, 0)
    box_thickness = 1
    label_background_color = (125, 175, 75)
    label_text_color = (255, 255, 255)

    img = frames
    cv2.putText(img, fpstext,(camera_width-170,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)

    if isinstance(object_areas, tuple):
        return img
    else:
    # if isinstance(object_areas, type(None)):
    #     return img


        img_cp = img.copy()

        # cv2.putText(img_cp, fpstext,(camera_width-170,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
        # text = make_status_bar(detectcount)
        # cv2.putText(img_cp, text,(camera_width-170,45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)

        # if detectcount < 6:
        #     return img_cp

        for (x, y, w, h) in object_areas:
            box_top = y
            box_left = x
            box_right = x + w
            box_bottom = y + h

            cv2.rectangle(img_cp, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness)

            label_text = "DETECT!"
            label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            label_left = box_left
            label_top = box_top - label_size[1]
            if (label_top < 1):
                label_top = 1
            label_right = label_left + label_size[0]
            label_bottom = label_top + label_size[1]

            cv2.rectangle(img_cp, (label_left - 1, label_top - 1), (label_right + 1, label_bottom + 1), label_background_color, 10)
            cv2.putText(img_cp, label_text, (label_left, label_bottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_text_color, 2)
        

            return img_cp

if __name__=="__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="", help="Path of the detection model.")
    parser.add_argument("--usbcam", type=int, default=0, help="USB Camera number.")
    parser.add_argument("--minsize", type=int, default=450, help="Detect minimum size..")
    args = parser.parse_args()

    cascade = args.model
    usbcam = args.usbcam
    minsize = args.minsize

    camera_width =  1024 #600
    camera_height = 768 #480
    vidfps = 15

    try:
        capture(usbcam, vidfps, camera_width, camera_height, cascade, minsize)

    finally:
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # 平均fpsを算出
        fps_ave = sum(fps_list) / len(fps_list)
        with open("../result/" + filename + ".csv", "w") as f:
            writer = csv.writer(f, lineterminator="\n") # 改行コード（\n）を指定しておく

            writer.writerow(["frames","matchpoint",round(fps_ave,2)])
            # frameのリスト作成
            frame_list = list(range(frame))
            # frame, matchpointを書き込み
            for (frame, point) in zip(frame_list, match_points):

                writer.writerow([frame, len(point)])
