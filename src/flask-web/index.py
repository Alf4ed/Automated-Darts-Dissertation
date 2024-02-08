from flask import Flask, render_template, request, Response
import cv2 as cv2

app = Flask(__name__)
frame = None
frame = cv2.imread('sample.jpg')
_, frame = cv2.imencode('.JPG', frame)
frame = frame.tobytes()

# Main pages
@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/skill')
def skill():
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

def gen():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'\r\n' + frame + b'\r\n')
        
@app.route('/video')
def video():
    if frame:
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return ""

@app.route('/')
def index():
    return 'image:<br><img src="/video">'

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)