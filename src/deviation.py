import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats as st

heat = np.zeros((460, 460))

# board = Dartboard('Deviation')
img = cv2.imread('../images/board.png')

fig, ax = plt.subplots()
ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), extent=[-230, 230, 230, -230])

def cartesianToPolar(x, y):
    r = math.sqrt(x**2 + y**2)

    if x == 0 and y >= 0:
        theta = math.pi/2
    elif x == 0 and y < 0:
        theta = math.pi*3/2
    elif x > 0:
        theta = math.atan(y/x)
    else:
        theta = math.atan(y/x) + math.pi
    
    return (r, theta)

def score(r, theta):
    sectors = [3,17,2,15,10,6,13,4,18,1,20,5,12,9,14,11,8,16,7,19]
    sector = math.floor(((theta)/(2*math.pi))*20 + 1/2)
    value = int(sectors[sector])

    if 170 < r:
        return 0
    elif 162 < r:
        return 2*value
    elif 107 < r:
        return value
    elif 99 < r:
        return 3*value
    elif 16 < r:
        return value
    elif 6.35 < r:
        return 25
    else:
        return 50

std = 50
middle = 230

probabilities = np.zeros((460, 460))
scores = np.zeros((460, 460))

from statistics import NormalDist

for i in range(-230, 230):
    for j in range(-230, 230):
        
        r, theta = cartesianToPolar(i+0.5, j+0.5)
        scores[i+230][j+230] = score(r, theta)

        lowerDist = math.sqrt(abs(i)**2 + abs(j)**2)
        upperDist = math.sqrt(abs(i+1)**2 + abs(j+1)**2)

        lower = NormalDist(0, 50).cdf(math.sqrt(abs(i)**2 + abs(j)**2))
        upper = NormalDist(0, 50).cdf(math.sqrt((abs(i)+1)**2 + (abs(j)+1)**2))

        probabilities[i+230][j+230] = upper-lower





for i in range(0, 460):
    for j in range(0, 460):
        
        blank = np.zeros((460, 460))

        # left = max(0, 230-i)
        # right = min(460, 460-i)
        # top = max(0, 230-j)
        # bottom = min(460, 460-j)

        # overlap = probabilities[left:right, top:bottom]

        # rowLeft = max(0, i-230)
        # rowRight = min(460, 230+i)
        # columnTop = max(0, j-230)
        # columnBottom = min(460, 230+j)

        # blank[rowLeft:rowRight, columnTop:columnBottom] = overlap

        # products = np.multiply(blank, scores)
        # total = np.sum(products)

        heat[i][j] = 2

ax.imshow(scores, alpha=1, cmap='hot', extent=[-230, 230, 230, -230])

plt.show()