# -*- coding: utf-8 -*-
"""
OpenCV 3.1.1による顔追跡
"""

import cv2

# 初期値格納用クラス
class DisplayInfomation:
    pass


# 第三引数はDisplayInformation
def traceFace(cap, cascade, di):
    _, im = cap.read()
    # 処理速度のためグレー化
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # 処理速度のため縮小
    di.height = round(gray.shape[1] / 2)
    di.width = round(gray.shape[0] / 2)
    gray = cv2.resize(gray, (di.height, di.width))

    # 顔探索(画像,縮小スケール,最低矩形数)
    face = cascade.detectMultiScale(gray, 1.1, 3)
    # 顔検出した部分を長方形で囲う
    # TODO:カメラ範囲を越えるとクラッシュする
    for x, y, w, h in face:
        cx = round(x + w / 2)
        cy = round(y + h / 2)
        di.x = x
        di.y = y
        di.w = w
        di.h = h
        di.cx = cx
        di.cy = cy
        if innerDisplay(di):
            infoStr = "(x,y)=" + "(" + str(di.cx) + "," + str(di.cy) + ")"
            cv2.rectangle(gray, (x, y), (x + w, y + h), 255, 3)
        else:
            infoStr = "Outer Area"
        # 画像表示
        cv2.putText(gray, infoStr, (10, 20), 1, 1, (220), 2)
        cv2.imshow("Face detect", gray)


def innerDisplay(di):
    print(di.x + di.w)
    if di.x > 0 and di.y > 0 and di.w < di.width and di.h < di.height:
        return True
    return False


def main():
    di = DisplayInfomation()
    # カメラ映像の取得
    cap = cv2.VideoCapture(0)
    # 顔探索用パターンファイルを取得
    # ファイルが無い場合、以下のリンクから入手
    # https://github.com/opencv/opencv/tree/master/data/haarcascades
    cascade = cv2.CascadeClassifier("../models/haarcascade_frontalface_alt.xml")

    # ロジック本体
    while 1:
        traceFace(cap, cascade, di)
        # キーが押されたら終了
        if cv2.waitKey(10) > 0:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
