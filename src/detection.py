import cv2
import time
import math
import numpy as np
import gamedata
import display
from skimage.filters import threshold_otsu, try_all_threshold
import matplotlib.pyplot as plt

# Camera properties
fov = 67.5
cameraWidth = 640

aCenter = display.findCenterAngle(320, cameraWidth, fov)
bCenter = display.findCenterAngle(320, cameraWidth, fov)
cCenter = display.findCenterAngle(320, cameraWidth, fov)

aCameraX = -335*math.cos(math.radians(27))
aCameraY = 335*math.sin(math.radians(27))
bCameraX = 335*math.cos(math.radians(27))
bCameraY = 335*math.sin(math.radians(27))
cCameraX = 335*math.cos(math.radians(81))
cCameraY = -335*math.sin(math.radians(81))

def startDetection(admin, game, lock):

    while True:
        lock.acquire()
        mode = admin.mode
        lock.release()

        if mode == gamedata.Mode.CAMOFF:
            time.sleep(1)
        else:
            startCameras(admin, game, lock)

def processImage(before, after, threshVal):
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

    # edges = cv2.Canny(norm_img1,10,200)

    # ret, all = cv2.threshold(all, 101, 255, cv2.THRESH_BINARY)

    # Morphological operations to remove noise
    kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    morphological = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelOpen)
    final = cv2.morphologyEx(morphological, cv2.MORPH_CLOSE, kernelClose)

    return final

def findDartTip(processedImg):
    # Find the lowest y point of the max size contour
    contours, hierarchy = cv2.findContours(processedImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    val = 0

    if len(contours) == 0:
        val =  0
    else:
        cnt = max(contours, key = cv2.contourArea)
        size = cv2.contourArea(cnt)

        if size > 1000:
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

    return val

def startCameras(admin, game, lock):
    # video_capture_1 = cv2.VideoCapture(0)
    # video_capture_2 = cv2.VideoCapture(3)
    # video_capture_3 = cv2.VideoCapture(1)
    video_capture_1 = cv2.VideoCapture('ToutputA.avi')
    video_capture_2 = cv2.VideoCapture('ToutputC.avi')
    video_capture_3 = cv2.VideoCapture('ToutputB.avi')

    oldFrameA = None
    oldFrameB = None
    oldFrameC = None

    detectAgain = False

    # Get camera frame proportions
    _, sample = video_capture_1.read()
    height, width, _ = sample.shape
    resizeHeight = int(height/1.5)
    resizeWidth = int(width/1.5)
    croppedHeight = int(resizeHeight/3)

    while True:
        lock.acquire()
        mode = admin.mode
        centerLine = admin.centerLine
        lock.release()

        # Capture frame-by-frame
        _, frame1 = video_capture_1.read()
        _, frame2 = video_capture_2.read()
        _, frame3 = video_capture_3.read()

        # Resize the images to reduce computational complexity
        resFrame1 = cv2.resize(frame1, (resizeWidth, resizeHeight))
        resFrame2 = cv2.resize(frame2, (resizeWidth, resizeHeight))
        resFrame3 = cv2.resize(frame3, (resizeWidth, resizeHeight))

        # Crop the images to show only the board
        croppedFrame1 = resFrame1[croppedHeight:resizeHeight, 0:resizeWidth]
        croppedFrame2 = resFrame2[croppedHeight:resizeHeight, 0:resizeWidth]
        croppedFrame3 = resFrame3[croppedHeight:resizeHeight, 0:resizeWidth]

        if mode == gamedata.Mode.CAMOFF:
            break
        
        if centerLine == True:
            cv2.line(croppedFrame1, (int(resizeWidth/2), 0), (int(resizeWidth/2), int(2*croppedHeight)), (0, 255, 0), thickness=1)
            cv2.line(croppedFrame2, (int(resizeWidth/2), 0), (int(resizeWidth/2), int(2*croppedHeight)), (0, 255, 0), thickness=1)
            cv2.line(croppedFrame3, (int(resizeWidth/2), 0), (int(resizeWidth/2), int(2*croppedHeight)), (0, 255, 0), thickness=1)
        
        if mode == gamedata.Mode.CAMON:
            lock.acquire()
            _, frameAData = cv2.imencode('.JPG', croppedFrame1)
            _, frameBData = cv2.imencode('.JPG', croppedFrame2)
            _, frameCData = cv2.imencode('.JPG', croppedFrame3)
            admin.frames[0] = frameAData.tobytes()
            admin.frames[1] = frameBData.tobytes()
            admin.frames[2] = frameCData.tobytes()
            lock.release()
        
        if oldFrameA is not None:
            processedImageA = processImage(oldFrameA, croppedFrame1, 25)
            processedImageB = processImage(oldFrameB, croppedFrame2, 25)
            processedImageC = processImage(oldFrameC, croppedFrame3, 25)

            aX = findDartTip(processedImageA)
            bX = findDartTip(processedImageB)
            cX = findDartTip(processedImageC)

            if aX == 0 and bX == 0 and cX == 0:
                detectAgain = False
            elif detectAgain == False:
                detectAgain = True
            elif detectAgain == True:
                if aX == "Hand" or bX == "Hand" or cX == "Hand":
                    # sync('Changeover')
                    pass
                elif aX != 0 and bX != 0 and cX != 0:
                    if mode == gamedata.Mode.PROCESSING:
                        showA = cv2.cvtColor(processedImageA, cv2.COLOR_GRAY2BGR )
                        showB = cv2.cvtColor(processedImageB, cv2.COLOR_GRAY2BGR )
                        showC = cv2.cvtColor(processedImageC, cv2.COLOR_GRAY2BGR )
                        lock.acquire()
                        _, frameAData = cv2.imencode('.JPG', showA)
                        _, frameBData = cv2.imencode('.JPG', showB)
                        _, frameCData = cv2.imencode('.JPG', showC)
                        admin.frames[0] = frameAData.tobytes()
                        admin.frames[1] = frameBData.tobytes()
                        admin.frames[2] = frameCData.tobytes()
                        lock.release()
                    
                    aGrad = display.angleToGradient(display.findAngle(aX[0], resizeWidth, fov) - aCenter - 27)
                    bGrad = display.angleToGradient(display.findAngle(bX[0], resizeWidth, fov) - bCenter + 27)
                    cGrad = display.rotateGradient90(display.angleToGradient(display.findAngle(cX[0], resizeWidth, fov) - cCenter + 9))

                    pointA = display.intersect(aCameraX, aCameraY, aGrad, bCameraX, bCameraY, bGrad)
                    pointB = display.intersect(bCameraX, bCameraY, bGrad, cCameraX, cCameraY, cGrad)
                    pointC = display.intersect(aCameraX, aCameraY, aGrad, cCameraX, cCameraY, cGrad)

                    xAvg = (pointA[0]+pointB[0]+pointC[0])/3
                    yAvg = (pointA[1]+pointB[1]+pointC[1])/3

                    r, theta = display.cartesianToPolar(xAvg, yAvg)
                    score = display.score(r, theta)

                    lock.acquire()
                    admin.history.append((xAvg, yAvg, score[0]))
                    admin.toShow.append((xAvg, yAvg, score[0]))
                    lock.release()

                detectAgain = False
        
        if oldFrameA is None or detectAgain == False:
            oldFrameA = croppedFrame1
            oldFrameB = croppedFrame2
            oldFrameC = croppedFrame3

        # Limit processing to 2 FPS
        time.sleep(0.75)
        # cv2.waitKey(250)

    # When everything is done, release the capture
    video_capture_1.release()
    video_capture_2.release()
    video_capture_3.release()