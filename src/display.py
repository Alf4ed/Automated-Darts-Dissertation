import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
import math
import cmath
import gamedata

def find_angle(xPos, width, fov):
    x = xPos - width/2

    angle = math.atan((2*x*math.tan(math.radians(fov/2)))/(width))
    angle = math.degrees(angle)
    
    return angle

def find_center_angle(centerPos, width, fov):

    x = centerPos - width/2

    angle = math.atan((2*x*math.tan(math.radians(fov/2)))/(width))
    angle = math.degrees(angle)
    
    return angle

def angle_to_gradient(angle):

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

def rotate_gradient_90(gradient):
    return -(1/gradient)

def intersect(xPos1, yPos1, gradient1, xPos2, yPos2, gradient2):
    yPos1 = -yPos1
    yPos2 = -yPos2

    c1 = yPos1 - (xPos1*gradient1)
    c2 = yPos2 - (xPos2*gradient2)

    x = (c2 - c1) / (gradient1 - gradient2)
    y = gradient1*x + c1

    return (x, y)

def cartesian_to_polar(x, y):
    r = math.sqrt(x**2 + y**2)

    input_num = complex(x, y)
    r, theta = cmath.polar(input_num)
    theta += -math.pi/2
    
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
    
def score_dart(x, y):
    r, theta = cartesian_to_polar(x, y)
    sectors = [20,5,12,9,14,11,8,16,7,19,3,17,2,15,10,6,13,4,18,1]
    sector = math.floor(((theta)/(2*math.pi))*20 + 1/2)
    value = sectors[sector]

    if 170 < r:
        return gamedata.Dart(0, 0, [x, y])
    elif 162 < r:
        return gamedata.Dart(value, 2, [x, y])
    elif 107 < r:
        return gamedata.Dart(value, 1, [x, y])
    elif 99 < r:
        return gamedata.Dart(value, 3, [x, y])
    elif 16 < r:
        return gamedata.Dart(value, 1, [x, y])
    elif 6.35 < r:
        return gamedata.Dart(25, 1, [x, y])
    else:
        return gamedata.Dart(25, 2, [x, y])

def score_prob(x, y, target, checkout):

    r, theta = cartesian_to_polar(x, y)
    result, double = score(r, theta)

    if not checkout or double:
        if target == result:
            return 1
        
    return 0
    
class Dartboard():
    def __init__(self, c_black, c_white, c_red, c_green):
        self.fig, self.ax = plt.subplots()

        # Set dimensions and force aspect ratio to be square
        self.ax.set_xlim([-350, 350])
        self.ax.set_ylim([350, -350])
        # self.ax.set_xlim([-20, 20])
        # self.ax.set_ylim([20, -20])
        self.ax.set_box_aspect(1)
        plt.gca().set_aspect('equal')

        self.draw_board(c_black, c_red, c_green)

        # self.ax.add_patch(self.foam)
        self.ax.add_patch(self.board)

        self.draw_sector(170, c_green, c_red)
        self.draw_sector(162, c_white, c_black)
        self.draw_sector(107, c_green, c_red)
        self.draw_sector(99, c_white, c_black)

        self.draw_radius()

        self.ax.add_patch(self.outerBull)
        self.ax.add_patch(self.innerBull)

        circle5 = Circle((0, 0), radius=16, color='grey', fill=False, linewidth=1)
        circle6 = Circle((0, 0), radius=6.35, color='grey', fill=False, linewidth=1)
        self.ax.add_patch(circle5)
        self.ax.add_patch(circle6)

        # self.addText()

    def add_text(self, color='gray'):
        sectors = ['10','15','2','17','3','19','7','16','8','11','14','9','12','5','20','1','18','4','13','6']

        for i in range(0, 20):
            x = math.cos((18/180)*math.pi + 2*math.pi/20*i)*200
            y = math.sin((18/180)*math.pi + 2*math.pi/20*i)*200

            plt.text(x, y, sectors[i], horizontalalignment='center',
                     verticalalignment='center', fontsize=12, color=color)
    
    def get_fig(self):
        # plt.axis('off')
        return self.fig
    
    def draw_board(self, cBlack, cRed, cGreen):
        # Board parts
        self.foam = plt.Circle((0, 0), 337.5, color='gray')
        self.board = plt.Circle((0,0), 225.5, color='#282C34')
        self.outerBull = plt.Circle((0,0), 16, color=cGreen)
        self.innerBull = plt.Circle((0,0), 6.35, color=cRed)

    def draw_sector(self, radius, color1, color2):
        for i in range(0, 20):
            theta1 = 9 + 18*(i-1)
            theta2 = 9 + (18*i)

            if i % 2 == 0:
                sector = Wedge((0,0), radius, theta1, theta2, color=color1)
            else:
                sector = Wedge((0,0), radius, theta1, theta2, color=color2)

            self.ax.add_patch(sector)

    def draw_radius(self, color='gray'):
        for i in range(0, 20):
            x1 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*16
            y1 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*16

            x2 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*170
            y2 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*170
        
            x1, y1 = [x1, x2], [y1, y2]
            self.ax.plot(x1, y1, color=color, linewidth=1)

        circle1 = Circle((0, 0), radius=170, color=color, fill=False, linewidth=1)
        circle2 = Circle((0, 0), radius=162, color=color, fill=False, linewidth=1)
        circle3 = Circle((0, 0), radius=107, color=color, fill=False, linewidth=1)
        circle4 = Circle((0, 0), radius=99, color=color, fill=False, linewidth=1)
        self.ax.add_patch(circle1)
        self.ax.add_patch(circle2)
        self.ax.add_patch(circle3)
        self.ax.add_patch(circle4)

    def draw_grid(self, color='grey'):
        for i in range(-200,201):
            for j in range(-200,201):
                self.ax.plot(i, j, color='#1E90FF', marker=',')

    def show(self):
        plt.show()
    
    def close(self):
        plt.close()

    def savefig(self, filename):
        # plt.axis('off')
        self.fig.savefig(filename, bbox_inches='tight', pad_inches=0, dpi=700, transparent=True)

    def draw_point(self, xPos, yPos, color='magenta', marker='x', markersize=1):
        self.ax.plot(xPos, yPos, color=color, marker=marker, markersize=markersize)

    def draw_line(self, xPos, yPos, gradient, color='cyan', linestyle='solid', linewidth=1):
        if gradient == math.inf:
            self.ax.axline((xPos, yPos), (xPos, yPos-10), color=color, linestyle=linestyle, linewidth=linewidth)
        else:
            self.ax.axline((xPos, yPos), (xPos+10, yPos-10*gradient), color=color, linestyle=linestyle, linewidth=linewidth)