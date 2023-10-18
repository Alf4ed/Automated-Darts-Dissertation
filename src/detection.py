import cv2, numpy as np

before = cv2.imread('1710-190431frame1.jpg')
after = cv2.imread('1710-190447frame1.jpg')

before = cv2.imread('1710-190431frame2.jpg')
after = cv2.imread('1710-190447frame2.jpg')

before = cv2.imread('1710-190431frame3.jpg')
after = cv2.imread('1710-190447frame3.jpg')

diff = cv2.subtract(before, after)

grayscale = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(grayscale, 20, 255, cv2.THRESH_BINARY)

kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
morphological = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelOpen)
morphological = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernelClose)

# cv2.imshow('Before', before)
# cv2.imshow('After', after)
# cv2.imshow('Difference', diff)
# cv2.imshow('Grayscale', grayscale)
# cv2.imshow('Thresholding', thresh)
cv2.imshow('Morphological', morphological)

k = cv2.waitKey(0)