from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import cv2 as cv2
import gameData

# Shared thread references
adminRef = None
gameRef = None
lockRef = None

app = Flask(__name__)

# Setup new game
@app.route('/')
@app.route('/play')
def play():
    change_mode('ON')
    return render_template('play.html')

# Play a game
@app.route('/new_game', methods=['POST'])
def new_game():
    change_mode('GAME')
    format = int(request.form['game-type'])
    first_to = int(request.form['legs'])
    playerA = request.form['player1name']
    playerB = request.form['player2name']
    
    lockRef.acquire()
    gameRef.start_game(first_to, format, playerA, playerB)
    adminRef.mode = gameData.CameraMode.GAME
    lockRef.release()

    return redirect('/game/'+playerA+'/'+playerB+'/'+str(format))

@app.route('/game/<playerA>/<playerB>/<format>')
def game(playerA, playerB, format):
    lockRef.acquire()
    a_wins = gameRef.players[0].wins
    b_wins = gameRef.players[1].wins
    lockRef.release()
    return render_template('game.html', playerA=playerA, playerB=playerB, total=format, a_wins=a_wins, b_wins=b_wins)

# Calculate skill
@app.route('/skill')
def skill():
    change_mode('OFF')
    return render_template('skill.html')

# Start skill calculation
@app.route('/start-skill', methods=['PUT'])
def start_skill():
    change_mode('POSITIONING')
    lockRef.acquire()
    gameRef.positions = []
    adminRef.skills.append([request.json.get('name')])
    lockRef.release()
    return "OK"

# Stop skill calculation
@app.route('/stop-skill', methods=['PUT'])
def stop_skill():
    change_mode('OFF')
    lockRef.acquire()
    adminRef.skills[-1].append(gameRef.get_positions())
    lockRef.release()
    return "OK"

# Display camera feeds
@app.route('/board-status')
def boardStatus():
    change_mode('ON')
    return render_template('board-status.html')

# Convert still camera frames to video
def gen(camID):
    while True:

        lockRef.acquire()
        data = adminRef.frames[camID]
        lockRef.release()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'\r\n' + data + b'\r\n')

# Convert still aim recomendation to video
def aimbot_gen():
    while True:

        lockRef.acquire()
        aimbot = adminRef.aimbot.getvalue()
        lockRef.release()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'\r\n' + aimbot + b'\r\n')

# Return aim recomendation as video
@app.route('/aim')
def aim():
    # return video(0)
    lockRef.acquire()
    aim_condition = adminRef.aimbot is not None
    lockRef.release()

    if aim_condition:
        return Response(aimbot_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return ""
    
# Return camera feeds as video
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

# Get the positions of darts for skill page
@app.route('/positions', methods=['GET'])
def positions():
    lockRef.acquire()
    dart_pos, dart_score = gameRef.get_new_dart()
    lockRef.release()
    return jsonify(position=dart_pos, score=dart_score)

# Get the updated game values after the most recent dart is thrown
@app.route('/scores', methods=['GET'])
def scores():
    lockRef.acquire()
    scores = gameRef.get_scores()
    totals = gameRef.get_totals()
    wins = gameRef.get_wins()
    dart_pos, _ = gameRef.get_new_dart()
    change = gameRef.change()
    clear = gameRef.is_clear()
    just_won, active_player = gameRef.has_just_won()
    lockRef.release()
    return jsonify(scores=scores, totals=totals, position=dart_pos, change=change, clear=clear, wins=wins, just_won=just_won, active_player=active_player)

# Change the camera mode
@app.route('/changeMode/<mode>', methods=['PUT'])
def change_mode(mode):
    lockRef.acquire()
    adminRef.mode = gameData.CameraMode(mode)
    lockRef.release()
    return "OK"

# Draw centerline on images for calibration
@app.route('/centerLine/<showCenter>', methods=['PUT'])
def center_line(showCenter):
    lockRef.acquire()
    if showCenter == "true":
        adminRef.center_line = True
    else:
        adminRef.center_line = False
    lockRef.release()
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0")

# Start the server
def start_server(admin, game, lock):
    global adminRef, gameRef, lockRef
    gameRef = game
    adminRef = admin
    lockRef = lock
    app.run(debug=True, use_reloader=False, host="0.0.0.0")