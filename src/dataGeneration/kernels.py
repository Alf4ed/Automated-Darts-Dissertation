
from scipy.stats import skewnorm
import math, numpy as np, matplotlib.pyplot as plt

def create_kernel(size,ax,locx,scalex,ay,locy,scaley):
        x, y = [], []

        # Use a players dart locations from skill calculation if they exist
        # Otherwise model as a standard circular normal distribution with standard deviation of 20mm
        # if data_x is None or data_y is None:
        #     ax, locx, scalex = 0, 0, std
        #     ay, locy, scaley = 0, 0, std
        # else:
        #     ax, locx, scalex = skewnorm.fit(data_x)
        #     ay, locy, scaley = skewnorm.fit(data_y)

        skewnorm_dist_x = skewnorm(ax, locx, scalex)
        skewnorm_dist_y = skewnorm(ay, locy, scaley)

        # Use cdf to bin the data
        for i in range(-math.floor(size/2), math.ceil(size/2)):
            leftx = skewnorm_dist_x.cdf(i-0.5)
            rightx = skewnorm_dist_x.cdf(i+0.5)
            x.append(rightx-leftx)

            lefty = skewnorm_dist_y.cdf(i-0.5)
            righty = skewnorm_dist_y.cdf(i+0.5)
            y.append(righty-lefty)

        # Return the horizontal and vertical discrete distributions
        return x, y

different = [[4,0,50,0,0,20]]

for i in different:
    x,y = create_kernel(401,i[0],i[1],i[2],i[3],i[4],i[5])

    kernel = np.outer(x,y)

    plt.imshow(kernel)
    plt.savefig('kernel'+str(i)+'.png', bbox_inches='tight', pad_inches=0, dpi=700, transparent=True)
    plt.show()