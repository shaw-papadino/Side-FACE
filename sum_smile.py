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
import time
import glob


class hist_smile(Detection):
    def sum_smile(self):

        P_P = 0
        P_N = 0
        N_P = 0
        N_N = 0
        imgFileSum = 0
        # pattern = "(.*)0.1s_" + str(x) + "([0-9]+).jpg"
        for x in range(1,5):
            imgFile = glob.glob(self.path_img + "img_nama/0.1s_"+ str(x) + "/*.jpg")
            pattern = "(.*?)_([0-9]+).jpg"
            m_list = []
            imgFile2 = []
            for i in imgFile:
                # print(i)
                m = re.search(pattern, i)
                n = m.group(1)
                m = m.group(2)
                # print(n)
                # print(m)
                m_list.append(m)
            m_list = sorted(m_list, key = int)

            for i in m_list:
                i = n + "_" + str(i) + ".jpg"
                # print(i)
                imgFile2.append(i)
            imgFileSum += len(imgFile2)
            # print(imgFileSum)
            sectionPlist = open(self.path_img + "section_positive_01s_" + str(x) + ".txt").readlines()
            # print(imgFile)
            for i in range(len(imgFile2) - 30):
                sum = 0
                P_in = 0
                #print("pi")
                if i % 30 == 0:
                    print(i)
                for file_list in imgFile2[0+i:30+i]:
                    # print(file_list)
                    flg, img, img_file_name = face_square_clips(self.cascade, file_list, self.m_size)
                    if flg == True:
                        sum += 0.1
                        # print(sum)
                for s in sectionPlist:
                    s = s.split("-")
                    # print(s[0])
                    if i == int(s[0]):
                        P_in += 1
                        # print(P_in)

                if P_in != 0 and sum >= 2: # default = 20
                    P_P += 1
                    print("P_P:{0}".format(P_P))
                elif P_in == 0 and sum < 2:
                    N_N += 1
                    # print("N_N:{0}".format(N_N))
                elif P_in != 0 and sum < 2:
                    P_N += 1
                    print("P_N:{0}".format(P_N))
                elif P_in == 0 and sum >= 2:
                    N_P += 1
                    print("N_P:{0}".format(N_P))
            # sum_smile_l.append(round(sum))
            # sum_smile_float.append(float(sum))
            # c_f = collections.Counter(sum_smile_float)
            # sum_smile_int.append(round(sum))
            # c_i = collections.Counter(sum_smile_int)
        result_d = {"ALL": imgFileSum - 120,"P_P": P_P, "P_N": P_N, "N_P": N_P, "N_N": N_N}
        for key, value in result_d.items():
            print("key:", key, "-- value:", str(value))
        # return sum_smile_int, c_i, sum_smile_float, c_f


    def create_section_positive(self):

        f = open(self.path_img + "section_positive_01s_4.txt", mode='w')
        f_n = open(self.path_img + "section_negative_01s_4.txt", mode='w')
        imgFile2 = []
        imgFile = glob.glob(self.path_img + "img_nama/0.1s_4/*.jpg")
        pattern = "(.*?)_([0-9]+).jpg"
        m_list = []
        for i in imgFile:
            # print(i)
            m = re.search(pattern, i)
            n = m.group(1)
            m = m.group(2)
            # print(n)
            # print(m)
            m_list.append(m)
        m_list = sorted(m_list, key = int)

        for i in m_list:
            i = n + "_" + str(i) + ".jpg"
            # print(i)
            imgFile2.append(i)

        # b = sorted(glob.glob(self.path_img + "img_nama/0.1s_2/*.jpg"))
        # c = sorted(glob.glob(self.path_img + "img_nama/0.1s_3/*.jpg"))
        # d = sorted(glob.glob(self.path_img + "img_nama/0.1s_4/*.jpg"))
        for i in range(len(imgFile2) - 30):
            sum = 0
            pinSection = 0
            for file_list in imgFile2[0+i:30+i]:
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


    def write_histgrum(self, ts_i, c_i, ts_f , c_f, flg):
        fp = FontProperties(fname = "/Users/okayama/Library/Fonts/ipaexg.ttf")
        fig = plt.figure()
        ax1 = fig.add_subplot(1,2,1)
        if flg == "time":
            c_v = [k for k in c.values()]
            c_k = [k for k in c]
            ax1.hist(time_s,bins=len(c_k))#int(max(s_s_l))
            ax1.set_xlabel(u"笑い秒/回", fontproperties = fp)
            ax1.set_ylabel(u"回数", fontproperties = fp)
            ax1.set_ylim(0,max(c_v)+1)
            ax1.set_title(u"笑い平均時間分布", fontproperties = fp)
        else:
            ax2 = fig.add_subplot(1,2,2)
            c_v_i = [k for k in c_i.values()]
            c_k_i = [k for k in c_i]
            ax1.hist(ts_i,bins=len(c_k_i))#int(max(s_s_l))
            ax1.set_xlabel(u"区間内笑い回数", fontproperties = fp)
            ax1.set_ylabel(u"回数", fontproperties = fp)
            ax1.set_ylim(0,max(c_v_i)+1)
            ax1.set_title(u"区間内笑い平均時間分布", fontproperties = fp)
            c_v_f = [k for k in c_f.values()]
            c_k_f = [k for k in c_f]
            ax2.hist(ts_f,bins=len(c_k_f))
            ax2.set_xlabel(u"区間内笑い回数", fontproperties = fp)
            ax2.set_ylabel(u"回数", fontproperties = fp)
            ax2.set_ylim(0,max(c_v_f)+1)
            ax2.set_title(u"区間内笑い平均時間分布", fontproperties = fp)
        plt.show()


    def hist_time(self):
        sum = 0
        time_smile_int = []
        time_smile_float = []
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
                    time_smile_int.append(round(sum))
                    time_smile_float.append(float(sum))
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
        c_int = collections.Counter(time_smile_int)
        c_float = collections.Counter(time_smile_float)
        # print(c)
        return time_smile_int , c_int, time_smile_float, c_float


if __name__ == "__main__":
    h = hist_smile()

    # ts_i, c_i, ts_f, c_f = h.sum_smile()#section
    # h.write_histgrum(ts_i, c_i, ts_f, c_f, "section")
    # h.create_section_positive()
    # time.sleep(5)
    h.sum_smile()

    # t_smile, c = h.hist_time()#time
    # h.write_histgrum(t_smile, "time", c)
