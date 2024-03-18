import threading
import flaskSite.index as website
import detection
import normal
import gameData
import time

# Create the locking condition and the shared memory
lock = threading.Condition()
admin = gameData.Admin()
game = gameData.Game()

# Create three threads to run the specified functions, passing the locking conditions and shared memory
t1 = threading.Thread(target=website.start_server, args=(admin,game,lock,))
t2 = threading.Thread(target=detection.start_detection, args=(admin,game,lock,))
t3 = threading.Thread(target=normal.start_normal, args=(admin,game,lock,))

# All threads terminate if the main thread terminates
t1.daemon = True
t2.daemon = True
t3.daemon = True

# Start the three threads
t1.start()
t2.start()
t3.start()

# This allows for keyboard interrupts
while True:
    time.sleep(1)