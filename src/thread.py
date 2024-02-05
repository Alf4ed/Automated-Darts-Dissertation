import threading, tkinter as tk
import numpy as np
from game import dartGame
from detection import cameraSetup
from display import score, cartesianToPolar
import normal, io

import PIL

# import tkinter as tk
from tkinter.ttk import *
from tkinter.font import BOLD


xKernel, yKernel = normal.createKernel(201)
normal.calculateRegionProbabilities(xKernel, yKernel)
normal.calculateCheckoutProbabilities()


class GUI():
    def __init__(self):
        # Creat tkinter window
        self.root = tk.Tk()

        # Set background color
        self.root.configure(background='#282C34')

    def createLayout(self):
        self.playerA = tk.Canvas(self.root, background = 'grey', highlightthickness = 0)
        self.playerA.grid(row = 0, column = 0, sticky = tk.W, padx = (25,0), pady = (20,0))

        self.playerB = tk.Canvas(self.root, background = 'grey', highlightthickness = 0)
        self.playerB.grid(row = 1, column = 0, sticky = tk.W, padx = (25,0), pady = (20,0))

        self.edit = tk.Canvas(self.root, background = '#282C34', highlightthickness = 0)
        self.edit.grid(row = 2, column = 0, sticky = tk.W, padx = (25,0), pady = 20)

        self.undoButton = tk.Button(self.edit, text = 'Undo', command = self.undo, width = 5, background = 'grey', font = ('Arial', 12, BOLD), foreground = '#CCCCCC')
        self.undoButton.grid(row = 0, column = 0, sticky = tk.W, pady = 5)
        self.override = tk.Entry(self.edit, width = 5, font = ('Arial', 12, BOLD))
        self.override.grid(row = 1, column = 0, sticky = tk.W, pady = 5)
        self.instructions = tk.Button(self.edit, text = 'Enter', command = self.manual, width = 5, background = 'grey', font = ('Arial', 12, BOLD), foreground = '#CCCCCC')
        self.instructions.grid(row = 1, column = 1, sticky = tk.W, pady = 5, padx = 5)

        self.boardA = tk.Canvas(self.root, background = '#282C34', highlightthickness = 0)
        self.boardA.grid(row = 0, column = 1, sticky = tk.W, pady = 20, rowspan = 3)
        self.boardB = tk.Canvas(self.root, background = '#282C34', highlightthickness = 0)
        self.boardB.grid(row = 0, column = 2, sticky = tk.W, padx = 20, pady = 20, rowspan = 3)

    def createPlayers(self, playerOneName, playerTwoName):
        self.nameA = tk.Label(self.playerA, text = playerOneName, background = 'grey', font = ('Arial', 25, BOLD), foreground = '#36454F')
        self.nameA.grid(row = 0, column = 0, sticky = tk.W, pady = 2, padx = 50, columnspan = 2)
        self.scoreA = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#267F54', width = 3)
        self.scoreA.grid(row = 0, column = 2, sticky = tk.E, pady = 2, padx = 50)

        self.aDart1 = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.aDart1.grid(row = 1, column = 0, sticky = tk.W, pady = 2, padx = 50)
        self.aDart2 = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.aDart2.grid(row = 1, column = 1, pady = 2, padx = 50)
        self.aDart3 = tk.Label(self.playerA, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.aDart3.grid(row = 1, column = 2, sticky = tk.E, pady = 2, padx = 50)

        self.nameB = tk.Label(self.playerB, text = playerTwoName, background = 'grey', font = ('Arial', 25, BOLD), foreground = '#36454F')
        self.nameB.grid(row = 0, column = 0, sticky = tk.W, pady = 2, padx = 50, columnspan = 2)
        self.scoreB = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#267F54', width = 3)
        self.scoreB.grid(row = 0, column = 2, sticky = tk.E, pady = 2, padx = 50)

        self.bDart1 = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.bDart1.grid(row = 1, column = 0, sticky = tk.W, pady = 2, padx = 50)
        self.bDart2 = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.bDart2.grid(row = 1, column = 1, pady = 2, padx = 50)
        self.bDart3 = tk.Label(self.playerB, text = "-", background = 'grey', font = ('Arial', 25, BOLD), foreground = '#CCCCCC', width = 2)
        self.bDart3.grid(row = 1, column = 2, sticky = tk.E, pady = 2, padx = 50)

    def setBoardImage(self, img):
        self.boardATitle = tk.Label(self.boardA, text = 'Board Status', background = '#282C34', font = ('Arial', 25, BOLD), foreground = 'grey')
        self.boardATitle.grid(row = 0, column = 0, sticky = tk.N)

        self.imgA = tk.Canvas(self.boardA, width=369, height=369, background = '#282C34', highlightthickness = 0)
        self.imgA.grid(row = 1, column = 0, sticky = tk.W, pady = 20)
        self.imgA.create_image(0, 0, image=img, anchor=tk.NW)

        self.imgA.bind("<Button-1>", self.addDart)

    def setOptimalImage(self, img):
        self.boardBTitle = tk.Label(self.boardB, text = 'AimBot', background = '#282C34', font = ('Arial', 25, BOLD), foreground = 'grey')
        self.boardBTitle.grid(row = 0, column = 0, sticky = tk.N)

        self.imgB = tk.Canvas(self.boardB, width=369, height=369, background = '#282C34', highlightthickness = 0)
        self.imgB.grid(row = 1, column = 0, sticky = tk.W, pady = 20)
        self.newBoard = self.imgB.create_image(0, 0, image=img, anchor=tk.NW)

    def start(self):
        tk.mainloop()
    
    def addDart(self, event):
        x = (230/185)*(event.x - 185)
        y = (230/185)*(185 - event.y)

        r, theta = cartesianToPolar(x, y)
        value = score(r, theta)

        self.drawPoint(x, y)
        sync(value)

    def drawPoint(self, x, y):
        
        x = (185/230)*x + 185
        y = 185 - (185/230)*y 
        color = "blue"
        self.imgA.create_oval(x-5, y-5, x+5, y+5, fill=color, tags = "darts")

    def undo(self):
        removeDart()

    def manual(self):
        sync(self.override.get())
        self.override.delete(0, 'end')


lock = threading.Condition()
game = dartGame('Alan', 'Alfred', 121)

def removeDart():
    lock.acquire()
    game.undo()
    lock.release()

def sync(value):
    lock.acquire()
    if value == 'Changeover':
        game.changeOver()
    else:
        print(value[0], value[1])
        game.dart(int(value[0]), value[1])
    lock.release()

def showBoard(x, y):
    r, theta = cartesianToPolar(x, y)    
    sync(score(r, theta))

    x = (185/230)*x + 185
    y = 185 - (185/230)*y 
    game.inBoard.append([x, y])

def guiStart():
    display = GUI()
    display.createLayout()
    display.createPlayers(game.players[0].name, game.players[1].name)

    img = tk.PhotoImage(file = r"result.png")
    img1 = img.subsample(3, 3)
    
    display.setBoardImage(img1)
    display.setOptimalImage(img1)

    update(display)
    display.start()

def update(display):
    lock.acquire()
    if game.justChanged == True:
        display.imgA.delete('darts')
    if game.change == True:

        if len(game.inBoard) > 0:
            coordinates = game.inBoard.pop()
            x = coordinates[0]
            y = coordinates[1]
            display.imgA.create_oval(x-5, y-5, x+5, y+5, fill = 'cyan', tags = "darts")
        if game.activePlayer == 0:
            display.nameA.configure(foreground  = '#267F54')
            display.scoreA.configure(foreground = '#267F54')
            display.nameB.configure(foreground  = '#36454F')
            display.scoreB.configure(foreground = '#36454F')
        else:
            display.nameB.configure(foreground  = '#267F54')
            display.scoreB.configure(foreground = '#267F54')
            display.nameA.configure(foreground  = '#36454F')
            display.scoreA.configure(foreground = '#36454F')

        display.scoreA.configure(text = str(game.players[0].score))
        display.scoreB.configure(text = str(game.players[1].score))

        display.aDart1.configure(text = str(game.players[0].display[0]))
        display.aDart2.configure(text = str(game.players[0].display[1]))
        display.aDart3.configure(text = str(game.players[0].display[2]))

        display.bDart1.configure(text = str(game.players[1].display[0]))
        display.bDart2.configure(text = str(game.players[1].display[1]))
        display.bDart3.configure(text = str(game.players[1].display[2]))
        game.change = False

        probabilities, aimX, aimY = 0, 0, 0
        probabilities = normal.optimalNDarts(game.players[game.activePlayer].score, 3)
        
        aimX, aimY = np.unravel_index(probabilities.argmax(), probabilities.shape)
        plt.plot(aimY, aimX,'ro')

        for i in range(0, 20):
            x1 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*16
            y1 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*16

            x2 = math.cos((9/180)*math.pi + 2*math.pi/20*i)*170
            y2 = math.sin((9/180)*math.pi + 2*math.pi/20*i)*170
        
            x1, y1 = [x1+200, x2+200], [y1+200, y2+200]
            plt.plot(x1, y1, color='gray', linewidth = '0.5')

        plt.imshow(probabilities)
        # plt.colorbar()
        # plt.show()
        buf = io.BytesIO()
        plt.axis('off')
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)

        pil_image = PIL.Image.open(buf)
        pil_image = pil_image.resize((369,369), PIL.Image.ANTIALIAS)
        image_ref = PIL.ImageTk.PhotoImage(pil_image)

        # img = tk.PhotoImage(data=b, format='png')
        # img = img.subsample(3, 3)

        display.imgB.itemconfig(display.newBoard, image=image_ref)
        display.imgB.imgref = image_ref
        # display.imgB.image = img2
        buf.close()
        plt.close()

    lock.release()

    display.root.after(250, update, display)


import cv2
from display import *
import math

def findDartTip(before, after, threshVal):
    diff = cv2.absdiff(before, after)
    grayscale = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blurred = cv2.medianBlur(grayscale, 3)

    # Normalise
    # norm_img1 = cv2.normalize(blurred, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    # norm_img1 = (255*norm_img1).astype(np.uint8)
    norm_img1 = blurred

    # # Thresholding operations
    ret, thresh = cv2.threshold(norm_img1, threshVal, 255, cv2.THRESH_BINARY)
    # ret3,otsuCV = cv2.threshold(norm_img1, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # triangle = threshold_triangle(norm_img1)
    # yen = threshold_yen(norm_img1)
    # li = threshold_li(norm_img1)
    # min = threshold_minimum(norm_img1)
    # otsu = threshold_otsu(norm_img1)
    # isodata = threshold_isodata(norm_img1)
    # ret, triangle = cv2.threshold(norm_img1, triangle, 255, cv2.THRESH_BINARY)
    # ret, yen = cv2.threshold(norm_img1, yen, 255, cv2.THRESH_BINARY)
    # ret, li = cv2.threshold(norm_img1, li, 255, cv2.THRESH_BINARY)
    # ret, min = cv2.threshold(norm_img1, min, 255, cv2.THRESH_BINARY)
    # ret, otsu = cv2.threshold(norm_img1, otsu, 255, cv2.THRESH_BINARY)
    # ret, isodata = cv2.threshold(norm_img1, isodata, 255, cv2.THRESH_BINARY)

    # ret, all = cv2.threshold(all, 101, 255, cv2.THRESH_BINARY)

    # Morphological operations to remove noise
    kernelOpen = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    kernelClose = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    morphological = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernelOpen)
    final = cv2.morphologyEx(morphological, cv2.MORPH_CLOSE, kernelClose)

    # Find the lowest y point of the max size contour
    contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    val = 0

    if len(contours) == 0:
        val =  0
    else:
        cnt = max(contours, key = cv2.contourArea)
        size = cv2.contourArea(cnt)

        if size > 3000:
            val = "Hand"
        elif size < 25:
            val =  0
        else:
            val =  tuple(cnt[cnt[:, :, 1].argmax()][0])

    # blank = np.zeros(img.shape, dtype=np.uint8)

    # rows,cols = img.shape[:2]
    # [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
    # lefty = int(((-x*vy/vx) + y)[0])
    # righty = int((((cols-x)*vy/vx)+y)[0])
    # cv2.line(blank,(cols-1,righty),(0,lefty),(255,255,255),15)

    # blank = cv2.bitwise_and(blank, final)
    # y, x = np.nonzero(blank)
    # y = y[-1]
    # x = x[-1]

    return cv2.cvtColor(final, cv2.COLOR_GRAY2BGR ), val

def cameraSetup():
    fov = 67.5
    cameraWidth = 640

    aCenter = findCenterAngle(320, cameraWidth, fov)
    bCenter = findCenterAngle(320, cameraWidth, fov)
    cCenter = findCenterAngle(320, cameraWidth, fov)

    aCameraX = -335*math.cos(math.radians(27))
    aCameraY = 335*math.sin(math.radians(27))
    bCameraX = 335*math.cos(math.radians(27))
    bCameraY = 335*math.sin(math.radians(27))
    cCameraX = 335*math.cos(math.radians(81))
    cCameraY = -335*math.sin(math.radians(81))

    video_capture_1 = cv2.VideoCapture(2)
    video_capture_2 = cv2.VideoCapture(3)
    video_capture_3 = cv2.VideoCapture(1)

    oldFrameA = None
    oldFrameB = None
    oldFrameC = None

    detectAgain = False

    # Get camera frame proportions
    _, sample = video_capture_1.read()
    height, width, _ = sample.shape
    resizeHeight = int(height/1.5)
    resizeWidth = int(width/1.5)

    while True:
        # Capture frame-by-frame
        _, frame1 = video_capture_1.read()
        _, frame2 = video_capture_2.read()
        _, frame3 = video_capture_3.read()

        # Resize the images to reduce computational complexity
        resFrame1 = cv2.resize(frame1, (resizeWidth, resizeHeight))
        resFrame2 = cv2.resize(frame2, (resizeWidth, resizeHeight))
        resFrame3 = cv2.resize(frame3, (resizeWidth, resizeHeight))

        resFrame1 = resFrame1[int(resizeHeight*2/5):int(resizeHeight*5/6), 0:resizeWidth]
        resFrame2 = resFrame2[int(resizeHeight*2/5):int(resizeHeight*5/6), 0:resizeWidth]
        resFrame3 = resFrame3[int(resizeHeight*2/5):int(resizeHeight*5/6), 0:resizeWidth]

        if oldFrameA is not None:
            _, aX = findDartTip(oldFrameA, resFrame1, 20)
            _, bX = findDartTip(oldFrameB, resFrame2, 20)
            _, cX = findDartTip(oldFrameC, resFrame3, 20)

            if aX == 0 and bX == 0 and cX == 0:
                detectAgain = False
            elif detectAgain == False:
                detectAgain = True
            elif detectAgain == True:
                if aX == "Hand" or bX == "Hand" or cX == "Hand":
                    sync('Changeover')
                elif aX != 0 and bX != 0 and cX != 0:
                    aGrad = angleToGradient(findAngle(aX[0], resizeWidth, fov) - aCenter - 27)
                    bGrad = angleToGradient(findAngle(bX[0], resizeWidth, fov) - bCenter + 27)
                    cGrad = rotateGradient90(angleToGradient(findAngle(cX[0], resizeWidth, fov) - cCenter + 9))

                    pointA = intersect(aCameraX, aCameraY, aGrad, bCameraX, bCameraY, bGrad)
                    pointB = intersect(bCameraX, bCameraY, bGrad, cCameraX, cCameraY, cGrad)
                    pointC = intersect(aCameraX, aCameraY, aGrad, cCameraX, cCameraY, cGrad)

                    xAvg = (pointA[0]+pointB[0]+pointC[0])/3
                    yAvg = (pointA[1]+pointB[1]+pointC[1])/3

                    showBoard(xAvg, yAvg)

                detectAgain = False

            imageA = resFrame1.copy()
            imageB = resFrame2.copy()
            imageC = resFrame3.copy()

            if type(aX) == tuple and type(bX) == tuple and type(cX) == tuple:
                imageA = cv2.circle(imageA, aX, 5, (255, 0, 0), -1)
                imageB = cv2.circle(imageB, bX, 5, (255, 0, 0), -1)
                imageC = cv2.circle(imageC, cX, 5, (255, 0, 0), -1)

                cv2.line(imageA, (int(resizeWidth/2), resizeHeight), (int(resizeWidth/2), 0), (0, 255, 0), thickness=2)
                cv2.line(imageB, (int(resizeWidth/2), resizeHeight), (int(resizeWidth/2), 0), (0, 255, 0), thickness=2)
                cv2.line(imageC, (int(resizeWidth/2), resizeHeight), (int(resizeWidth/2), 0), (0, 255, 0), thickness=2)

                # processed = np.hstack([aImg, bImg, cImg])
                horizontal = np.hstack([imageA, imageB, imageC])

                # all = np.vstack([horizontal, processed])
                cv2.imshow('Dartboard', horizontal)
        
        if oldFrameA is None or detectAgain == False:
            oldFrameA = resFrame1
            oldFrameB = resFrame2
            oldFrameC = resFrame3

        k = cv2.waitKey(500)
        if k == ord('q'):
            break

    # When everything is done, release the capture
    video_capture_1.release()
    video_capture_2.release()
    video_capture_3.release()

    # cv2.destroyAllWindows()





t1 = threading.Thread(target=guiStart)
t2 = threading.Thread(target=cameraSetup)

t1.start()
t2.daemon = True
t2.start()

t1.join()