import numpy as np
import cv2, time

video_capture_1 = cv2.VideoCapture(0)
video_capture_2 = cv2.VideoCapture(1)
video_capture_3 = cv2.VideoCapture(3)

ret1, frame1 = video_capture_1.read()
height, width, layers = frame1.shape
resizeHeight = int(height/1.5)
resizeWidth = int(width/1.5)
before = cv2.resize(frame1, (resizeWidth, resizeHeight))

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

    after = resFrame1




    diff = cv2.subtract(before, after)

    grayscale = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    grayscale = 255 - grayscale

    ret,thresh = cv2.threshold(grayscale, 40, 255, cv2.THRESH_BINARY)

    blur = cv2.GaussianBlur(grayscale,(5,5),0)
    grayscale = cv2.medianBlur(grayscale, 5)

    adaptiveGaussThresh = cv2.adaptiveThreshold(grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 1)

    adaptiveGaussThresh = 255 - adaptiveGaussThresh

    kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,17))
    morphological = cv2.morphologyEx(adaptiveGaussThresh, cv2.MORPH_OPEN, kernelOpen)
    morphological = cv2.morphologyEx(morphological, cv2.MORPH_CLOSE, kernelClose)

    # contours, hierarchy = cv2.findContours(morphological, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnt = max(contours, key = cv2.contourArea)
    # lowest = tuple(cnt[cnt[:, :, 1].argmax()][0])
    # after = cv2.circle(after, lowest, radius=2, color=(0, 255, 0), thickness=-1)

    cv2.imshow('Contour', morphological)

    before = resFrame1










    # cv2.line(resFrame1, (int(resizeWidth/2), 0), (int(resizeWidth/2), resizeHeight), (255,0,255), 2)
    # cv2.line(resFrame2, (int(resizeWidth/2), 0), (int(resizeWidth/2), resizeHeight), (255,0,255), 2)
    # cv2.line(resFrame3, (int(resizeWidth/2), 0), (int(resizeWidth/2), resizeHeight), (255,0,255), 2)

    # horizontal = np.hstack([resFrame1, resFrame2, resFrame3])

    # cv2.imshow('Dartboard', horizontal)

    k = cv2.waitKey(500)
    if k == ord('q'):
        break
    if k == ord('s'):
        timestr = time.strftime('%d%m-%H%M%S')
        cv2.imwrite(timestr + 'frame1.jpg', frame1)
        cv2.imwrite(timestr + 'frame2.jpg', frame2)
        cv2.imwrite(timestr + 'frame3.jpg', frame3)

# When everything is done, release the capture
video_capture_1.release()
video_capture_2.release()
video_capture_3.release()
cv2.destroyAllWindows()
