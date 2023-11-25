import cv2, numpy as np
from matplotlib import pyplot as plt
import os, re
from skimage import data, img_as_ubyte
from skimage.filters import threshold_isodata, threshold_li, threshold_minimum, threshold_yen, threshold_triangle, threshold_otsu
from display import *
import math

def findDartTip(before, after, go, threshVal, colour):
    diff = cv2.absdiff(before, after)
    grayscale = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blurred = cv2.medianBlur(grayscale, 5)

    # Normalise
    norm_img1 = cv2.normalize(blurred, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    norm_img1 = (255*norm_img1).astype(np.uint8)
    # inverted = 255 - norm_img1

    # # Thresholding operations
    ret, thresh = cv2.threshold(norm_img1, threshVal, 255, cv2.THRESH_BINARY)
    # ret3,otsuCV = cv2.threshold(norm_img1, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # adaptiveMeanThresh = cv2.adaptiveThreshold(inverted, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)
    # adaptiveGaussThresh = cv2.adaptiveThreshold(inverted, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)

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

    # thresh = isodata

    img = thresh

    # all = np.zeros(img.shape)
    # all = cv2.normalize(255 - adaptiveMeanThresh, all, 0, 25, cv2.NORM_MINMAX)\
    # all = cv2.normalize(yen, all, 0, 25, cv2.NORM_MINMAX)\
    #         + cv2.normalize(otsuCV, all, 0, 25, cv2.NORM_MINMAX)\
    #         + cv2.normalize(min, all, 0, 25, cv2.NORM_MINMAX)\
    #         + cv2.normalize(otsu, all, 0, 25, cv2.NORM_MINMAX)\
    #         + cv2.normalize(isodata, all, 0, 25, cv2.NORM_MINMAX)\
    #         + cv2.normalize(thresh, all, 0, 25, cv2.NORM_MINMAX)\
    #         + cv2.normalize(li, all, 0, 25, cv2.NORM_MINMAX)
            # + cv2.normalize(255 - adaptiveGaussThresh, all, 0, 25, cv2.NORM_MINMAX)\
            # + cv2.normalize(triangle, all, 0, 25, cv2.NORM_MINMAX)\
            

    # ret, all = cv2.threshold(all, 101, 255, cv2.THRESH_BINARY)
    all = thresh

    # Morphological operations to remove noise
    kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,7))
    morphological = cv2.morphologyEx(all, cv2.MORPH_OPEN, kernelOpen)
    final = cv2.morphologyEx(morphological, cv2.MORPH_CLOSE, kernelClose)
    out = final
    # final = thresh

    # Find the lowest y point of the max size contour
    contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key = cv2.contourArea)

    blank = np.zeros(img.shape, dtype=np.uint8)

    rows,cols = img.shape[:2]
    [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
    lefty = int(((-x*vy/vx) + y)[0])
    righty = int((((cols-x)*vy/vx)+y)[0])
    cv2.line(blank,(cols-1,righty),(0,lefty),(255,255,255),15)

    blank = cv2.bitwise_and(blank, final)
    y, x = np.nonzero(blank)
    y = y[-1]
    x = x[-1]
    
    # lowest = tuple(cnt[cnt[:, :, 1].argmax()][0])
    final = cv2.cvtColor(after, cv2.COLOR_BGR2RGB)
    final = cv2.circle(after, (x,y), radius=2, color=colour, thickness=-1)

    # Plot the results
    ax1 = plt.subplot(2, 4, 2+(2*go))
    ax1.imshow(cv2.cvtColor(after, cv2.COLOR_BGR2RGB))
    ax1.title.set_text('After')

    # ax2 = plt.subplot(2, 4, 3+(2*go), sharex=ax1, sharey=ax1)
    # ax2.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
    # ax2.title.set_text('Thresh')

    ax3 = plt.subplot(2, 4, 3+(2*go), sharex=ax1, sharey=ax1)
    # ax3.imshow(cv2.cvtColor(final, cv2.COLOR_BGR2RGB))
    ax3.imshow(out)
    ax3.title.set_text('Final')

    # ax4 = plt.subplot(2, 2, 3, sharex=ax1, sharey=ax1)
    # ax4.imshow(cv2.cvtColor(blank, cv2.COLOR_BGR2RGB))
    # ax4.title.set_text('Line')

    # ax5 = plt.subplot(3, 5, 5, sharex=ax1, sharey=ax1)
    # ax5.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
    # ax5.title.set_text('Global')

    # ax6 = plt.subplot(3, 5, 6, sharex=ax1, sharey=ax1)
    # ax6.imshow(cv2.cvtColor(otsuCV, cv2.COLOR_BGR2RGB))
    # ax6.title.set_text('OtsuCV')

    # ax7 = plt.subplot(3, 5, 7, sharex=ax1, sharey=ax1)
    # ax7.imshow(cv2.cvtColor(255 - adaptiveMeanThresh, cv2.COLOR_BGR2RGB))
    # ax7.title.set_text('Mean')

    # ax8 = plt.subplot(3, 5, 8, sharex=ax1, sharey=ax1)
    # ax8.imshow(cv2.cvtColor(255 - adaptiveGaussThresh, cv2.COLOR_BGR2RGB))
    # ax8.title.set_text('Gaussian')

    # ax10 = plt.subplot(2, 4, 3+(2*go), sharex=ax1, sharey=ax1)
    # ax10.imshow(cv2.cvtColor(norm_img1, cv2.COLOR_BGR2RGB))
    # ax10.title.set_text('Normalised')

    # ax10 = plt.subplot(3, 5, 10, sharex=ax1, sharey=ax1)
    # ax10.imshow(cv2.cvtColor(triangle, cv2.COLOR_BGR2RGB))
    # ax10.title.set_text('Triangle')

    # ax10 = plt.subplot(3, 5, 11, sharex=ax1, sharey=ax1)
    # ax10.imshow(cv2.cvtColor(yen, cv2.COLOR_BGR2RGB))
    # ax10.title.set_text('Yen')

    # ax11 = plt.subplot(3, 5, 12, sharex=ax1, sharey=ax1)
    # ax11.imshow(cv2.cvtColor(li, cv2.COLOR_BGR2RGB))
    # ax11.title.set_text('Li')

    # ax10 = plt.subplot(3, 5, 13, sharex=ax1, sharey=ax1)
    # ax10.imshow(cv2.cvtColor(min, cv2.COLOR_BGR2RGB))
    # ax10.title.set_text('Min')

    # ax10 = plt.subplot(2, 2, 4, sharex=ax1, sharey=ax1)
    # ax10.imshow(cv2.cvtColor(all, cv2.COLOR_BGR2RGB))
    # ax10.title.set_text('All')

    # ax11 = plt.subplot(3, 5, 15, sharex=ax1, sharey=ax1)
    # ax11.imshow(cv2.cvtColor(isodata, cv2.COLOR_BGR2RGB))
    # ax11.title.set_text('Isodata')

    # ax1.set_xlim([x-60, x+60])
    # ax1.set_ylim([y+50, max(0,y-300)])

    # plt.show()

    return(x, y)

fov = 70

aCenter = findCenterAngle(319, 640, fov)
bCenter = findCenterAngle(326, 640, fov)
cCenter = findCenterAngle(327, 640, fov)

# print(findAngle(132, 640, fov)-aCenter)
# print(findAngle(436, 640, fov)-aCenter)
# print(findAngle(532, 640, fov)-aCenter)

aCameraX = -(335)*math.sin(math.radians(13.2))
aCameraY = -(335)*math.cos(math.radians(13.2))
bCameraX = -(335)*math.sin(math.radians(52.8))
bCameraY = (335)*math.cos(math.radians(52.8))
cCameraX = (335)*math.sin(math.radians(27.5))
cCameraY = (335)*math.cos(math.radians(27.5))

rootdir = 'C:/Users/alfre/Documents/cs310/src/dataset/'

for subdir, dirs, files in os.walk(rootdir):
    if re.search("25", subdir):
        for file in files:
            
            if re.search("A", file) is not None:
                print(subdir)
                board = Dartboard(subdir)
                board.drawPoint(aCameraX, aCameraY, color='r')
                board.drawPoint(bCameraX, bCameraY, color='g')
                board.drawPoint(cCameraX, cCameraY, color='b')

                aBefore = cv2.imread('C:/Users/alfre/Documents/cs310/src/dataset/empty125/_A.jpg')
                bBefore = cv2.imread('C:/Users/alfre/Documents/cs310/src/dataset/empty125/_B.jpg')
                cBefore = cv2.imread('C:/Users/alfre/Documents/cs310/src/dataset/empty125/_C.jpg')

                aAfter = cv2.imread(os.path.join(subdir, '_A.jpg'))
                bAfter = cv2.imread(os.path.join(subdir, '_B.jpg'))
                cAfter = cv2.imread(os.path.join(subdir, '_C.jpg'))

                aX, _ = findDartTip(aBefore, aAfter, 0, 65, (0, 0, 255))
                bX, _ = findDartTip(bBefore, bAfter, 1, 50, (0, 255, 0))
                cX, _ = findDartTip(cBefore, cAfter, 2, 50, (255, 0, 0))

                aGrad = angleToGradient(findAngle(aX, 640, fov) - aCenter + 68)
                bGrad = angleToGradient(findAngle(bX, 640, fov) - bCenter - 46)
                cGrad = angleToGradient(findAngle(cX, 640, fov) - cCenter - 127)

                board.drawLine(aCameraX, aCameraY, aGrad, color='r')
                board.drawLine(bCameraX, bCameraY, bGrad, color='g')
                board.drawLine(cCameraX, cCameraY, cGrad, color='b')

                x1, y1 = board.intersect(aCameraX, aCameraY, aGrad, bCameraX, bCameraY, bGrad)
                x2, y2 = board.intersect(bCameraX, bCameraY, bGrad, cCameraX, cCameraY, cGrad)
                x3, y3 = board.intersect(aCameraX, aCameraY, aGrad, cCameraX, cCameraY, cGrad)

                avX = (x1+x2+x3)/3
                avY = (y1+y2+y3)/3

                board.drawPoint(avX, avY, 'cyan')

                r, theta = board.cartesianToPolar(avX, avY)
                score = board.score(r, theta)

                print(score)

                # if re.search(score, subdir) is None:
                board.show()

                board.close()