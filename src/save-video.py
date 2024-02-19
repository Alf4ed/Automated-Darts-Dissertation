import numpy as np
import cv2 as cv

# capA = cv.VideoCapture(0)
# capB = cv.VideoCapture(1)
# capC = cv.VideoCapture(3)

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'3IVD')

outA = cv.VideoWriter('show.avi', fourcc, 1.0, (2840,  3029), True)
# outB = cv.VideoWriter('TBoutputB.avi', fourcc, 1.0, (640,  480), True)
# outC = cv.VideoWriter('TBoutputC.avi', fourcc, 1.0, (640,  480), True)

# while True:
    # retA, frameA = capA.read()
    # retB, frameB = capB.read()
    # retC, frameC = capC.read()

    # horizontal = np.hstack((frameA, frameB, frameC))
    # cv.imshow('All', horizontal)

    # key = cv.waitKey(1000)
    # if key == ord('q'):
        # break
    # elif key == ord('s'):
        # write the frame
        # outA.write(frameA)
        # outB.write(frameB)
        # outC.write(frameC)

for i in range(1, 104, 5):
    img = cv.imread('std'+str(i)+'.png')
    
    outA.write(img)


# Release everything if job is finished
# capA.release()
# capB.release()
# capC.release()

outA.release()
# outB.release()
# outC.release()

# cv.destroyAllWindows()