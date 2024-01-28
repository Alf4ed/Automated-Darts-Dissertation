import cv2, numpy as np
from matplotlib import pyplot as plt
import os, re
from skimage.filters import threshold_isodata, threshold_li, threshold_minimum, threshold_yen, threshold_triangle, threshold_otsu
from display import *
import math, time

def findDartTip(before, after, threshVal):
    diff = cv2.absdiff(before, after)
    grayscale = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blurred = cv2.medianBlur(grayscale, 3)

    # Normalise
    # norm_img1 = cv2.normalize(blurred, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    # norm_img1 = (255*norm_img1).astype(np.uint8)
    norm_img1 = blurred

    # # Thresholding operations
    ret, thresh = cv2.threshold(norm_img1, threshVal, 255, cv2.THRESH_BINARY)
    # ret3,otsuCV = cv2.threshold(norm_img1, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # triangle = threshold_triangle(norm_img1)
    # yen = threshold_yen(norm_img1)
    # li = threshold_li(norm_img1)
    # min = threshold_minimum(norm_img1)
    # otsu = threshold_otsu(norm_img1)
    # isodata = threshold_isodata(norm_img1)
    # ret, triangle = cv2.threshold(norm_img1, triangle, 255, cv2.THRESH_BINARY)
    # ret, yen = cv2.threshold(norm_img1, yen, 255, cv2.THRESH_BINARY)
    # ret, li = cv2.threshold(norm_img1, li, 255, cv2.THRESH_BINARY)
    # ret, min = cv2.threshold(norm_img1, min, 255, cv2.THRESH_BINARY)
    # ret, otsu = cv2.threshold(norm_img1, otsu, 255, cv2.THRESH_BINARY)
    # ret, isodata = cv2.threshold(norm_img1, isodata, 255, cv2.THRESH_BINARY)

    # ret, all = cv2.threshold(all, 101, 255, cv2.THRESH_BINARY)

    # Morphological operations to remove noise
    kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    morphological = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelOpen)
    final = cv2.morphologyEx(morphological, cv2.MORPH_CLOSE, kernelClose)

    # Find the lowest y point of the max size contour
    contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    val = 0

    if len(contours) == 0:
        val =  0
    else:
        cnt = max(contours, key = cv2.contourArea)
        size = cv2.contourArea(cnt)

        if size > 3000:
            val = "Hand"
        elif size < 25:
            val =  0
        else:
            val =  tuple(cnt[cnt[:, :, 1].argmax()][0])

    # blank = np.zeros(img.shape, dtype=np.uint8)

    # rows,cols = img.shape[:2]
    # [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
    # lefty = int(((-x*vy/vx) + y)[0])
    # righty = int((((cols-x)*vy/vx)+y)[0])
    # cv2.line(blank,(cols-1,righty),(0,lefty),(255,255,255),15)

    # blank = cv2.bitwise_and(blank, final)
    # y, x = np.nonzero(blank)
    # y = y[-1]
    # x = x[-1]

    return cv2.cvtColor(final, cv2.COLOR_GRAY2BGR ), val

fov = 67.5

aCenter = findCenterAngle(320, 640, fov)
bCenter = findCenterAngle(320, 640, fov)
cCenter = findCenterAngle(320, 640, fov)

aCameraX = -335*math.cos(math.radians(27))
aCameraY = 335*math.sin(math.radians(27))

bCameraX = 335*math.cos(math.radians(27))
bCameraY = 335*math.sin(math.radians(27))

cCameraX = 335*math.cos(math.radians(81))
cCameraY = -335*math.sin(math.radians(81))

# board = Dartboard('Darboard')

# board.drawPoint(aCameraX, aCameraY, 'r')
# board.drawPoint(bCameraX, bCameraY, 'g')
# board.drawPoint(cCameraX, cCameraY, 'b')

# board.show()

video_capture_1 = cv2.VideoCapture(2)
video_capture_2 = cv2.VideoCapture(3)
video_capture_3 = cv2.VideoCapture(1)

oldFrameA = None
oldFrameB = None
oldFrameC = None

detectAgain = False

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

    resFrame1 = resFrame1[int(resizeHeight/3):resizeHeight, 0:resizeWidth]
    resFrame2 = resFrame2[int(resizeHeight/3):resizeHeight, 0:resizeWidth]
    resFrame3 = resFrame3[int(resizeHeight/3):resizeHeight, 0:resizeWidth]

    if oldFrameA is not None:
        aImg, aX = findDartTip(oldFrameA, resFrame1, 20)
        bImg, bX = findDartTip(oldFrameB, resFrame2, 20)
        cImg, cX = findDartTip(oldFrameC, resFrame3, 20)

        if aX == 0 and bX == 0 and cX == 0:
            detectAgain = False
        elif detectAgain == False:
            detectAgain = True
        elif detectAgain == True:
            if aX == "Hand" or bX == "Hand" or cX == "Hand":
                print("CHANGEOVER")
            else:
                guess = Dartboard("Dartboard")
                guess.drawPoint(aCameraX, aCameraY, color='r')
                guess.drawPoint(bCameraX, bCameraY, color='g')
                guess.drawPoint(cCameraX, cCameraY, color='b')

                aGrad = angleToGradient(findAngle(aX[0], resizeWidth, fov) - aCenter - 27)
                bGrad = angleToGradient(findAngle(bX[0], resizeWidth, fov) - bCenter + 27)
                cGrad = rotateGradient90(angleToGradient(findAngle(cX[0], resizeWidth, fov) - cCenter + 9))

                guess.drawLine(aCameraX, aCameraY, aGrad, color='r')
                guess.drawLine(bCameraX, bCameraY, bGrad, color='g')
                guess.drawLine(cCameraX, cCameraY, cGrad, color='b')

                pointA = guess.intersect(aCameraX, aCameraY, aGrad, bCameraX, bCameraY, bGrad)
                pointB = guess.intersect(bCameraX, bCameraY, bGrad, cCameraX, cCameraY, cGrad)
                pointC = guess.intersect(aCameraX, aCameraY, aGrad, cCameraX, cCameraY, cGrad)

                xAvg = (pointA[0]+pointB[0]+pointC[0])/3
                yAvg = (pointA[1]+pointB[1]+pointC[1])/3

                r, theta = guess.cartesianToPolar(xAvg, yAvg)

                print(guess.score(r, theta))

                guess.close()

            detectAgain = False

        imageA = resFrame1.copy()
        imageB = resFrame2.copy()
        imageC = resFrame3.copy()

        if type(aX) == tuple and type(bX) == tuple and type(cX) == tuple:
            imageA = cv2.circle(imageA, aX, 5, (255, 0, 0), -1)
            imageB = cv2.circle(imageB, bX, 5, (255, 0, 0), -1)
            imageC = cv2.circle(imageC, cX, 5, (255, 0, 0), -1)

        processed = np.hstack([aImg, bImg, cImg])
        horizontal = np.hstack([imageA, imageB, imageC])

        all = np.vstack([horizontal, processed])
        cv2.imshow('Dartboard', all)
    
    if oldFrameA is None or detectAgain == False:
        oldFrameA = resFrame1
        oldFrameB = resFrame2
        oldFrameC = resFrame3

    k = cv2.waitKey(500)
    if k == ord('q'):
        break

# When everything is done, release the capture
video_capture_1.release()
video_capture_2.release()
video_capture_3.release()
cv2.destroyAllWindows()

