import cv2
from skimage import feature
from matplotlib import pyplot as plt

points = 22
radius = 8


file_name = '/Users/okayamashoya/side_face_test1.png'
bgr_img = cv2.imread(file_name)
gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

# compute the Local Binary Pattern representation of the image
lbp = feature.local_binary_pattern(gray_img, points, radius, method="uniform")
plt.hist(lbp.ravel(), bins=points+2, range=(0, points+2), color='red', alpha=0.3)

file_name = '/Users/okayamashoya/side_face_test2.png'
bgr_img = cv2.imread(file_name)
gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

# compute the Local Binary Pattern representation of the image
lbp = feature.local_binary_pattern(gray_img, points, radius, method="uniform")
plt.hist(lbp.ravel(), bins=points+2, range=(0, points+2), color='blue', alpha=0.3)
plt.show()
