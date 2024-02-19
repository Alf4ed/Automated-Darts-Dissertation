from flask import Flask, render_template, request, Response, jsonify
import cv2 as cv2
import gamedata

adminRef = None
gameRef = None
lockRef = None

app = Flask(__name__)

# Main pages
@app.route('/')
@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/skill')
def skill():
    changeMode('POSITIONING')
    return render_template('skill.html')

@app.route('/board-status')
def boardStatus():
    return render_template('board-status.html')

# Camera updating
@app.route('/upload', methods=['PUT'])
def upload():
    global frame
    frame = request.data
    return "OK"

def gen(camID):
    while True:

        lockRef.acquire()
        data = adminRef.frames[camID]
        lockRef.release()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'\r\n' + data + b'\r\n')

@app.route('/video/<camID>')
def video(camID):
    camID = int(camID)

    lockRef.acquire()
    cam = adminRef.frames[camID] is not None
    lockRef.release()

    if cam:
        return Response(gen(camID), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return ""

@app.route('/positions', methods=['GET'])
def positions():
    lockRef.acquire()
    dartPos = adminRef.showNew()
    lockRef.release()
    return jsonify(position=dartPos)

@app.route('/changeMode/<mode>', methods=['PUT'])
def changeMode(mode):
    lockRef.acquire()
    adminRef.mode = gamedata.Mode(mode)
    lockRef.release()
    return "OK"

@app.route('/moveCam/<camID>/<direction>', methods=['PUT'])
def moveCam(camID, direction):
    return "OK"

@app.route('/updateThresh/<threshVal>', methods=['PUT'])
def updateThresh(threshVal):
    print(threshVal)
    return "OK"

@app.route('/centerLine/<showCenter>', methods=['PUT'])
def centerLine(showCenter):
    lockRef.acquire()
    adminRef.centerLine = bool(showCenter)
    lockRef.release()
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0")

def startServer(admin, game, lock):
    global adminRef, gameRef, lockRef
    gameRef = game
    adminRef = admin
    lockRef = lock
    app.run(debug=True, use_reloader=False, host="0.0.0.0")