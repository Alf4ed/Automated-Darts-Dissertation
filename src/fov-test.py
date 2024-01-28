import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

width = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
center = int(width/2)

while rval:

    line_thickness = 1
    cv2.line(frame, (center, 0), (center, height), (0, 255, 0), thickness=line_thickness)

    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)

    if key == 27:
        cv2.imwrite('fov.png', frame)
        break

cv2.destroyWindow("preview")
vc.release()