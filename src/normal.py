import numpy as np
from scipy import signal
from scipy.stats import skewnorm
import matplotlib.pyplot as plt
import math
import display
import gamedata

DOUBLES = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,50]

IMPOSSIBLESCORES = [[23,29,31,35,37,41,43,44,46,47,49,52,53,55,56,58,59],
                    [103,106,109,112,113,115,116,118,119],
                    [163,166,169,172,173,175,176,178,179]]

def startNormal():
    pass

class Normal():
    def __init__(self):
        self.DOUBLEREGIONPROBABILITIES = dict()
        self.SCORINGREGIONPROBABILITIES = dict()

        self.CHECKOUTPROBABILITIES = [dict(), dict()]

    def createKernel(self, size, dataX=None, dataY=None, std=10):
        x, y = [], []

        if dataX is None or dataY is None:
            ax, locx, scalex = 0, 0, std
            ay, locy, scaley = 0, 0, std
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

    def calculateRegionProbability(self, total, horizontal, vertical, checkout):

        scores = np.fromfunction(np.vectorize(lambda i, j: display.scoreProb(i-200, j-200, total, checkout)), (400, 400))

        totals = np.fromfunction(np.vectorize(lambda i, j: display.score(i-200, j-200)[0]), (400, 400))

        horizontal = np.array(horizontal)
        horizontal = horizontal.reshape(1, -1)
        vertical = np.array(vertical)
        vertical = vertical.reshape(1, -1)

        resultA = signal.correlate(totals, horizontal, mode='same')
        probabilities = signal.correlate(resultA, vertical.T, mode='same')
        
        return probabilities

    def calculateRegionProbabilities(self, horizontal, vertical):
        # Calculate probabilities for doubles
        for total in DOUBLES:
            self.DOUBLEREGIONPROBABILITIES[total] = self.calculateRegionProbability(total, horizontal, vertical, True)
        
        # Calculate probabilities for all totals
        for total in range(0,61):
            if total in IMPOSSIBLESCORES[0]:
                continue

            self.SCORINGREGIONPROBABILITIES[total] = self.calculateRegionProbability(total, horizontal, vertical, False)

    def calculateCheckoutProbabilities(self):
        for total in DOUBLES:
            self.CHECKOUTPROBABILITIES[0][total] = self.DOUBLEREGIONPROBABILITIES[total].max()

        for total in range(0,120):
            if total in IMPOSSIBLESCORES[1]:
                continue

            if total not in self.DOUBLEREGIONPROBABILITIES:
                a = 0
            else:
                a = self.DOUBLEREGIONPROBABILITIES[total]

            probabilities = a

            for region in range(0, 61):
                if region in IMPOSSIBLESCORES[0]:
                    continue

                if (total-region) in self.CHECKOUTPROBABILITIES[0]:
                    b = np.multiply(self.CHECKOUTPROBABILITIES[0][total-region], self.SCORINGREGIONPROBABILITIES[region])
                else:
                    b = 0

                probabilities = np.add(probabilities, b)

            self.CHECKOUTPROBABILITIES[1][total] = probabilities.max()

    def optimalNDarts(self, total, n):
        if total < 0 or n*60 < total:
            return 0
        elif total in IMPOSSIBLESCORES[n-1]:
            return 0

        if n == 1:
            return self.DOUBLEREGIONPROBABILITIES[total]
        
        if total not in self.DOUBLEREGIONPROBABILITIES:
            a = 0
        else:
            a = self.DOUBLEREGIONPROBABILITIES[total]

        probabilities = a

        for region in range(0, 61):
            if region in IMPOSSIBLESCORES[0]:
                continue

            if (total-region) in self.CHECKOUTPROBABILITIES[n-2]:
                b = np.multiply(self.CHECKOUTPROBABILITIES[n-2][total-region], self.SCORINGREGIONPROBABILITIES[region])
            else:
                b = 0

            probabilities = np.add(probabilities, b)

        return probabilities


# kernel, xKernel, yKernel = createKernel(41, exampleDartLocationsX, exampleDartLocationsY)
# xKernel, yKernel = createKernel(201)

# heatmap = np.outer(xKernel, yKernel)
# print(heatmap.sum())
# plt.imshow(heatmap)
# plt.colorbar()
# plt.show()