from PIL import Image
import numpy as np
import os, glob

#画像フォルダへの絶対パス
ROOT_DIR = "/Users/tatsuro64/BeautifulWomenCLF/MyDataSet/imgs/"
#各美女の顔画像フォルダ名
WOMEN = ["aoi_ROI", "erika_ROI", "gakky_ROI", "hikari_ROI", "tsubasa_ROI"]

#美女クラス
class SideSmile:
    def __init__(self, data, target, target_names, images):
        self.data = data
        self.target = target
        self.target_names = target_names
        self.images = images

    #キー(インスタンス変数)を取得するメソッド
    def keys(self):
        print("[data, target, target_names, images]")


#画像データをNumpy形式に変換してデータセットを作成
def load_beautiful_women():
    data = []      #画像の一次元データを格納するlist
    target = []    #ラベル(正解)の情報を格納するlist
    target_names = ["aoi", "erika", "gakky", "hikari", "tsubasa"]
    images = []    #画像の2次元データを格納するlist

    for label, woman in enumerate(WOMEN):
        file_dir = ROOT_DIR + woman
        #美女画像を全て取ってくる
        files = glob.glob(file_dir + "/*.jpg")
        print("~~~~~~~~{}の画像をNumpy形式に変換し、Listに格納中~~~~~~~~".format(woman))
        for i, f in enumerate(files):
            img = Image.open(f)
            img = img.convert('L')          #画像をグレースケールに変換
            #img = img.resize((128, 128))    #画像サイズの変更
            imgdata = np.asarray(img)       #Numpy配列に変換
            images.append(imgdata)          #画像データ: 128*128の2次元配列
            data.append(imgdata.flatten())  #画像データ: 16,384の1次元配列
            target.append(label)            #正解ラベルを格納

    print("------------ListをNumpy形式に変換中--------------")
    data = np.array(data)
    target = np.array(target)
    target_names = np.array(target_names)
    images = np.array(images)

    #インスタンスを生成
    beautifulWomen = BeautifulWomen(data, target, target_names, images)

    return beautifulWomen
