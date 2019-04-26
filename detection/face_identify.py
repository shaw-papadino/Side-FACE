# -*- coding: utf-8 -*-
# 電気技術特論 I-a 2018/6/19
# 顔認識　with opencv 3.3
from datetime import datetime
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import sys
import time
import csv

class face_recognizer() :
    # open cv の顔認識の準備。
    def __init__(self) :
        # path = "../201804280930/"
        # cascade = "cascade/0629_neo/cascade.xml"
        # self.cascade = cv.CascadeClassifier(path + cascade)
        self.face_cascade = cv.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')
        self.path = "./201804280930/05_8/"
    #　opencv をつかって、顔を見つけて、1つ目の顔の位置を返す関数, detect_face
    def detect_face(self,img):
        # カラー画像から、グレー画像に変換する。
        print("predetect")
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        #　img画像から、顔を検出する。
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

        #if 顔が見つからなかったら、False, None, None  を返す。
        if (len(faces) == 0):
            print("noface")
            return False, None, None

        # 一つ目の顔の領域を、取り出す。
        (x, y, w, h) = faces[0]

        #　顔が見つかったら、True, 一つ目の顔の画像と、その位置を返す。
        return True, gray[y:y+w, x:x+h], faces[0]

    # USBカメラでキャプチャーし、顔が検知されたら、顔の部分の画像だけ、ファイルに保存する。
    # ファイル名は、検出した 月日時分秒.jpg
    def capture_face_from_usbcam(self,dir,number) :
        # usb カメラから画像を取り込む準備。
        cap = cv.VideoCapture(0)

        count = 0
        while True:
            ret, img = cap.read()
            if not ret:
                continue

            f, img, face = self.detect_face(img)
            if f :
                print("Found face in "+str(face))
                plt.imshow(img,"gray")
                cv.imwrite(dir+"/p_"+datetime.now().strftime("%y%m%d%H%M%S")+".jpg", img)
                count = count + 1
                time.sleep(1)
            if count > number :
                break
        cap.release()

    # 顔識別を行うために、全景の画像から、顔の部分を切り出したファイルを作成する。
    # 　全景の画像　./faces/*/org/*.jpg
    #  作成する顔画像 ./faces/*/*.jpg
    def prepare_facefiles(self) :
        face_org_dirs = glob.glob("./faces/*/org")
        for dir in face_org_dirs :
            p_dir = os.path.dirname(dir)
            for org in glob.glob(dir+'/*.jpg') :
                new_f = p_dir+'/'+os.path.basename(org)
                if os.path.exists(new_f) :
                    continue
                img = cv.imread(org)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                #　img画像から、顔を検出する。
                faces = self.face_cascade.detectMultiScale(gray,
                                                      scaleFactor=1.2,
                                                      minNeighbors=5)
                if len(faces) > 0 :
                    (x,y,w,h) = faces[0]
                    face_img = gray[y:y+w, x:x+h]
                    cv.imwrite(new_f,face_img)

    # 顔画像から、識別器を作る（学習させる）
    # 利用するデータ、　
    #      ./faces 以下のディレクトリ名が、顔識別のラベル
    #      ./faces/*/*.jpg  が、ラベルの正解画像
    def make_classifier(self) :
        # print(cv.__version__)
        # LBPH face recognizer 　を作成する。
        # self.face_recognizer = cv.createLBPHFaceRecognizer()  # for opencv 2.7
        self.face_recognizer = cv.face.LBPHFaceRecognizer_create() # for opencv 3.3

        face_dirs = glob.glob(self.path + "faces/Train/*")
        faces = []
        idxes = []
        self.labels= []
        idx = 1
        print(face_dirs)
        for ps in face_dirs :
            name = os.path.basename(ps)
            self.labels.append(name)
            n = 0
            for p in glob.glob(ps+"/*.jpg") :
                img = cv.imread(p,cv.IMREAD_GRAYSCALE)
                faces.append(img)
                idxes.append(idx)
                n = n + 1

            idx = idx + 1
        print(self.labels)
        # print(idxes)
        self.face_recognizer.train(faces,np.array(idxes))
        print("Training FINISH!")
        self.face_recognizer.save(self.path + "0814_05.yml")

        with open(self.path + '0814_05.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerow(self.labels)     # list（1次元配列）の場合

    #
    # 識別器の確認を行う。
    #
    def check_classifier(self) :
        face_dirs = glob.glob(self.path + "faces/Test/*")
        n = 0
        c = 0
        path = "./201804280930/"
        fileList = sorted(glob.glob(self.path + "faces/Test/N_P_450/*.jpg"))
        self.face_recognizer = cv.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read(self.path + "0814_05.yml")

        with open(self.path + "0814_05.csv", 'r') as f:
            reader = csv.reader(f)
            # header = next(reader)  # ヘッダーを読み飛ばしたい時

            for i in reader:
                # print(i)
                self.labels = i

        print(self.labels)
        for ps in face_dirs :
            name = os.path.basename(ps)
            for p in fileList :
                face = cv.imread(p,cv.IMREAD_GRAYSCALE)
                print(p)
                idx = self.face_recognizer.predict(face)
                print(idx)
                # print(name + ": " + reg.labels[idx[0]-1])
                if name == self.labels[idx[0]-1] :
                    print(name)
                    c = c + 1
                n = n + 1
            print(c)
        print(n)
        print(c*100.0/n)

    #
    #  USBカメラでキャプチャーされた画像を、作成された識別器で、識別し、結果を表示する。
    #
    def recognize(self) :
        # usb カメラから画像を取り込む準備。
        # cap = cv.VideoCapture(0)

        # count = 0
        # while True:
            # ret, img = cap.read()


            # if not ret:
            #     continue
        f, face, rect = self.detect_face(img)

        if f :
            print("Found face in "+str(face))
            (x,y,w,h) = rect
            idx = self.face_recognizer.predict(face)
            #        print(idx)
            if idx[0] > 0 :
                cv.rectangle(img,(x,y),(x+w,y+h), (0,255,0),2)
                print(self.labels[idx[0]-1], idx[1])

                #plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
                # cv.imshow("result",img)
                # cv.waitKey(10000)
                # count = count + 1
            # if count > 0 :
            #     break
        # cap.release()

if __name__ == '__main__' :
    args = sys.argv

    if len(args) == 1 :
        recg = face_recognizer()
        # recg.prepare_facefiles()
        recg.make_classifier()
        # recg.check_classifier()
        # recg.recognize()
    else :
        if len(args) == 4 :
            if args[1] == "register" :
                name = args[2]
                number = int(args[3])
                if not os.path.exists("./faces/"+name ) :
                    os.makedirs("./faces/"+name)
                recg = face_recognizer()
                recg.capture_face_from_usbcam("./faces/"+name,number)
