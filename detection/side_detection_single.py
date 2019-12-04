import os
import cv2
import argparse
import sys
import time
from time import sleep
import csv
import datetime

from match_keypoint import *
from WebcamVideoStream import WebcamVideoStream
# webcam高速?
from imutils.video import FPS
import imutils
fps = FPS()

match_points = []
time_list = []
area_list = []


def make_status_bar(count):
    """
    認識数をステータスバーに表示する
    """

    maxcount = 10
    bar = count * "@" + (maxcount - count) * " "
    text = "\r| {} | [ {} / {} % ]".format(bar, str(count * 10), str(maxcount * 10))
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
        return image[y : y + h, x : x + w]


def apply_areas(result_areas, prev_areas, area_list):

    if isinstance(result_areas, tuple) and isinstance(prev_areas, tuple):
        "not 認識 & not 過去の認識"
        area_list.append([["null", "null", "null", "null"]])

    elif isinstance(prev_areas, tuple):
        "過去の座標がなければ現フレーム座標を代入"
        prev_areas = result_areas
        area_list.append(result_areas)

    elif isinstance(result_areas, tuple):
        "現フレーム座標なければ過去の座標を代入"
        result_areas = prev_areas
        area_list.append(result_areas)
    else:
        "現フレーム座標を過去の座標に代入"
        prev_areas = result_areas
        area_list.append(result_areas)

    return result_areas, prev_areas, area_list


def capture(
    usbcam, vidfps, camera_width, camera_height, cascade, minsize, file_format, vision, record, vs
):

    # csv 書き込む用
    global match_points
    global time_list
    global area_list

    # 前フレーム保持用
    prev_areas = ()
    prev_keypoint = []
    prev_description = []
    

    cam = cv2.VideoCapture(usbcam)
    cam.set(cv2.CAP_PROP_FPS, vidfps)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
    strtime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    if record:
        if file_format == "Movie":
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            # 幅
            W = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            # 高さ
            H = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter("../result/" + strtime + ".avi", fourcc, vidfps, (W, H))
        elif file_format == "Image":
            if not os.path.isfile("../result/" + strtime):
                os.mkdir("../result/" + strtime)
    else:
        pass

    starttime = time.perf_counter()
    time_list.append(starttime - starttime)
    # vs.start()
    fps.start()
    while True:

        ret, img = cam.read()
        # img = vs.read()

        if not ret:
            continue

        str_frame_time = datetime.datetime.now().strftime("%H-%M-%S-%f")[:-3]
        detecttime = time.perf_counter() - starttime
        time_list.append(detecttime)

        result_areas = detection(img, cascade, minsize)
        result_areas, prev_areas, area_list = apply_areas(result_areas, prev_areas, area_list)

        cropimage = crop_image(img, result_areas)

        if isinstance(cropimage, list):
            "cropimageがなければ"
            match_points.append([])

        else:
            keypoint, description = detect_keypoint(cropimage)

            if keypoint == []:
                "現在のkeypointがなければ"
                match_points.append([])

            elif prev_keypoint == []:
                "過去のkeypointがなければ"
                prev_keypoint = keypoint
                prev_description = description
                match_points.append([])

            else:
                "どちらもある場合"
                previmg_points, _, _ = match_keypoint(
                    prev_keypoint, keypoint, prev_description, description
                )
                # print("match:{}".format(len(previmg_points)))
                match_points.append(previmg_points)

                prev_keypoint = keypoint
                prev_description = description

        if vision:
            # crop結果を重畳
            imdraw = overlay_on_detect_image(img, camera_width, result_areas)
            cv2.imshow("usb Camera", imdraw)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            pass

        if record:
            # 記録する用
            if file_format == "Movie":
                out.write(img)

            elif file_format == "Image":
                cv2.imwrite("../result/" + strtime + "/" + str_frame_time + ".jpg", img)

        else:
            pass

        fps.update()


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

    ans = cascade.detectMultiScale(
        grayimg,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(minsize, minsize),
        maxSize=(minsize + 100, minsize + 100),
    )

    return ans


def overlay_on_fps_image(frames, camera_width, fpstext):
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
    cv2.putText(
        img,
        fpstext,
        (camera_width - 170, 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (38, 0, 255),
        1,
        cv2.LINE_AA,
    )

    return img


def overlay_on_detect_image(frames, camera_width, object_areas):
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

    if isinstance(object_areas, tuple):
        return img
    else:

        img_cp = img.copy()

        for (x, y, w, h) in object_areas:
            box_top = y
            box_left = x
            box_right = x + w
            box_bottom = y + h

            cv2.rectangle(
                img_cp, (box_left, box_top), (box_right, box_bottom), box_color, box_thickness
            )

            label_text = "DETECT!"
            label_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            label_left = box_left
            label_top = box_top - label_size[1]
            if label_top < 1:
                label_top = 1
            label_right = label_left + label_size[0]
            label_bottom = label_top + label_size[1]

            cv2.rectangle(
                img_cp,
                (label_left - 1, label_top - 1),
                (label_right + 1, label_bottom + 1),
                label_background_color,
                10,
            )
            cv2.putText(
                img_cp,
                label_text,
                (label_left, label_bottom),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                label_text_color,
                2,
            )

            return img_cp


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", default="", help="Path of the detection model.")
    parser.add_argument("--usbcam", type=int, default=0, help="USB Camera number.")
    parser.add_argument("--minsize", type=int, default=250, help="Detect minimum size.")
    parser.add_argument("--vision", action="store_true", help="If you want to show image.")
    parser.add_argument("--record", action="store_true", help="if you want to record.")
    parser.add_argument(
        "--StoreFileType",
        "-s",
        default="Image",
        help="Choose Movie or Image file you want to store.",
    )
    args = parser.parse_args()

    cascade = args.model
    usbcam = args.usbcam
    minsize = args.minsize
    file_format = args.StoreFileType
    vision = args.vision
    record = args.record
    camera_width = 600  # 1024 #600
    camera_height = 480  # 768 #480
    vidfps = 27

    try:
        vs = WebcamVideoStream(usbcam, vidfps, camera_width, camera_height)
        capture(
            usbcam,
            vidfps,
            camera_width,
            camera_height,
            cascade,
            minsize,
            file_format,
            vision,
            record,
            vs
        )

    finally:
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # fps_ave = 0
        fps.stop()
        try:
            # 平均fpsを算出
            # fps_ave = sum(fps_list) / len(fps_list)
            fps_ave = fps.fps()

        except ZeroDivisionError as e:
            print("{0}".format(e))

        with open("../result/" + filename + ".csv", "w") as f:
            writer = csv.writer(f, lineterminator="\n")  # 改行コード（\n）を指定しておく

            writer.writerow(
                ["frames", "time[ms]", "matchpoint", "x", "y", "w", "h", round(fps_ave, 2)]
            )
            # frameのリスト作成
            # frame_list = list(range(frame))
            frame_list = list(range(fps._numFrames))
            # frame, 経過時間,  matchpoint, crop座標を書き込み
            for frame, detecttime, point, area in zip(
                frame_list, time_list, match_points, area_list
            ):
                area = area[0]
                writer.writerow(
                    [frame, int(detecttime * 1000), len(point), area[0], area[1], area[2], area[3]]
                )
