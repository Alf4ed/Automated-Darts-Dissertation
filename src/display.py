import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import math

def findAngle(xPos, width, fov):
    x = xPos - width/2

    angle = math.atan((2*x*math.tan(math.radians(fov/2)))/(width))
    angle = math.degrees(angle)
    
    return angle

def findCenterAngle(centerPos, width, fov):

    x = centerPos - width/2

    angle = math.atan((2*x*math.tan(math.radians(fov/2)))/(width))
    angle = math.degrees(angle)
    
    return angle

def angleToGradient(angle):
    angle += 9

    if angle == 0:
        slope = 0
    if angle < 0:
        slope = 1
    if angle > 0:
        slope = -1

    angle = abs(angle)

    gradient = math.sin(math.radians(angle)) / math.cos(math.radians(angle))
    gradient *= slope
    
    return gradient

def rotateGradient(gradient):
    return -1 * (1/gradient)

class Dartboard():
    def __init__(self, title):
        # self.fig, self.ax = plt.subplots()
        # self.ax = plt.subplot(1, 3, 1)
        self.ax = plt.subplot(2, 4, 1)

        # Set dimensions and force aspect ratio to be square
        self.ax.set_xlim([-350, 350])
        self.ax.set_ylim([350, -350])
        self.ax.set_box_aspect(1)
        plt.gca().set_aspect('equal')

        # self.fig.suptitle(title)
        # self.ax.title.set_text(title)

        self.drawBoard()

        self.ax.add_patch(self.foam)
        self.ax.add_patch(self.board)

        self.drawSector(170, 'g', 'r')
        self.drawSector(162, 'w', 'k')
        self.drawSector(107, 'g', 'r')
        self.drawSector(99, 'w', 'k')

        self.drawRadius()

        self.ax.add_patch(self.outerBull)
        self.ax.add_patch(self.innerBull)

    def drawBoard(self):
        # Board parts
        self.foam = plt.Circle((0, 0), 337.5, color='gray')
        self.board = plt.Circle((0,0), 225.5, color='k')
        self.outerBull = plt.Circle((0,0), 16, color='g')
        self.innerBull = plt.Circle((0,0), 6.35, color='r')

    def drawSector(self, radius, color1, color2):
        for i in range(0, 20):
            theta1 = 9 + 18*(i-1)
            theta2 = 9 + (18*i)

            if i % 2 == 0:
                sector = Wedge((0,0), radius, theta1, theta2, color=color1)
            else:
                sector = Wedge((0,0), radius, theta1, theta2, color=color2)

            self.ax.add_patch(sector)

    def drawRadius(self):
        for i in range(0, 20):
            x1 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*16
            y1 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*16

            x2 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*170
            y2 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*170
        
            x1, y1 = [x1, x2], [y1, y2]
            self.ax.plot(x1, y1, color='gray', linewidth = '1')

    def show(self):
        plt.show()

    def save(self):
        plt.axis('off')
        self.fig.savefig('board.png', bbox_inches='tight', pad_inches=0, dpi=300)
    
    def close(self):
        plt.close()

    def drawPoint(self, xPos, yPos, color='magenta'):
        self.ax.plot(xPos, yPos, color=color, marker='x')

    def drawLine(self, xPos, yPos, gradient, color='cyan'):
        if gradient == math.inf:
            self.ax.axline((xPos, yPos), (xPos, yPos-10), linewidth=1, color=color)
        else:
            self.ax.axline((xPos, yPos), (xPos+10, yPos-10*gradient), linewidth=1, color=color)

    def intersect(self, xPos1, yPos1, gradient1, xPos2, yPos2, gradient2):
        yPos1 = -yPos1
        yPos2 = -yPos2

        c1 = yPos1 - (xPos1*gradient1)
        c2 = yPos2 - (xPos2*gradient2)

        x = (c2 - c1) / (gradient1 - gradient2)
        y = gradient1*x + c1

        self.drawPoint(x, -y)

        return (x, -y)

    def cartesianToPolar(self, x, y):
        r = math.sqrt(x**2 + y**2)

        if x > 0:
            theta = math.atan(y/x)
        else:
            theta = math.atan(y/x) + math.pi
        
        return (r, theta)
    
    def score(self, r, theta):
        sectors = [6,13,4,18,1,20,5,12,9,14,11,8,16,7,19,3,17,2,15,10]
        sector = math.floor(((theta)/(2*math.pi))*20 + 1/2)
        value = str(sectors[sector])

        if 170 < r:
            return("MISS")
        elif 162 < r:
            return('D' + value)
        elif 107 < r:
            return('S' + value)
        elif 99 < r:
            return('T' + value)
        elif 16 < r:
            return('S' + value)
        elif 6.35 < r:
            return('S25')
        else:
            return('D25')

# topRatio = 0.10304878048780487
# sideRatio = 0.46463414634146344

# fov = 175

# topAngle = math.radians(fov*topRatio)
# sideAngle = math.radians(fov*sideRatio)

# fromTop(10, -310 + 10*math.sin(topAngle)/math.cos(topAngle))
# fromSide(-310, -10*math.sin(sideAngle)/math.cos(sideAngle))

# plt.show()