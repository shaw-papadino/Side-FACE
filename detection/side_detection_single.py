import cv2
import argparse
import sys
import time
from time import sleep
import csv
import datetime
fps = ""
framecount = 0
time1 = 0
time2 = 0
detectcount = 0
detectcounts = []

def make_status_bar(count):

    maxcount = 10
    bar  = count*"@" + (maxcount - count)*" "
    text = "\r| {} | [ {} / {} % ]".format(bar, str(count*10), str(maxcount*10))
    return text

def write_status_bar(count):

    text = make_status_bar(count)
    sys.stdout.write(text)
    sys.stdout.flush()

def capture(usbcam, vidfps, camera_width, camera_height, cascade, minsize):

    global fps
    global framecount
    global detectcount
    global time1
    global time2

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
    out = cv2.VideoWriter(filename + ".avi",fourcc, vidfps, (W, H))
    while True:
        t1 = time.perf_counter()
        
        ret, img = cam.read()
        if not ret:
            continue

        result_areas = detection(img, cascade, minsize)

        imdraw = overlay_on_image(img, result_areas, camera_width, fps)
        cv2.imshow("usb Camera", imdraw)
        out.write(imdraw)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break

        # FPS calculation
        framecount += 1
        if framecount >= 15:
            fps       = "(Playback) {:.1f} FPS".format(time1/15)
            framecount = 0
            time1 = 0
            time2 = 0
        t2 = time.perf_counter()
        elapsedTime = t2-t1
        time1 += 1/elapsedTime
        time2 += elapsedTime

        write_status_bar(detectcount)
        if framecount % 9 == 0:
            # print(detectcount)
            detectcounts.append([,detectcount])
            detectcount = 0



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

def overlay_on_image(frames, object_areas, camera_width, fps):
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
    global detectcount

    box_color = (255, 128, 0)
    box_thickness = 1
    label_background_color = (125, 175, 75)
    label_text_color = (255, 255, 255)

    img = frames
    if object_areas  == ():
        return img
    else:
        detectcount += 1

    # if isinstance(object_areas, type(None)):
    #     return img


        img_cp = img.copy()

        cv2.putText(img_cp, fps,(camera_width-170,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
        text = make_status_bar(detectcount)
        cv2.putText(img_cp, text,(camera_width-170,45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)

        if detectcount < 6:
            return img_cp

        for (x, y, w, h) in object_areas:
            box_top = y
            box_left = x
            box_right = x + w
            box_bottom = y + h

            cv2.rectangle(img_cp, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness)

            label_text = "SMILE!"
            label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 5)[0]
            label_left = box_left
            label_top = box_top - label_size[1]
            if (label_top < 1):
                label_top = 1
            label_right = label_left + label_size[0]
            label_bottom = label_top + label_size[1]

            cv2.rectangle(img_cp, (label_left - 1, label_top - 1), (label_right + 1, label_bottom + 1), label_background_color, 5)
            cv2.putText(img_cp, label_text, (label_left, label_bottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_text_color, 5)
        

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
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        with open(filename + ".csv", "w") as f:
            writer = csv.writer(f, lineterminator="\n") # 改行コード（\n）を指定しておく

            writer.writerow(["frames","detects"])
            writer.writerow([0,0])
            writer.writerows(detectcounts)
