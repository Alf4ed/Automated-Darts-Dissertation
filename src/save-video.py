import numpy as np
import cv2 as cv

capA = cv.VideoCapture(0)
capB = cv.VideoCapture(2)
capC = cv.VideoCapture(1)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'3IVD')

# outA = cv.VideoWriter('show.avi', fourcc, 1.0, (2840,  3029), True)
outA = cv.VideoWriter('TBoutputA.avi', fourcc, 9.0, (640,  480), True)
outB = cv.VideoWriter('TBoutputB.avi', fourcc, 9.0, (640,  480), True)
outC = cv.VideoWriter('TBoutputC.avi', fourcc, 9.0, (640,  480), True)

blank_frameA = None
blank_frameB = None
blank_frameC = None
change_frameA = None
change_frameB = None
change_frameC = None

while True:
    retA, frameA = capA.read()
    retB, frameB = capB.read()
    retC, frameC = capC.read()

    horizontal = np.hstack((frameA, frameB, frameC))
    cv.imshow('All', horizontal)

    key = cv.waitKey(1000)
    if key == ord('q'):
        break
    elif key == ord('s'):
        # write the frame
        for i in range(3):
            outA.write(blank_frameA)
            outB.write(blank_frameB)
            outC.write(blank_frameC)

        for i in range(3):
            outA.write(frameA)
            outB.write(frameB)
            outC.write(frameC)

        for i in range(3):
            outA.write(change_frameA)
            outB.write(change_frameB)
            outC.write(change_frameC)

    elif key == ord('b'):
        blank_frameA = frameA
        blank_frameB = frameB
        blank_frameC = frameC

    elif key == ord('c'):
        change_frameA = frameA
        change_frameB = frameB
        change_frameC = frameC

# for i in range(1, 104, 5):
#     img = cv.imread('std'+str(i)+'.png')
    
#     outA.write(img)


# Release everything if job is finished
capA.release()
capB.release()
capC.release()

outA.release()
outB.release()
outC.release()

cv.destroyAllWindows()