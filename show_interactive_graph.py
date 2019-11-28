import matplotlib.pyplot as plt
import csv
import pandas as pd

def get_column_csv(path):
    df = pd.read_csv(path)
    columns = df.columns
    column_dict = {}
    for column in columns:
        column_dict.setdefault(column, df[column])
    return column_dict

def read_csv(path):

    csv_list = []
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            csv_list.append(row)
    return csv_list



# 初期化
x = []
y = []
plt.ion()

# MATPLOTLIB コンフィグ
plt.title('Simple Curve Graph') ## グラフタイトル（必須ではない）
plt.xlabel("frame") ## x軸ラベル（必須ではない）
plt.ylabel("match") ## y軸ラベル（必須ではない）
xlim = [0,100] # x軸範囲固定（必須ではない）
# plt.grid() ## グリッド線オン（必須ではない）

path = "/Users/okayamashoya/Downloads/2019-11-27-19-50-39.csv"
column_dict = get_column_csv(path)
all_x = column_dict.get("frames")
all_y  = column_dict.get("matchpoint")
for (ix, iy) in zip(all_x, all_y):
    x.append(ix)
    y.append(iy)
    plt.plot(x,y,color='blue')

    ## グラフ描画
    plt.draw()

    ## 更新待機（秒）
    plt.pause(0.08)

    if len(x) >= 100:
        del x[0]
        del y[0]
        xlim[0] += 1
        xlim[1] += 1

    plt.xlim(xlim[0], xlim[1])


# グラフを閉じる
plt.close()
