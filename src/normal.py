import numpy as np
from scipy import signal
from scipy.stats import skewnorm
import matplotlib.pyplot as plt
import math
from display import cartesianToPolar

# def cartesianToPolar(x, y):
#     r = math.sqrt(x**2 + y**2)

#     if x == 0 and y >= 0:
#         theta = math.pi/2
#     elif x == 0 and y < 0:
#         theta = math.pi*3/2
#     elif x > 0:
#         theta = math.atan(y/x)
#     else:
#         theta = math.atan(y/x) + math.pi
    
#     return (r, theta)

def scoreProb(x, y, check, checkout=False):

    r, theta = cartesianToPolar(x, y)

    sectors = [3,17,2,15,10,6,13,4,18,1,20,5,12,9,14,11,8,16,7,19]
    sector = math.floor(((theta)/(2*math.pi))*20 + 1/2)
    value = int(sectors[sector])

    returnval = 0

    if r <= 6.35:
        returnval = 50
    elif r <= 16 and not checkout:
        returnval = 25
    elif 170 < r:
        returnval = 0
    elif 162 < r:
        returnval = 2*value
    elif 107 < r and not checkout:
        returnval = value
    elif 99 < r and not checkout:
        returnval = 3*value
    elif 16 < r and not checkout:
        returnval = value

    if returnval == check:
        return 1
    else:
        return 0
    
##########################################################################################################################

def createKernel(size, dataX=None, dataY=None):
    x, y = [], []

    if dataX is None or dataY is None:
        ax, locx, scalex = 0, 0, 25
        ay, locy, scaley = 0, 0, 25
    else:
        # Estimate distribution
        ax, locx, scalex = skewnorm.fit(dataX)
        ay, locy, scaley = skewnorm.fit(dataY)

    skewnorm_dist_x = skewnorm(ax, locx, scalex)
    skewnorm_dist_y = skewnorm(ay, locy, scaley)

    for i in range(-math.floor(size/2), math.ceil(size/2)):
        leftx = skewnorm_dist_x.cdf(i-0.5)
        rightx = skewnorm_dist_x.cdf(i+0.5)
        x.append(rightx-leftx)

        lefty = skewnorm_dist_y.cdf(i-0.5)
        righty = skewnorm_dist_y.cdf(i+0.5)
        y.append(righty-lefty)

    return x, y

# kernel, xKernel, yKernel = createKernel(41, exampleDartLocationsX, exampleDartLocationsY)
# xKernel, yKernel = createKernel(201)

# heatmap = np.outer(xKernel, yKernel)
# print(heatmap.sum())
# plt.imshow(heatmap)
# plt.colorbar()
# plt.show()



DOUBLES = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,50]

IMPOSSIBLESCORES = [[23,29,31,35,37,41,43,44,46,47,49,52,53,55,56,58,59],
                    [103,106,109,112,113,115,116,118,119],
                    [163,166,169,172,173,175,176,178,179]]

DOUBLEREGIONPROBABILITIES = dict()
SCORINGREGIONPROBABILITIES = dict()

CHECKOUTPROBABILITIES = [dict(), dict()]

def calculateRegionProbability(total, horizontal, vertical, checkout):
    print(total)

    scores = np.fromfunction(np.vectorize(lambda i, j: scoreProb(i-200, j-200, total, checkout)), (400, 400))

    horizontal = np.array(horizontal)
    horizontal = horizontal.reshape(1, -1)
    vertical = np.array(vertical)
    vertical = vertical.reshape(1, -1)

    resultA = signal.correlate(scores, horizontal, mode='same')
    probabilities = signal.correlate(resultA, vertical.T, mode='same')
    
    return probabilities

def calculateRegionProbabilities(horizontal, vertical):
    # Calculate probabilities for doubles
    for total in DOUBLES:
        DOUBLEREGIONPROBABILITIES[total] = calculateRegionProbability(total, horizontal, vertical, True)
    
    # Calculate probabilities for all totals
    for total in range(0,61):
        if total in IMPOSSIBLESCORES[0]:
            continue

        SCORINGREGIONPROBABILITIES[total] = calculateRegionProbability(total, horizontal, vertical, False)

def calculateCheckoutProbabilities():
    for total in DOUBLES:
        CHECKOUTPROBABILITIES[0][total] = DOUBLEREGIONPROBABILITIES[total].max()

    for total in range(0,120):
        if total in IMPOSSIBLESCORES[1]:
            continue

        if total not in DOUBLEREGIONPROBABILITIES:
            a = 0
        else:
            a = DOUBLEREGIONPROBABILITIES[total]

        probabilities = a

        for region in range(0, 61):
            if region in IMPOSSIBLESCORES[0]:
                continue

            if (total-region) in CHECKOUTPROBABILITIES[0]:
                b = np.multiply(CHECKOUTPROBABILITIES[0][total-region], SCORINGREGIONPROBABILITIES[region])
            else:
                b = 0

            probabilities = np.add(probabilities, b)

        CHECKOUTPROBABILITIES[1][total] = probabilities.max()

def optimalNDarts(total, n):
    if total < 0 or n*60 < total:
        return 0
    elif total in IMPOSSIBLESCORES[n-1]:
        return 0

    if n == 1:
        return DOUBLEREGIONPROBABILITIES[total]
    
    if total not in DOUBLEREGIONPROBABILITIES:
        a = 0
    else:
        a = DOUBLEREGIONPROBABILITIES[total]

    probabilities = a

    for region in range(0, 61):
        if region in IMPOSSIBLESCORES[0]:
            continue

        if (total-region) in CHECKOUTPROBABILITIES[n-2]:
            b = np.multiply(CHECKOUTPROBABILITIES[n-2][total-region], SCORINGREGIONPROBABILITIES[region])
        else:
            b = 0

        probabilities = np.add(probabilities, b)

    return probabilities

# calculateRegionProbabilities(xKernel, yKernel)
# calculateCheckoutProbabilities()

while False:
    total = int(input("What score to checkout?"))

    probabilities = optimalNDarts(total, 3)
    x, y = np.unravel_index(probabilities.argmax(), probabilities.shape)
    plt.plot(y, x,'ro')
    plt.imshow(probabilities)
    plt.colorbar()

    # plt.show()





























# oneMaxProb = dict()
# twoMaxProb = dict()

# def probabilityScore(value, throwsLeft, skill, checkout):
#     # Cannot checkout a score of less than two
#     if value < 0:
#         return 0
#     if value < 2 and checkout == True:
#         return 0
    
#     if throwsLeft == 1:
#         scores = np.fromfunction(np.vectorize(lambda i, j: score(i-200, j-200, value, checkout)), (400, 400))
#         result = signal.convolve2d(scores, skill, mode='full')

#         return result

#     elif throwsLeft == 2:
#         inOne = probabilityScore(value, 1, skill, True)
#         miss = probabilityScore(0, 1, skill, False)

#         probability = np.add(inOne, np.multiply(miss, inOne.max()))

#         for i in range(1, value-1):
#             specific = probabilityScore(i, 1, skill, False)

#             if value-i in oneMaxProb:
#                 finish = oneMaxProb[value-i]
#             else:
#                 finish = probabilityScore(value-i, 1, skill, True).max()
#                 oneMaxProb[value-i] = finish

#             probability = np.add(probability, np.multiply(specific, finish))

#         return probability
    
#     elif throwsLeft == 3:
#         inTwo = probabilityScore(value, 2, skill, True)

#         probability = inTwo

#         for i in range(1,value-1):
#             specific = probabilityScore(i, 1, skill, False)

#             if value-i in twoMaxProb:
#                 finish = twoMaxProb[value-i]
#             else:
#                 finish = probabilityScore(value-i, 2, skill, True).max()
#                 twoMaxProb[value-i] = finish

#             probability = np.add(probability, np.multiply(specific, finish))

#         return probability
    
# # heatmap = probabilityScore(11, 3, kernel, True)

# # plt.imshow(heatmap)
# # plt.colorbar()
# # plt.show()

# # The size of the kernel
# # N = 50
# # k1d = signal.windows.gaussian(N, std=10).reshape(N, 1)
# # kernel = np.outer(k1d, k1d)
# # kernel = kernel/np.sum(kernel)

# # # Create a figure and axis
# # fig, ax = plt.subplots()

# # # Display the kernel using imshow
# # im = ax.imshow(kernel)
# # # Add a colorbar
# # cbar = fig.colorbar(im)

# # plt.imshow(kernel)
# # plt.colorbar()
# # plt.show()

# # indices = np.arange(400)
# # for region in range(0, 61):
#     # scores = np.fromfunction(np.vectorize(lambda i, j: score(i-200, j-200, region, False)), (400, 400))

#     # result = signal.convolve2d(scores, kernel, mode='full')


#     # plt.imshow(result)
#     # plt.colorbar()
#     # Show the plot
#     # plt.show()

# # Show the plot
# # plt.show()
        

