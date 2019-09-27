# -*- coding: utf-8 -*-
#
# カメラの歪みを戻すための値を計算する
#
import numpy as np
import cv2
import glob
from time import sleep
from datetime import datetime
# from switch_cam import switch_cam

TMP_FOLDER_PATH = "./tmp/"
MTX_PATH = TMP_FOLDER_PATH + "mtx.csv"
DIST_PATH = TMP_FOLDER_PATH + "dist.csv"

# メイン関数
def main():
    switch_cam()
    calcCamera() # カメラの歪みを計算

def switch_cam() :
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    if cap.isOpened() == False:
    	print("Not connected!")
    cap.set(3, 1024)
    cap.set(4, 768)
    frame_count = 1
    print("If you want to resume, press the 'q' key")
    print("----------------------------------------")
    while True :
        ret, img = cap.read()
        if ret == False :
            continue
        # print(ret)
        img = cv2.resize(img, (1000,750))
        img = cv2.flip(cv2.flip(img, 0), 1)
        cv2.putText(img, str(frame_count), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,200), 2, cv2.LINE_AA)
        cv2.imshow("img", img)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            print(frame_count)
            saveImgByTime("img/", img)
            frame_count += 1
            print("If you want to resume, press the 'q' key")
            print("----------------------------------------")

        if cv2.waitKey(100) & 0xFF == ord('t'):
            break
    cap.release()

# カメラの歪みを計算する関数
def calcCamera():
    square_size = 21.0      # 正方形のサイズ(mm)
    pattern_size = (13, 9)  # 模様のサイズ
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []

    for fn in glob.glob("./img/*"):
        # 画像の取得
        im = cv2.imread(fn,0)
        print ("loading..." + fn)
        # チェスボードのコーナーを検出
        found, corner = cv2.findChessboardCorners(im, pattern_size)
        # コーナーがあれば
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            corners2 = cv2.cornerSubPix(im, corner, (5,5), (-1,-1), term)
            # マークをつけて画像保存
            img = cv2.drawChessboardCorners(im, pattern_size, corners2, found)
            saveImgByTime(TMP_FOLDER_PATH, img)
            sleep(1)
        # コーナーがない場合のエラー処理
        if not found:
            print ('chessboard not found')
            continue
        img_points.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
        obj_points.append(pattern_points)

    # 内部パラメータを計算
    rms, K, d, r, t = cv2.calibrateCamera(obj_points, img_points, (im.shape[1],im.shape[0]), None, None)

    # 計算結果を表示
    print ("RMS = ", rms)
    print ("K = \n", K)
    print ("d = ", d.ravel())

    # ファイル保存
    saveCalibrationFile(K, d, MTX_PATH, DIST_PATH)

# キャリブレーションCSVファイルを上書き保存する関数
def saveCalibrationFile(mtx, dist, mtx_path, dist_path):
    np.savetxt(mtx_path, mtx, delimiter =',',fmt="%0.14f")   #カメラ行列の保存
    np.savetxt(dist_path, dist, delimiter =',',fmt="%0.14f") #歪み係数の保存

# 画像を時刻で保存する関数
def saveImgByTime(dirPath, img):
    # 時刻を取得
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = dirPath + date + ".png"
    cv2.imwrite(path, img) # ファイル保存
    print("saved: ", path)


if __name__ == '__main__':
    main()
