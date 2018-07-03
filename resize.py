import cv2
import os
import glob

path_img = "./201804280930/"


p_list = path_img + "positive.dat"
file = open('positive1.dat', 'w')
P_f = open(p_list, 'r')
P_l = P_f.readlines()
file_lists = glob.glob("./img/*.jpg")
# p_king_width = 2000
# p_king_height = 2000

for positive_img in P_l:
    p_split = positive_img.split()
    x1 = int(p_split[2]) // 2
    y1 = int(p_split[3]) // 2
    x2 = int(p_split[4]) // 2
    y2 = int(p_split[5]) // 2
# p_split[2] = str(int(p_split[2]) // 2)
# p_split[3] = str(int(p_split[3]) // 2)
# p_split[4] = str(int(p_split[4]) // 2)
# p_split[5] = str(int(p_split[5]) // 2)
    string = p_split[0] + " 1 " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + "\n"
    file.write(string)
# print(file_lists)
# 
# for file_list in file_lists:
#     img = cv2.imread(file_list, cv2.IMREAD_COLOR)
#     #print(img)
#     orgHeight, orgWidth = img.shape[:2]
#     #print(orgWidth)
#     #print(orgHeight)
#     size = (orgWidth//2, orgHeight//2)
#     #print(size)
#     f_name = os.path.splitext(os.path.basename(file_list))[0]
#     #Create Half Size Image
#     #halfImg = cv2.resize(img, (orgHeight / 2, orgWidth / 2))
#     halfImg = cv2.resize(img, size)
#
#     cv2.imwrite(path_img  + "img/" + f_name + ".jpg", halfImg)
#     p_current_width = int(p_split[4]) - int(p_split[2])
#     p_current_height = int(p_split[5]) - int(p_split[3])
#     if p_current_width < p_king_width and p_current_height < p_king_height :
#         p_king_width = p_current_width
#         p_king_height = p_current_height
# print(p_king_width)
# print(p_king_height)
