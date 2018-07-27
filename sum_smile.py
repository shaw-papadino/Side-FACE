# ~utf-8~
import cv2
from face_square_clips import face_square_clips
from side_smile import Detection
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import datetime as dt
import collections
import re
import os



class hist_smile(Detection):
    def sum_smile(self):
        sectionPlist = open(self.path_img + "section_positive.txt").readlines()
        sum_smile_l = []
        P_P = 0
        P_N = 0
        N_P = 0
        N_N = 0
        for i in range(len(self.file_lists) - 30):
            sum = 0
            P_in = 0
            #print("pi")
            if i % 30 == 0:
                print(i)
            for file_list in self.file_lists[0+i:30+i]:

                flg, img, img_file_name = face_square_clips(self.cascade, file_list, self.m_size)
                if flg == True:
                    sum += 1
                    # print(sum)
            for s in sectionPlist:
                s = s.split("-")
                # print(s[0])
                if i == int(s[0]):
                    P_in += 1
                    print(P_in)

            if P_in != 0 and sum >= 15: # default = 20
                P_P += 1
                print(P_P)
            elif P_in == 0 and sum < 15:
                N_N += 1
            elif P_in != 0 and sum < 15:
                P_N += 1
            elif P_in == 0 and sum >= 15:
                N_P += 1
            sum_smile_l.append(sum)
        result_d = {"ALL": len(self.file_lists) - 30,"P_P": P_P, "P_N": P_N, "N_P": N_P, "N_N": N_N}
        for key, value in result_d.items():
            print("key:", key, "-- value:", str(value))


    def create_section_positive(self):
        f = open("./section_positive.txt", mode='w')
        f_n = open("./section_negative.txt", mode='w')
        for i in range(len(self.file_lists) - 30):
            sum = 0
            pinSection = 0
            for file_list in self.file_lists[0+i:30+i]:
                f_name = os.path.splitext(os.path.basename(file_list))[0]
                # print("f_name" + f_name)
                for s in self.P_l:
                    # print(s)
                    s = s.replace("img/", "").replace(".jpg", "")
                    s = s.split(" ")
                    # print("s_name" + s[0])
                    if f_name == s[0]:
                        pinSection += 1
                        # print(pinSection)
            # print(pinSection)
            if pinSection >= 20:
                s = str(0+i) + "-" + str(30+i) + ":" + str(pinSection) + "\n"
                f.write(s)
            else:
                s = str(0+i) + "-" + str(30+i) + ":" + str(pinSection) + "\n"
                f_n.write(s)


    def write_histgrum(self, time_s, flg, c):
        fp = FontProperties(fname = "/Users/okayama/Library/Fonts/ipaexg.ttf")
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        if flg == "time":
            c_v = [k for k in c.values()]
            c_k = [k for k in c]
            ax.hist(time_s,bins=len(c_k))#int(max(s_s_l))
            ax.set_xlabel(u"笑い秒/回", fontproperties = fp)
            ax.set_ylabel(u"回数", fontproperties = fp)
            ax.set_ylim(0,max(c_v)+1)
            ax.set_title(u"笑い平均時間分布", fontproperties = fp)
        else:
            ax.hist(time_s_t,bins=len(time_s))#int(max(s_s_l))
            ax.set_xlabel(u"区間内笑い回数", fontproperties = fp)
            ax.set_ylabel(u"回数", fontproperties = fp)
            ax.set_ylim(0,max(time_s))
            ax.set_title(u"区間内笑い平均時間分布", fontproperties = fp)
        plt.show()


    def hist_time(self):
        sum = 0
        time_smile = []
        pattern = "(.*)_(.*)"
        list_sect = [352, 1900, 1914, 3730, 4660]
        f = open("./short_smile(0.4).txt", mode='w')
        for idx_l, i_l in enumerate(list_sect):

            if idx_l == 4:
                break
            for idx, p_img in enumerate(self.P_l[i_l:list_sect[idx_l+1]]):
                print(p_img)
                if idx == list_sect[idx_l+1] - (i_l+1):#351
                    break
                # print(p_img)
                p_img = p_img.replace("img/", "")
                p_img = p_img.split(" ")
                p_img_d = re.search(pattern, str(p_img[0]))
                # current_slice_s = p_img[0][-6:-4]
                # current_slice_m = p_img[0][-8:-6]
                # current_slice_h = p_img[0][-10:-8]
                current_slice = p_img_d.group(2)

                name_c, ext = os.path.splitext(str(current_slice))
                print(name_c)
                #new_time1 = dt.datetime.strptime(current_slice_s, "%H%M%S")
                #print(new_time1)
                next_img = self.P_l[i_l:][idx+1].replace("img/", "")
                next_img = next_img.split(" ")
                next_img_d = re.search(pattern, str(next_img[0]))

                # next_slice_s = next_img[0][-6:-4]
                # next_slice_m = next_img[0][-8:-6]
                # next_slice_h = next_img[0][-10:-8]
                next_slice = next_img_d.group(2)
                name_n, ext = os.path.splitext(str(next_slice))
                print(name_n)
                #new_time2 = dt.datetime.strptime(next_slice_s, "%H%M%S")
                #t = new_time1 - new_time2
                #print(t)
                if int(name_n) - int(name_c) == 1:
                    s = int(name_n) - int(name_c)
                    # print(s)
                    sum += 0.1
                    print("{0:.2}".format(sum))
                else:
                    time_smile.append(round(sum))
                    # time_smile.append(float(sum))
                    # print(time_smile)
                    if sum < 0.41 and sum > 0.32:
                        s = str(sum) + " " + str(p_img[0]) + "\n"
                        f.write(s)
                    sum = 0
                '''
                if current_slice_s[0] == "0":
                    current_slice_s = current_slice_s[1:]
                if next_slice_s[0] == "0":
                    next_slice_s = next_slice_s[1:]
                if current_slice_m[0] == "0":
                    current_slice_m = current_slice_m[1:]
                if next_slice_m[0] == "0":
                    next_slice_m = next_slice_m[1:]
                if current_slice_h[0] == "0":
                    current_slice_h = current_slice_h[1:]
                if next_slice_h[0] == "0":
                    print(next_slice_h)
                    next_slice_h = next_slice_h[1:]
                print(next_slice_h, current_slice_h)
                if int(next_slice_h) - int(current_slice_h) == 1 or int(next_slice_h) - int(current_slice_h) == -22:
                    next_slice_m = int(next_slice_m) + 60
                    if int(next_slice_m) - int(current_slice_m) == 1:
                        next_slice_s = int(next_slice_s) + 60
                        slice_time = int(next_slice_s) - int(current_slice_s)
                        print(next_slice_s, current_slice_s)
                        print(slice_time)
                        if slice_time >= 3 and slice_time <= 5:
                            sum += slice_time
                            print("sum")
                        else:
                            time_smile.append(sum)
                            print(time_smile)
                            sum = 0
                elif int(next_slice_h) - int(current_slice_h) == 0:
                    if int(next_slice_m) - int(current_slice_m) == 1:
                        next_slice_s = int(next_slice_s) + 60
                        slice_time = int(next_slice_s) - int(current_slice_s)
                        print(next_slice_s, current_slice_s)
                        print(slice_time)
                        if slice_time >= 3 and slice_time <= 5:
                            sum += slice_time
                            print("sum")
                        else:
                            time_smile.append(sum)
                            print(time_smile)
                            sum = 0
                    elif int(next_slice_m) - int(current_slice_m) == 0:
                        slice_time = int(next_slice_s) - int(current_slice_s)
                        print(next_slice_s, current_slice_s)
                        print(slice_time)
                        if slice_time >= 3 and slice_time <= 5:
                            sum += slice_time
                            print("sum")
                        else:
                            time_smile.append(sum)
                            print(time_smile)
                            sum = 0
                    else:
                        time_smile.append(sum)
                        print(time_smile)
                        sum = 0
                else:
                    time_smile.append(sum)
                    print(time_smile)
                    sum = 0
                '''
        c = collections.Counter(time_smile)
        print(c)
        return time_smile , c


if __name__ == "__main__":
    h = hist_smile()

    # s_s_l = h.sum_smile()#section
    # h.write_histgrum(s_s_l)
    h.sum_smile()
    # h.create_section_positive()
    # t_smile, c = h.hist_time()#time
    # h.write_histgrum(t_smile, "time", c)
