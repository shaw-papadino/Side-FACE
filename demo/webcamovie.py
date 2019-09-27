import datetime
import os

from side_smilecam_threding import main



now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
mov_path = now + ".avi"
# h_path = now + ".h264"
filepath = "./"
# side_path = filepath + "sideye/"
file_path = filepath + "fisheye/"
if not os.path.exists(file_path):
	os.mkdir(file_path)

main(file_path, mov_path)
