import detection
import cv2
import os
import numpy as np
import display
import math

correctly_classified = 0
total = 0

def iterateExamples():
    global correctly_classified, total

    multipliers = os.listdir('../data/largeDataset')

    raw = []
    processed = []

    for multiplier in multipliers:
        regions = os.listdir('../data/largeDataset/'+str(multiplier))

        for region in regions:
            examples = os.listdir('../data/largeDataset/'+str(multiplier)+'/'+str(region))

            examples.remove('BLANK')
            before = []
            before.append(cv2.imread('../data/largeDataset/'+str(multiplier)+'/'+str(region)+'/BLANK/A.jpg'))
            before.append(cv2.imread('../data/largeDataset/'+str(multiplier)+'/'+str(region)+'/BLANK/B.jpg'))
            before.append(cv2.imread('../data/largeDataset/'+str(multiplier)+'/'+str(region)+'/BLANK/C.jpg'))

            for example in examples:
                images = os.listdir('../data/largeDataset/'+str(multiplier+'/'+str(region)+'/'+str(example)))

                processed = []
                for i, image in enumerate(images):
                    after = cv2.imread('../data/largeDataset/'+str(multiplier)+'/'+str(region)+'/'+str(example)+'/'+str(image))
                    raw.append(after)
                    diff = detection.test_process_image(before[i], after, 25)

                    result = diff[0]

                    x = detection.find_dart_tip(diff[0])

                    if x != 'Hand' and x != 0:
                        croppedAfter = after[0:480, max(0, x[0]-100):min(x[0]+100, 640)]
                        croppedBefore = before[i][0:480, max(0, x[0]-100):min(x[0]+100, 640)]

                        diff2 = detection.test_process_image(croppedBefore, croppedAfter, 25)[0]

                        # Create a black image with the same dimensions
                        black_image = np.zeros_like(diff[0])
                        black_image[0:480, max(0, x[0]-100):min(x[0]+100, 640)] = diff2

                        diff = black_image

                        # diff = detection.create_difference(before[i], after)
                        # norm_img1 = cv2.normalize(diff, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
                        # diff = (255*norm_img1).astype(np.uint8)
                        # diff = cv2.Canny(diff, 100, 200)
                        # processed.append(diff)

                        result = diff

                    processed.append(result)

                correct = ""
                if multiplier == "SINGLE" or multiplier == "INNER_SINGLE":
                    correct = 'S'
                elif multiplier == 'DOUBLE':
                    correct = 'D'
                elif multiplier == 'TRIPLE':
                    correct = 'T'

                if correct == "":
                    correct = '0'
                else:
                    correct += str(region)

                scoreExample(processed[0], processed[1], processed[2], correct)
                
                # horizontal = np.hstack([processed[0], processed[1], processed[2]])
                # cv2.imshow('Difference'+str(example)+' '+str(multiplier)+str(region), horizontal)
                # cv2.waitKey(0)

    # return raw, processed
    return correctly_classified/total

def weightedAverage(pointA, pointB, pointC):
    ab = 1/math.dist(pointA, pointB)
    ac = 1/math.dist(pointA, pointC)
    bc = 1/math.dist(pointB, pointC)

    total = ab*ac + ab*bc + ac*bc

    aWeight = ab*ac/total
    bWeight = ab*bc/total
    cWeight = ac*bc/total

    x = pointA[0]*aWeight + pointB[0]*bWeight + pointC[0]*cWeight
    y = pointA[1]*aWeight + pointB[1]*bWeight + pointC[1]*cWeight

    return x, y

def scoreExample(imgA, imgB, imgC, correct):
    global correctly_classified, total

    aX = detection.find_dart_tip(imgA)
    bX = detection.find_dart_tip(imgB)
    cX = detection.find_dart_tip(imgC)

    if aX != 'Hand' and aX != 0 and bX != 'Hand' and bX != 0 and bX != 'Hand' and bX != 0 and cX != 'Hand' and cX != 0:
        aGrad = display.angle_to_gradient(display.find_angle(aX[0], 640, detection.fov) - detection.aCenter - 27)
        bGrad = display.angle_to_gradient(display.find_angle(bX[0], 640, detection.fov) - detection.bCenter + 27)
        cGrad = display.rotate_gradient_90(display.angle_to_gradient(display.find_angle(cX[0], 640, detection.fov) - detection.cCenter + 9))

        pointA = display.intersect(detection.aCameraX, detection.aCameraY, aGrad, detection.bCameraX, detection.bCameraY, bGrad)
        pointB = display.intersect(detection.bCameraX, detection.bCameraY, bGrad, detection.cCameraX, detection.cCameraY, cGrad)
        pointC = display.intersect(detection.aCameraX, detection.aCameraY, aGrad, detection.cCameraX, detection.cCameraY, cGrad)

        # xAvg = (pointA[0]+pointB[//0]+pointC[0])/3
        # yAvg = (pointA[1]+pointB[1]+pointC[1])/3
        xAvg, yAvg = weightedAverage(pointA, pointB, pointC)

        dart_score = display.score_dart(xAvg, yAvg)

        value = dart_score.to_string()

        # print('Correct: ' + str(correct) + ' Actual: ' + str(value))

        if correct == value:
            correctly_classified += 1
            # print('NICE')
        # else:
            
        #     board = display.Dartboard('black', 'white', 'green', 'red')

        #     xAvg = (pointA[0]+pointB[0]+pointC[0])/3
        #     yAvg = -(pointA[1]+pointB[1]+pointC[1])/3

        #     board.draw_line(detection.aCameraX, detection.aCameraY, aGrad)
        #     board.draw_line(detection.bCameraX, detection.bCameraY, bGrad)
        #     board.draw_line(detection.cCameraX, detection.cCameraY, cGrad)

        #     board.draw_point(xAvg, yAvg, marker='+', markersize=10)
            
        #     imgA = cv2.cvtColor(imgA, cv2.COLOR_GRAY2BGR)
        #     imgB = cv2.cvtColor(imgB, cv2.COLOR_GRAY2BGR)
        #     imgC = cv2.cvtColor(imgC, cv2.COLOR_GRAY2BGR)

        #     cv2.line(imgA, (int(aX[0]),0), (int(aX[0]), 480), (0,255,0), 2)
        #     cv2.line(imgB, (int(bX[0]),0), (int(bX[0]), 480), (0,255,0), 2)
        #     cv2.line(imgC, (int(cX[0]),0), (int(cX[0]), 480), (0,255,0), 2)

        #     horizontal = np.hstack([imgA, imgB, imgC])
        #     cv2.imshow('Difference', horizontal)
            
        #     board.show()

        #     cv2.waitKey(0)
            
        total += 1


def runAnnotated():
    images = os.listdir('./annotated')

    fov = 67.5

    for i, image in enumerate(images):
        if i % 3 == 0:
            resultA = eval(([j for j in images if j.startswith(str(i)+'_')][0]).removeprefix(str(i)+'_').removesuffix('.jpg'))
            resultB = eval(([j for j in images if j.startswith(str(i+1)+'_')][0]).removeprefix(str(i+1)+'_').removesuffix('.jpg'))
            resultC = eval(([j for j in images if j.startswith(str(i+2)+'_')][0]).removeprefix(str(i+2)+'_').removesuffix('.jpg'))

            aGrad = display.angle_to_gradient(display.find_angle(resultA[0], 640, fov) - detection.aCenter - 27)
            bGrad = display.angle_to_gradient(display.find_angle(resultB[0], 640, fov) - detection.bCenter + 27)
            cGrad = display.rotate_gradient_90(display.angle_to_gradient(display.find_angle(resultC[0], 640, fov) - detection.cCenter + 9))

            pointA = display.intersect(detection.aCameraX, detection.aCameraY, aGrad, detection.bCameraX, detection.bCameraY, bGrad)
            pointB = display.intersect(detection.bCameraX, detection.bCameraY, bGrad, detection.cCameraX, detection.cCameraY, cGrad)
            pointC = display.intersect(detection.aCameraX, detection.aCameraY, aGrad, detection.cCameraX, detection.cCameraY, cGrad)

            xAvg = (pointA[0]+pointB[0]+pointC[0])/3
            yAvg = (pointA[1]+pointB[1]+pointC[1])/3

            dart_score = display.score_dart(xAvg, yAvg)
            value = dart_score.to_string()

            # Weighted
            aAngle = 1/abs(display.find_angle(212, 640, detection.fov))
            bAngle = 1/abs(display.find_angle(558, 640, detection.fov))
            cAngle = 1/abs(display.find_angle(198, 640, detection.fov))
            totalAngle = (aAngle+bAngle+cAngle)*2

            weightedXAvg = (pointA[0]*(aAngle+bAngle)+pointB[0]*(bAngle+cAngle)+pointC[0]*(aAngle+cAngle))/totalAngle
            weightedYAvg = (pointA[1]*(aAngle+bAngle)+pointB[1]*(bAngle+cAngle)+pointC[1]*(aAngle+cAngle))/totalAngle

            weightedDartScore = display.score_dart(weightedXAvg, weightedYAvg)
            weightedValue = weightedDartScore.to_string()

            print(value, weightedValue)