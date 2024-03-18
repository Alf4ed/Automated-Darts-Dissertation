import numpy as np
import cv2 as cv


capA = cv.VideoCapture(0)
capB = cv.VideoCapture(2)
capC = cv.VideoCapture(1)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'3IVD')

# Define the output formats
outA = cv.VideoWriter('LotsA.avi', fourcc, 9.0, (640,  480), True)
outB = cv.VideoWriter('LotsB.avi', fourcc, 9.0, (640,  480), True)
outC = cv.VideoWriter('LotsC.avi', fourcc, 9.0, (640,  480), True)

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

    # Display the three video feeds
    horizontal = np.hstack((frameA, frameB, frameC))
    cv.imshow('All', horizontal)

    key = cv.waitKey(1000)
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Write three 'blank' frames, then
        # Write three 'dart' frames, then
        # Write three 'change' frames
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

    # Update the 'blank' frame
    elif key == ord('b'):
        blank_frameA = frameA
        blank_frameB = frameB
        blank_frameC = frameC

    # Update the 'change' frame
    elif key == ord('c'):
        change_frameA = frameA
        change_frameB = frameB
        change_frameC = frameC

# Release everything if job is finished
capA.release()
capB.release()
capC.release()

outA.release()
outB.release()
outC.release()

cv.destroyAllWindows()