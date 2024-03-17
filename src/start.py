import threading
import flaskSite.index as website
import detection
import normal
import gameData
import time

lock = threading.Condition()
admin = gameData.Admin()
game = gameData.Game()

t1 = threading.Thread(target=website.start_server, args=(admin,game,lock,))
t2 = threading.Thread(target=detection.start_detection, args=(admin,game,lock,))
t3 = threading.Thread(target=normal.start_normal, args=(admin,game,lock,))

t1.daemon = True
t2.daemon = True
t3.daemon = True

t1.start()
t2.start()
t3.start()

while True:
    time.sleep(1)