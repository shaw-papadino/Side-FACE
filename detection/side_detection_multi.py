import cv2
import argparse
import time
from time import sleep
import multiprocessing as mp
from PIL import Image

lastresults = None
processes = []
frameBuffer = None
results = None
fps = ""
detectfps = ""
framecount = 0
detectframecount = 0
time1 = 0
time2 = 0
box_color = (255, 128, 0)
box_thickness = 1
label_background_color = (125, 175, 75)
label_text_color = (255, 255, 255)

def capture_thread(usbcam, frameBuffer, results, vidfps, camera_width, camera_height):
    """
    "
    "
    "
    "USBカメラ(0)でキャプチャする
    "
    "
    "
    "
    """
    global fps
    global detectfps
    global framecount
    global detectframecount
    global time1
    global time2
    global lastresults
    global cam
    global window_name

    cam = cv2.VideoCapture(usbcam)
    cam.set(cv2.CAP_PROP_FPS, vidfps)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)

    while True:
        t1 = time.perf_counter()
        ret, img = cam.read()
        if not ret:
            continue

        if frameBuffer.full():
            frameBuffer.get()

        frames = img
        frameBuffer.put(img.copy())
        res = None

        if not results.empty():
            res = results.get(False)
            detectframecount += 1
            imdraw = overlay_on_image(frames, res, camera_width, fps, detectfps)
            lastresults = res

        else:
            imdraw = overlay_on_image(frames, lastresults, camera_width, fps, detectfps)

        cv2.imshow("usb Camera",imdraw)

        if cv2.waitKey(1)&0xFF == ord('q'):
            break

        # FPS calculation
        framecount += 1
        if framecount >= 15:
            fps       = "(Playback) {:.1f} FPS".format(time1/15)
            detectfps = "(Detection) {:.1f} FPS".format(detectframecount/time2)
            framecount = 0
            detectframecount = 0
            time1 = 0
            time2 = 0
        t2 = time.perf_counter()
        elapsedTime = t2-t1
        time1 += 1/elapsedTime
        time2 += elapsedTime

def detection(results, frameBuffer, cascade, minsize): 
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
    while True:
        
        if frameBuffer.empty():
            continue
        else:
            img = frameBuffer.get()
            prepimg = img[:, :, ::-1].copy()
            prepimg = Image.fromarray(prepimg)
            grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            tinf = time.perf_counter()
            ans = cascade.detectMultiScale(grayimg, scaleFactor=1.1, minNeighbors=5,\
                    minSize=(minsize,minsize), maxSize=(minsize+300,minsize+300))
            results.put(ans)

def overlay_on_image(frames, object_areas, camera_width, fps, detectfps):
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
    img = frames
    if isinstance(object_areas, type(None)):
        return img
    img_cp = img.copy()
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
    
    cv2.putText(img_cp, fps,       (camera_width-170,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
    cv2.putText(img_cp, detectfps, (camera_width-170,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)

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
    vidfps = 30

    try:
        mp.set_start_method('forkserver')
        # Quene(maxsize)
        frameBuffer = mp.Queue(10)
        results = mp.Queue()

        # Start streaming
        p = mp.Process(target=capture_thread,
                       args=(usbcam, frameBuffer, results, vidfps, camera_width, camera_height),
                       daemon=True)
        p.start()
        processes.append(p)

        # Activation of detection
        p = mp.Process(target=detection,
                       args=(results, frameBuffer, cascade, minsize),
                       daemon=True)
        p.start()
        processes.append(p)

        while True:
            sleep(1)

    finally:
        for p in range(len(processes)):
            processes[p].terminate()
