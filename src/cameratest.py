import numpy as np
import cv2, os

video_capture_1 = cv2.VideoCapture(0)
video_capture_2 = cv2.VideoCapture(1)
video_capture_3 = cv2.VideoCapture(2)

ret1, frame1 = video_capture_1.read()
height, width, layers = frame1.shape
resizeHeight = int(height/1.5)
resizeWidth = int(width/1.5)
before = cv2.resize(frame1, (resizeWidth, resizeHeight))

number = 25
region = ['S1', 'S2', 'S3', 'S4', 'D1', 'D2', 'D3', 'D4', 'empty1', 'empty2', 'calib1', 'calib2', 'calib3']

while True:
    # Capture frame-by-frame
    ret1, frame1 = video_capture_1.read()
    ret2, frame2 = video_capture_2.read()
    ret3, frame3 = video_capture_3.read()

    height, width, layers = frame1.shape
    resizeHeight = int(height/1.5)
    resizeWidth = int(width/1.5)

    resFrame1 = cv2.resize(frame1, (resizeWidth, resizeHeight))
    resFrame2 = cv2.resize(frame2, (resizeWidth, resizeHeight))
    resFrame3 = cv2.resize(frame3, (resizeWidth, resizeHeight))

    

    # cv2.line(resFrame1, (int(resizeWidth/2), 0), (int(resizeWidth/2), resizeHeight), (255,0,255), 2)
    # cv2.line(resFrame2, (int(resizeWidth/2), 0), (int(resizeWidth/2), resizeHeight), (255,0,255), 2)
    # cv2.line(resFrame3, (int(resizeWidth/2), 0), (int(resizeWidth/2), resizeHeight), (255,0,255), 2)

    horizontal = np.hstack([resFrame1, resFrame2, resFrame3])

    cv2.imshow('Dartboard', horizontal)

    k = cv2.waitKey(500)
    if k == ord('q'):
        break
    if k == ord('s'):

        reg = (number-25)
        num = 25

        os.mkdir('dataset/'+region[reg]+str(num))

        cv2.imwrite('dataset/'+region[reg]+str(num)+'/A.jpg', frame1)
        cv2.imwrite('dataset/'+region[reg]+str(num)+'/B.jpg', frame2)
        cv2.imwrite('dataset/'+region[reg]+str(num)+'/C.jpg', frame3)

        print(region[reg]+str(num))
        number += 1

# When everything is done, release the capture
video_capture_1.release()
video_capture_2.release()
video_capture_3.release()
cv2.destroyAllWindows()
