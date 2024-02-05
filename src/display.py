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

def rotateGradient90(gradient):
    return -(1/gradient)

def intersect(xPos1, yPos1, gradient1, xPos2, yPos2, gradient2):
    yPos1 = -yPos1
    yPos2 = -yPos2

    c1 = yPos1 - (xPos1*gradient1)
    c2 = yPos2 - (xPos2*gradient2)

    x = (c2 - c1) / (gradient1 - gradient2)
    y = gradient1*x + c1

    return (x, y)

def cartesianToPolar(x, y):
    r = math.sqrt(x**2 + y**2)

    if x == 0:
        theta = math.pi/2
    elif y == 0:
        theta = 0
    elif x > 0:
        theta = math.atan(y/x)
    else:
        theta = math.atan(y/x) + math.pi
    
    return (r, theta)

def score(r, theta):
    sectors = [6,13,4,18,1,20,5,12,9,14,11,8,16,7,19,3,17,2,15,10]
    sector = math.floor(((theta)/(2*math.pi))*20 + 1/2)
    value = str(sectors[sector])

    if 170 < r:
        return(0, False)
    elif 162 < r:
        return(2*int(value), True)
    elif 107 < r:
        return(int(value), False)
    elif 99 < r:
        return(3*int(value), False)
    elif 16 < r:
        return(int(value), False)
    elif 6.35 < r:
        return(25, False)
    else:
        return(50, True)

class Dartboard():
    def __init__(self, title, cBlack, cWhite, cRed, cGreen):
        self.fig, self.ax = plt.subplots()

        # Set dimensions and force aspect ratio to be square
        self.ax.set_xlim([-350, 350])
        self.ax.set_ylim([350, -350])
        self.ax.set_box_aspect(1)
        plt.gca().set_aspect('equal')

        # self.ax.title.set_text(title)

        self.drawBoard(cRed, cGreen)

        # self.ax.add_patch(self.foam)
        # self.ax.add_patch(self.board)

        self.drawSector(170, cGreen, cRed)
        self.drawSector(162, cWhite, cBlack)
        self.drawSector(107, cGreen, cRed)
        self.drawSector(99, cWhite, cBlack)

        self.drawRadius()

        self.ax.add_patch(self.outerBull)
        self.ax.add_patch(self.innerBull)

        self.addText()

    def addText(self):
        sectors = ['10','15','2','17','3','19','7','16','8','11','14','9','12','5','20','1','18','4','13','6']

        for i in range(0, 20):
            x = math.cos((18/180)*math.pi + 2*math.pi/20*i)*200
            y = math.sin((18/180)*math.pi + 2*math.pi/20*i)*200

            plt.text(x, y, sectors[i], horizontalalignment='center',
                     verticalalignment='center', fontsize=14, color='#CCCCCC')
    
    def getFig(self):
        plt.axis('off')
        self.ax.set_xlim([-230, 230])
        self.ax.set_ylim([230, -230])
        return self.fig
    
    def drawBoard(self, cRed, cGreen):
        # Board parts
        # self.foam = plt.Circle((0, 0), 337.5, color='gray')
        # self.board = plt.Circle((0,0), 225.5, color='k')
        self.outerBull = plt.Circle((0,0), 16, color=cGreen)
        self.innerBull = plt.Circle((0,0), 6.35, color=cRed)

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

    def savefig(self, filename):
        plt.savefig(filename, dpi=400)

    def drawPoint(self, xPos, yPos, color='magenta'):
        self.ax.plot(xPos, yPos, color=color, marker='x')

    def drawLine(self, xPos, yPos, gradient, color='cyan', linestyle='solid'):
        if gradient == math.inf:
            self.ax.axline((xPos, yPos), (xPos, yPos-10), linewidth=1, color=color, linestyle=linestyle)
        else:
            self.ax.axline((xPos, yPos), (xPos+10, yPos-10*gradient), linewidth=1, color=color, linestyle=linestyle)