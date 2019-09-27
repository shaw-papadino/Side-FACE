import cv2

def switch_cam() :
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    if cap.isOpened() == False:
    	print("Not connected!")
    cap.set(3, 320)
    cap.set(4, 240)
    frame_count = 1
    print("If you want to resume, press the 'q' key")
    print("----------------------------------------")
    while True :
        ret, img = cap.read()
        cv2.imshow("img", img)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            print(frame_count)
            saveImgByTime("img/", img)
            print("If you want to resume, press the 'q' key")
            print("----------------------------------------")

        if cv2.waitKey(100) & 0xFF == ord('t'):
            break
