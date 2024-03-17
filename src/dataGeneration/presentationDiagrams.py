import display
import math
# import normal
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.patches import Circle
# import cv2

# hmm = normal.Normal()

# for i in range(1, 104, 5):
#     xKernel, yKernel = hmm.createKernel(401, std=i)
#     probs = hmm.calculateRegionProbability(1, xKernel, yKernel, False)
#     fig, ax = plt.subplots()
#     heatmap = ax.imshow(probs)
#     ax.set_title('STD = ' + str(i) + 'mm\nExpected Score: ' + str(round(probs.max())), loc='left')
#     # fig.colorbar(heatmap)

#     aimX, aimY = np.unravel_index(probs.argmax(), probs.shape)
#     ax.plot(aimY, aimX,'ro')

#     # plt.show()
#     fig.savefig('std'+str(i)+'.png', bbox_inches='tight', pad_inches=0, dpi=700)

# flatx = -335
# flaty = 0
# aCameraX = -335*math.cos(math.radians(27))
# aCameraY = 335*math.sin(math.radians(27))
# bCameraX = 335*math.cos(math.radians(27))
# bCameraY = 335*math.sin(math.radians(27))
# cCameraX = 335*math.cos(math.radians(81))
# cCameraY = -335*math.sin(math.radians(81))

dbBlack = '#282C34'
dbWhite = '#F9DFBC'
dbGreen = '#309F6A'
dbRed = '#E3292E'
complementary1 = '#29E3DE'
complementary2 = '#9F3065'
dodgerBlue = '#1E90FF'

board = display.Dartboard(dbBlack, dbWhite, dbRed, dbGreen)
board.savefig('board.png')

# # board.drawPoint(flatx, flaty, color=dodgerBlue, marker=(3, 0, -90), markersize=15)
# # board.drawPoint(aCameraX, aCameraY, color=dodgerBlue, marker=(3, 0, -63), markersize=15)
# # board.drawPoint(bCameraX, bCameraY, color=dodgerBlue, marker=(3, 0, 63), markersize=15)
# # board.drawPoint(cCameraX, cCameraY, color=dodgerBlue, marker=(3, 0, 171), markersize=15)
# # board.savefig('board-cam.png')

# # board.drawLine(aCameraX, aCameraY, display.angleToGradient(-27), color=dodgerBlue, linestyle='dashed', linewidth=2)
# # board.drawLine(bCameraX, bCameraY, display.angleToGradient(27), color=dodgerBlue, linestyle='dashed', linewidth=2)
# # board.drawLine(cCameraX, cCameraY, display.angleToGradient(-81), color=dodgerBlue, linestyle='dashed', linewidth=2)

# # board.drawPoint(112, -72, color='red', marker='x')
# # board.savefig('board-cam-dart.png')

# # board.drawGrid()
# # board.savefig('board-gridded.png')

# vertical = [70.93,36.74,-24.58,-14.17,56.55,-1.31,-23.58,-1.63,-15.7,-18.35,45.53,46.76,32.22,-25.25,8.53,-30.83,-25.89,9.36,-10.13,14.6,4.38,-8.25,-0.03,-5.21,-30.78,-4.62,68.5,12.68,12.08,-25.07,12.23,8.44,-48.17,-10.48,-16.9,-11.85,-4.17,4.13,6.19,12.2,-17.83,6.81,-41.3,-27.18,-28.71,-32,30.2,57.64,-13.57,-105.64]
# horizontal = [16.11,10.98,-21.25,27.82,4.22,33.87,24.91,16.69,10.01,14.42,17.13,21.88,29.92,13.9,25.75,8.55,-5.57,19.63,31.93,27.21,-17.27,-0.08,18.22,-21.49,-5,27.76,9.07,24.95,-18.94,-10.96,33.57,-6.37,55.9,-2.74,-21.68,4.46,-0.3,-36.85,-1.82,-25.98,19.57,47.34,43.91,-3,41.41,-22.03,-25.26,4.7,41.47,-17.7]

# for i in range(0, 50):
#     board.drawPoint(horizontal[i], vertical[i], markersize=5, color=dodgerBlue)

# board.savefig('board-with-darts.png')

# fig, ax = plt.subplots()
# ax.set_xlim([-230, 230])
# ax.set_ylim([230, -230])

# strategy = normal.Normal()
# x,y = strategy.createKernel(201, vertical, horizontal)
# heatmap = np.outer(x, y)

# center = (0, 0)
# radius = 225.5
# circle = Circle(center, radius, zorder=1, color='#000000')
# ax.add_patch(circle)

# ax.imshow(heatmap, extent=[-100, 100, -100, 100], zorder=2, cmap='hot')
# fig.savefig('board-heatmap.png', bbox_inches='tight', pad_inches=0, dpi=700, transparent=True)

# # Read Image
# imgA = cv2.imread('board-with-darts.png', 1) 
# imgB = cv2.imread('board-heatmap.png', 1) 
  
# # Add the images 
# img = cv2.addWeighted(imgB, 0.5, imgA, 0.5, 0)
# # img = cv2.add(imgA, imgB)
# # imS = cv2.resize(img, (960, 900))
# # Show the image 
# # cv2.imshow('image', imS)

# cv2.imwrite('heatmap-overlayed.png', img)

# cv2.waitKey(0)

# # plt.colorbar()