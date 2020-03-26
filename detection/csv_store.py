import csv
import datetime
from image_check import Checker

class CsvStore():
    def __init__(self,path):
        self.store_lists = []
        Check = Checker()
        self.path = path
        if Check.store_path(self.path):
            pass
        else:
            os.mkdir(self.path)

    def store(self, store_list):
        s_cp = store_list.copy()
        self.store_lists.append(s_cp)

    def write(self, frame_list, fps):
        strtime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        with open(self.path + "/" + strtime + ".csv", "w") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(
                ["frames", "time[ms]", "matchpoint", "norm_result", "x", "y", "w", "h", fps]
            )
            # print(self.store_lists[0])
            # frame, 経過時間,  matchpoint, crop座標を書き込み
            for frame, (detecttime, area, point, norm_result) in zip(frame_list,self.store_lists):
                area = area[0]
                writer.writerow(
                    [frame, int(detecttime * 1000), len(point), norm_result, area[0], area[1], area[2], area[3]]
                )

