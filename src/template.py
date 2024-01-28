for subdir, dirs, files in os.walk(rootdir):
    if re.search("25", subdir):
        for file in files:
            
            if re.search("A", file) is not None:
                # print(subdir)
                # board = Dartboard(subdir)
                # board.drawPoint(aCameraX, aCameraY, color='r')
                # board.drawPoint(bCameraX, bCameraY, color='g')
                # board.drawPoint(cCameraX, cCameraY, color='b')

                aBefore = cv2.imread('C:/Users/alfre/Documents/cs310/src/dataset/empty125/_A.jpg')
                bBefore = cv2.imread('C:/Users/alfre/Documents/cs310/src/dataset/empty125/_B.jpg')
                cBefore = cv2.imread('C:/Users/alfre/Documents/cs310/src/dataset/empty125/_C.jpg')

                aAfter = cv2.imread(os.path.join(subdir, '_A.jpg'))
                bAfter = cv2.imread(os.path.join(subdir, '_B.jpg'))
                cAfter = cv2.imread(os.path.join(subdir, '_C.jpg'))

                aX, _ = findDartTip(aBefore, aAfter, 0, 65, (0, 0, 255))
                bX, _ = findDartTip(bBefore, bAfter, 1, 50, (0, 255, 0))
                cX, _ = findDartTip(cBefore, cAfter, 2, 50, (255, 0, 0))

                aGrad = angleToGradient(findAngle(aX, 640, fov) - aCenter + (90-camAAngle))
                bGrad = angleToGradient(findAngle(bX, 640, fov) - bCenter + (90-camBAngle))
                cGrad = angleToGradient(findAngle(cX, 640, fov) - cCenter + (90-camCAngle))

                board.drawLine(aCameraX, aCameraY, aGrad, color='r')
                board.drawLine(bCameraX, bCameraY, bGrad, color='g')
                board.drawLine(cCameraX, cCameraY, cGrad, color='b')

                x1, y1 = board.intersect(aCameraX, aCameraY, aGrad, bCameraX, bCameraY, bGrad)
                x2, y2 = board.intersect(bCameraX, bCameraY, bGrad, cCameraX, cCameraY, cGrad)
                x3, y3 = board.intersect(aCameraX, aCameraY, aGrad, cCameraX, cCameraY, cGrad)

                avX = (x1+x2+x3)/3
                avY = (y1+y2+y3)/3

                board.drawPoint(avX, -avY, 'cyan')

                r, theta = board.cartesianToPolar(avX, avY)
                score = board.score(r, theta)

                print(score)

                if re.search(score, subdir) is None:
                    compare = subdir+score
                    if re.search("(?P<type>[SD])[1-4]25(?P=type)25", compare) is None:
                        board.show()

                board.close()