import ffmpeg
import glob
import os
from datetime import datetime
import time
import argparse
from env_sidesmile_calc import text2lists
"""
1.連番画像のタイトルを取得
2.与えられたフレームレートと1を使って、その画像が動画の何秒地点なのかを計算
3.1のはじめから次の画像が0.3秒以内に存在するのかを確認
4.あれば同一の笑いとみなす、なければ、次の笑い区間として2に戻る
5.次の区間に移る際に、1秒以上笑い区間であれば、その区間の始まりと終わりの時間から真ん中を算出
6.その真ん中から8秒手前2秒後の時に何秒地点なのかを変数(s=8,f=18)に保持
7.配列の末尾の値内にsがなければ、変数を配列[[8,18],[25,35],[40,50]]に格納、あれば末尾の値の2番目にfを代入する
8.配列内の値を使ってffmpegで前側カメラで撮影した動画を切り取った動画を出力する。
"""
def cut_video(startT, input, output, path, f, pathtype):

    stream = ffmpeg.input(input)
    # path = "./20190124201103_result/P_20190124201103/"
    starttime = int(startT * 60) # 1は39分から,2は34分から
    framerate = f
    beforeTime = 0
    sumTime = 0
    time_List = []
    flg = False
    nextTime = -1

    if pathtype:
        filelist = text2lists(path)
    else:

        filelist = sorted(glob.glob(path + "*.jpg"))

    for file in filelist:
        if pathtype:
            file = file.split()
            file = file[0].replace("img/", "").replace("image_", "").replace(".jpg", "")
        else:
            file = os.path.splitext(os.path.basename(file))[0]
        fileTime = round(int(file.replace("image_", "")) / int(framerate), 2)

        if fileTime < nextTime:
            # print("un")
            continue
        # print(fileTime)
        # print(sumTime)
        elapsed = round(fileTime - beforeTime, 2)


        # 0.5秒ぶんより大きければ、次の区間へ
        if beforeTime == 0 or elapsed > 0.5:
            # 1笑い0.4~0.8が一番多かったため。
            if sumTime >= 0.4:
                mid = beforeTime - (sumTime / 2)
                s = mid - 8
                # s = (beforeTime - sumTime) + ((beforeTime - (beforeTime - sumTime)) / 2) - 8
                if s < 0:
                    s = 0
                f = mid + 8
                # f = (beforeTime - sumTime) + ((beforeTime - (beforeTime - sumTime)) / 2) + 8
                time_List.append([s, f])
                nextTime = mid + 10
                # if time_List != [] and time_List[-1][1] > s:
                #     time_List[-1][1] = f
                # else:
                #     time_List.append([s, f])
                print(time_List)
            sumTime = 0
        else:
            print("sum:{0}".format(sumTime))
            sumTime += elapsed
        beforeTime = fileTime
    # time_List = time_List + starttime

    for time_l in time_List:
        f = time_l[1] - time_l[0]
        s = time_l[0] + starttime
        print(time_l)
        dstream = ffmpeg.output(stream, output + str(s) + "-" + str(f) + ".avi",t=f, ss=s)
        ffmpeg.run(dstream)
        # time.sleep(10)
def parse_args():
    parser = argparse.ArgumentParser(description='cutting video')
    parser.add_argument('--starttime', '-s', type=int, default=24,
                        help='Start time')
    parser.add_argument('--input', '-i', type=str,
                        help='Input movie')
    parser.add_argument('--output', '-o', type=str,
                        help="Output dir")
    parser.add_argument('--path', '-p', type=str,
                        help='imageFile dir or textfile')
    parser.add_argument('--framerate', '-f', type=int, default=25,
                        help='framerate in the movie')
    args = parser.parse_args()
    return args

if __name__ == "__main__":

    args = parse_args()

    if os.path.isdir(args.path):
        pathtype = 0
    else:
        assert os.path.splitext(args.path) not in [".txt", ".dat"], "ファイルの拡張子は.txtか.datにしてね。"
        pathtype = 1

    cut_video(args.starttime,args.input,args.output,args.path,args.framerate, pathtype)
