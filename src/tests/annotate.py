import cv2
import tests.createDifference
import os

dart_tip = None

# define a function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    global dart_tip

    if event == cv2.EVENT_LBUTTONDOWN:
        dart_tip = (x, y)
        print(dart_tip)
 

# Create a window
cv2.namedWindow('Point Coordinates', cv2.WND_PROP_FULLSCREEN)
# Bind the callback function to window
cv2.setMouseCallback('Point Coordinates', click_event)

raw, processed = tests.createDifference.iterateExamples()

os.mkdir('annotated/')

# display the image
for i, image in enumerate(raw):
    cv2.imshow('Point Coordinates', image)
    k = cv2.waitKey(0)
    cv2.imwrite('annotated/'+str(i)+'_'+str(dart_tip)+'.jpg', processed[i])

cv2.destroyAllWindows()