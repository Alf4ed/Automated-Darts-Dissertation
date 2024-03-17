import numpy as np
import cv2, os

video_capture_1 = cv2.VideoCapture(0)
video_capture_2 = cv2.VideoCapture(2)
video_capture_3 = cv2.VideoCapture(1)

region = 0
count = 0

multipliers = ['TRIPLE', 'INNER_SINGLE']
multiplier = 'ERROR'
# os.mkdir('large_dataset/')
os.mkdir('large_dataset/'+str(multiplier))

print(str(multiplier)+'/'+str(region), 'BLANK')

while True:
    # Capture frame-by-frame
    ret1, frame1 = video_capture_1.read()
    ret2, frame2 = video_capture_2.read()
    ret3, frame3 = video_capture_3.read()

    horizontal = np.hstack([frame1, frame2, frame3])

    cv2.imshow('Dartboard', horizontal)

    k = cv2.waitKey(500)
    if k == ord('q'):
        break
    if k == ord('s'):

        if count == 0:
            os.mkdir('large_dataset/'+str(multiplier)+'/'+str(region))

            os.mkdir('large_dataset/'+str(multiplier)+'/'+str(region)+'/BLANK')

            cv2.imwrite('large_dataset/'+str(multiplier)+'/'+str(region)+'/BLANK'+'/A.jpg', frame1)
            cv2.imwrite('large_dataset/'+str(multiplier)+'/'+str(region)+'/BLANK'+'/B.jpg', frame2)
            cv2.imwrite('large_dataset/'+str(multiplier)+'/'+str(region)+'/BLANK'+'/C.jpg', frame3)
        else:
            os.mkdir('large_dataset/'+str(multiplier)+'/'+str(region)+'/'+str(count))

            cv2.imwrite('large_dataset/'+str(multiplier)+'/'+str(region)+'/'+str(count)+'/A.jpg', frame1)
            cv2.imwrite('large_dataset/'+str(multiplier)+'/'+str(region)+'/'+str(count)+'/B.jpg', frame2)
            cv2.imwrite('large_dataset/'+str(multiplier)+'/'+str(region)+'/'+str(count)+'/C.jpg', frame3)

        count += 1

        if count % 6 == 0:
            count = 0
            region += 1

        if region == 21 and (multiplier == 'SINGLE' or multiplier == 'DOUBLE'):
            region = 25
        elif region == 21:
            region = 26

        if region == 26:
            region = 1
            count = 0
            multiplier = multipliers.pop(0)
            os.mkdir('large_dataset/'+str(multiplier))

        if count == 0:
            print(str(multiplier)+'/'+str(region), 'BLANK')
        else:
            print(str(multiplier)+'/'+str(region))


# When everything is done, release the capture
video_capture_1.release()
video_capture_2.release()
video_capture_3.release()
cv2.destroyAllWindows()
