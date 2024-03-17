import cv2
import time
import math
import numpy as np
import gameData
import display
from skimage.filters import threshold_otsu, threshold_sauvola, threshold_isodata, threshold_li, threshold_local, threshold_mean, threshold_minimum, threshold_niblack, threshold_triangle, threshold_yen
import matplotlib.pyplot as plt

# Camera properties
fov = 67.5
cameraWidth = 640

aCenter = display.find_center_angle(320, cameraWidth, fov)
bCenter = display.find_center_angle(320, cameraWidth, fov)
cCenter = display.find_center_angle(320, cameraWidth, fov)

aCameraX = -335*math.cos(math.radians(27))
aCameraY = 335*math.sin(math.radians(27))
bCameraX = 335*math.cos(math.radians(27))
bCameraY = 335*math.sin(math.radians(27))
cCameraX = 335*math.cos(math.radians(81))
cCameraY = -335*math.sin(math.radians(81))

def start_detection(admin, game, lock):
    while True:
        lock.acquire()
        mode = admin.mode
        lock.release()

        if mode == gameData.CameraMode.OFF:
            time.sleep(1)
        else:
            start_cameras(admin, game, lock)

def process_image(before, after, threshVal):
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

def find_dart_tip(processedImg):
    # Find the lowest y point of the max size contour
    contours, hierarchy = cv2.findContours(processedImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    val = 0

    if len(contours) == 0:
        val =  0
    else:
        cnt = max(contours, key = cv2.contourArea)
        size = cv2.contourArea(cnt)

        if size > 1500:
            val = "Hand"
        elif size < 100:
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

def start_cameras(admin, game, lock):
    video_capture_1 = cv2.VideoCapture(0)
    video_capture_2 = cv2.VideoCapture(2)
    video_capture_3 = cv2.VideoCapture(1)
    # video_capture_1 = cv2.VideoCapture('TBoutputA.avi')
    # video_capture_2 = cv2.VideoCapture('TBoutputC.avi')
    # video_capture_3 = cv2.VideoCapture('TBoutputB.avi')

    oldFrameA = None
    oldFrameB = None
    oldFrameC = None

    detectAgain = False

    # Get camera frame proportions
    _, sample = video_capture_1.read()
    height, width, _ = sample.shape
    resizeHeight = int(height/1.5)
    resizeWidth = int(width/1.5)
    croppedHeight = int(2*resizeHeight/5)

    while True:
        lock.acquire()
        mode = admin.mode
        center_line = admin.center_line
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

        if mode == gameData.CameraMode.OFF:
            break
        
        elif mode == gameData.CameraMode.ON:
            if center_line == True:
                cv2.line(croppedFrame1, (int(resizeWidth/2), 0), (int(resizeWidth/2), int(2*croppedHeight)), (0, 255, 0), thickness=1)
                cv2.line(croppedFrame2, (int(resizeWidth/2), 0), (int(resizeWidth/2), int(2*croppedHeight)), (0, 255, 0), thickness=1)
                cv2.line(croppedFrame3, (int(resizeWidth/2), 0), (int(resizeWidth/2), int(2*croppedHeight)), (0, 255, 0), thickness=1)

            lock.acquire()
            _, frameAData = cv2.imencode('.JPG', croppedFrame1)
            _, frameBData = cv2.imencode('.JPG', croppedFrame2)
            _, frameCData = cv2.imencode('.JPG', croppedFrame3)
            admin.frames[0] = frameAData.tobytes()
            admin.frames[1] = frameBData.tobytes()
            admin.frames[2] = frameCData.tobytes()
            lock.release()
        
        elif mode == gameData.CameraMode.POSITIONING or mode == gameData.CameraMode.GAME:
            if oldFrameA is not None:
                processedImageA, threshA = test_process_image(oldFrameA, croppedFrame1, 15)
                processedImageB, threshB = test_process_image(oldFrameB, croppedFrame2, 15)
                processedImageC, threshC = test_process_image(oldFrameC, croppedFrame3, 15)

                aX = find_dart_tip(processedImageA)
                bX = find_dart_tip(processedImageB)
                cX = find_dart_tip(processedImageC)
                existsA = find_dart_tip(threshA)
                existsB = find_dart_tip(threshB)
                existsC = find_dart_tip(threshC)

                if existsA == 0 and existsB == 0 and existsC == 0:
                    detectAgain = False
                elif detectAgain == False:
                    detectAgain = True
                elif detectAgain == True:
                    if existsA == "Hand" or existsB == "Hand" or existsC == "Hand":
                        lock.acquire()
                        if mode == gameData.CameraMode.GAME:
                            game.clear_board()
                        lock.release()
                    elif aX != "Hand" and bX != "Hand" and cX != "Hand":
                        aGrad, bGrad, cGrad = None, None, None
                        if aX != 0:
                            aGrad = display.angle_to_gradient(display.find_angle(aX[0], resizeWidth, fov) - aCenter - 27)
                        if bX != 0:
                            bGrad = display.angle_to_gradient(display.find_angle(bX[0], resizeWidth, fov) - bCenter + 27)
                        if cX != 0:
                            cGrad = display.rotate_gradient_90(display.angle_to_gradient(display.find_angle(cX[0], resizeWidth, fov) - cCenter + 9))

                        points = []

                        if aGrad is not None and bGrad is not None:
                            points.append(display.intersect(aCameraX, aCameraY, aGrad, bCameraX, bCameraY, bGrad))
                        if aGrad is not None and cGrad is not None:
                            points.append(display.intersect(aCameraX, aCameraY, aGrad, cCameraX, cCameraY, cGrad))
                        if bGrad is not None and cGrad is not None:
                            points.append(display.intersect(bCameraX, bCameraY, bGrad, cCameraX, cCameraY, cGrad))

                        if len(points) > 0:
                            xAvg = (sum([i[0] for i in points]))/len(points)
                            yAvg = (sum([i[1] for i in points]))/len(points)

                            dart_score = display.score_dart(xAvg, yAvg)

                            lock.acquire()
                            game.new_dart(dart_score)

                            if mode == gameData.CameraMode.GAME:
                                game.dart(dart_score)
                            lock.release()

                    detectAgain = False
        
            if oldFrameA is None or detectAgain == False:
                oldFrameA = croppedFrame1
                oldFrameB = croppedFrame2
                oldFrameC = croppedFrame3

        # Limit processing to 2 FPS
        # time.sleep(0.5)
        cv2.waitKey(250)

    # When everything is done, release the capture
    video_capture_1.release()
    video_capture_2.release()
    video_capture_3.release()























def test_process_image(before, after, thresh_val):
    diff = cv2.absdiff(before, after)
    grayscale = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blurred = cv2.medianBlur(grayscale, 3)

    # Normalise
    # norm_img1 = cv2.normalize(blurred, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    # norm_img1 = (255*norm_img1).astype(np.uint8)
    norm_img1 = blurred

    thresh = None

    # if option == 1:
    #     ret, thresh = cv2.threshold(norm_img1, 25, 255, cv2.THRESH_BINARY)
    # elif option == 2:
    #     triangle = threshold_triangle(norm_img1)
    #     ret, thresh = cv2.threshold(norm_img1, triangle, 255, cv2.THRESH_BINARY)
    # elif option == 3:
    #     yen = threshold_yen(norm_img1)
    #     ret, thresh = cv2.threshold(norm_img1, yen, 255, cv2.THRESH_BINARY)
    # elif option == 4:
    #     li = threshold_li(norm_img1)
    #     ret, thresh = cv2.threshold(norm_img1, li, 255, cv2.THRESH_BINARY)
    # elif option == 5:
    #     otsu = threshold_otsu(norm_img1)
    #     ret, thresh = cv2.threshold(norm_img1, otsu, 255, cv2.THRESH_BINARY)
    # elif option == 6:
    #     isodata = threshold_isodata(norm_img1)
    #     ret, thresh = cv2.threshold(norm_img1, isodata, 255, cv2.THRESH_BINARY)
    # elif option == 7:
    #     mean = threshold_mean(norm_img1)
    #     ret, thresh = cv2.threshold(norm_img1, mean, 255, cv2.THRESH_BINARY)
    # elif option == 8:
    #     local = threshold_local(norm_img1)
    #     ret, thresh = cv2.threshold(norm_img1, local, 255, cv2.THRESH_BINARY)

    # final = thresh

    triangle = threshold_triangle(norm_img1)
    ret, triangle = cv2.threshold(norm_img1, triangle, 255, cv2.THRESH_BINARY)
    yen = threshold_yen(norm_img1)
    ret, yen = cv2.threshold(norm_img1, yen, 255, cv2.THRESH_BINARY)
    li = threshold_li(norm_img1)
    ret, li = cv2.threshold(norm_img1, li, 255, cv2.THRESH_BINARY)

    combined = (triangle/2)+(yen/2)
    combined = cv2.convertScaleAbs(combined)
    ret, all = cv2.threshold(combined, 150, 255, cv2.THRESH_BINARY)

    thresh = all
    
    # edges = cv2.Canny(norm_img1,10,200)
    # ret, all = cv2.threshold(all, 101, 255, cv2.THRESH_BINARY)

    # Morphological operations to remove noise
    kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    morphological = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelOpen)
    final = cv2.morphologyEx(morphological, cv2.MORPH_CLOSE, kernelClose)

    # cv2.imwrite("im_before.jpg", before) 
    # cv2.imwrite("im_after.jpg", after)
    # cv2.imwrite("im_difference.jpg", diff)
    # cv2.imwrite("im_grayscale.jpg", grayscale) 
    # cv2.imwrite("im_blurred.jpg", blurred) 
    # cv2.imwrite("im_triangle.jpg", triangle) 
    # cv2.imwrite("im_yen.jpg", yen) 
    # cv2.imwrite("im_combined.jpg", all) 
    # cv2.imwrite("im_morphological.jpg", morphological) 
    # cv2.imwrite("im_final.jpg", final)

    # out = input("HI")

    ret, thresh = cv2.threshold(norm_img1, thresh_val, 255, cv2.THRESH_BINARY)
    thresh_morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelOpen)
    thresh_final = cv2.morphologyEx(thresh_morph, cv2.MORPH_CLOSE, kernelClose)

    return final, thresh_final








def test_all():
    modes = ["thresh","triangle","yen","li","otsu","isodata","mean","local"]

    for i in range(0, len(modes)):
        print(modes[i])
        test(i)

def test(mode):
    video_capture_1 = cv2.VideoCapture('AllA.avi')
    video_capture_2 = cv2.VideoCapture('AllB.avi')
    video_capture_3 = cv2.VideoCapture('AllC.avi')

    oldFrameA = None
    oldFrameB = None
    oldFrameC = None

    detectAgain = False

    actual = ['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20',
              'S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','S11','S12','S13','S14','S15','S16','S17','S18','S19','S20',
              'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D15','D16','D17','D18','D19','D20',
              'T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12','T13','T14','T15','T16','T17','T18','T19','T20',
              'S25','S25','S25','S25','D25','D25','D25','D25','0','0','0','0','0','0']

    # Get camera frame proportions
    _, sample = video_capture_1.read()
    height, width, _ = sample.shape
    # resizeHeight = int(height/1.5)
    # resizeWidth = int(width/1.5)
    resizeHeight = height
    resizeWidth = width
    # croppedHeight = int(resizeHeight/3)
    croppedHeight = 0

    total = 0
    count = 0
    correct = 0
    incorrect = 0
    false_positives = 0

    while correct+incorrect < 94:
        value = -1
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

        if oldFrameA is not None:
            processedImageA = test_process_image(oldFrameA, croppedFrame1, mode)
            processedImageB = test_process_image(oldFrameB, croppedFrame2, mode)
            processedImageC = test_process_image(oldFrameC, croppedFrame3, mode)

            aX = find_dart_tip(processedImageA)
            bX = find_dart_tip(processedImageB)
            cX = find_dart_tip(processedImageC)

            if aX == 0 and bX == 0 and cX == 0:
                detectAgain = False
            elif detectAgain == False:
                detectAgain = True
            elif detectAgain == True:
                if aX == "Hand" or bX == "Hand" or cX == "Hand":
                    pass
                elif aX != 0 and bX != 0 and cX != 0:                        
                    aGrad = display.angle_to_gradient(display.find_angle(aX[0], resizeWidth, fov) - aCenter - 27)
                    bGrad = display.angle_to_gradient(display.find_angle(bX[0], resizeWidth, fov) - bCenter + 27)
                    cGrad = display.rotate_gradient_90(display.angle_to_gradient(display.find_angle(cX[0], resizeWidth, fov) - cCenter + 9))

                    pointA = display.intersect(aCameraX, aCameraY, aGrad, bCameraX, bCameraY, bGrad)
                    pointB = display.intersect(bCameraX, bCameraY, bGrad, cCameraX, cCameraY, cGrad)
                    pointC = display.intersect(aCameraX, aCameraY, aGrad, cCameraX, cCameraY, cGrad)

                    xAvg = (pointA[0]+pointB[0]+pointC[0])/3
                    yAvg = (pointA[1]+pointB[1]+pointC[1])/3

                    dart_score = display.score_dart(xAvg, yAvg)

                    value = dart_score.to_string()

                detectAgain = False
    
        if oldFrameA is None or detectAgain == False:
            oldFrameA = croppedFrame1
            oldFrameB = croppedFrame2
            oldFrameC = croppedFrame3

        if total % 9 == 3:
            if value == actual[count]:
                correct += 1
            else:
                print(value, actual[count])
                incorrect += 1
            count += 1
        else:
            if value != -1:
                false_positives += 1
        total += 1

        # time.sleep(0.2)
    
    print(correct, "out of", correct+incorrect)
    print(correct/(correct+incorrect))
    print(false_positives, "false positives")

if __name__ == "__main__":
    test(1)