import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats as st

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

    r, theta = cartesianToPolar(r-180, theta-180)

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

import numpy as np
from scipy.stats import norm

def expectation_matrix(sd):
    # Values used to approximate integral
    values = np.arange(0, 361)
    
    # Compute values of 2D normal density at approximating points
    density_matrix = np.outer(norm.pdf(values, 0, sd), norm.pdf(values, 0, sd))
    
    # Compute scores at approximating points
    score_matrix = np.fromfunction(np.vectorize(lambda x, y: score(x, y)), (361, 361))

    plt.imshow(score_matrix)
    plt.show()
    
    # Pad with zeros on all sides
    score_matrix = np.pad(score_matrix, ((361, 361), (361, 361)), mode='constant', constant_values=0)
    
    # Matrix to hold expected values
    expectation_matrix = np.zeros((361, 361))
    
    # Sweep distribution matrix over the board
    for i in range(361):
        for j in range(361):
            # Which subset of the score matrix to multiply with the density
            score_matrix_subset = score_matrix[i + 361 + values, j + 361 + values]
            
            # Contribution to expected value at approximating point
            contrib = np.sum(score_matrix_subset * density_matrix)
            expectation_matrix[i, j] = contrib
    
    return expectation_matrix

# Example usage with a standard deviation of 1.0
result_matrix = expectation_matrix(15.0)

plt.imshow(result_matrix)
plt.show()

plt.show()