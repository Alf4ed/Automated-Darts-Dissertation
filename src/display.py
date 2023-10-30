import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import math

fig, ax = plt.subplots()

# Set dimensions and force aspect ratio to be square
ax.set_xlim([-350, 350])
ax.set_ylim([350, -350])
ax.set_box_aspect(1)

# Board parts
foam = plt.Circle((0, 0), 337.5, color='gray')
board = plt.Circle((0,0), 225.5, color='k')
outerBull = plt.Circle((0,0), 16, color='g')
innerBull = plt.Circle((0,0), 6.35, color='r')

def drawSector(radius, color1, color2):
    for i in range(0, 20):
        theta1 = 9 + 18*(i-1)
        theta2 = 9 + (18*i)

        if i % 2 == 0:
            sector = Wedge((0,0), radius, theta1, theta2, color=color1)
        else:
            sector = Wedge((0,0), radius, theta1, theta2, color=color2)

        ax.add_patch(sector)

def drawLine():
    for i in range(0, 20):
        x1 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*16
        y1 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*16

        x2 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*170
        y2 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*170
    
        x1, y1 = [x1, x2], [y1, y2]
        ax.plot(x1, y1, color='gray', linewidth = '1')

ax.add_patch(foam)
ax.add_patch(board)

drawSector(170, 'g', 'r')
drawSector(162, 'k', 'k')
drawSector(107, 'g', 'r')
drawSector(99, 'k', 'k')

drawLine()

ax.add_patch(outerBull)
ax.add_patch(innerBull)

ax.plot(0, -335, color='m', marker='+')
ax.plot(-335, 0, color='m', marker='+')
ax.plot(335, 0, color='m', marker='+')

ax.axline((0, -335), (-10, -45), linewidth=1, color='c')
ax.axline((-335, 0), (-10, -45), linewidth=1, color='c')
ax.axline((335, 0), (-10, -45), linewidth=1, color='c')

plt.gca().set_aspect('equal')
plt.show()