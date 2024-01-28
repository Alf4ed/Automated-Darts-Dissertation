# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask import render_template, Response
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import io
import sys
sys.path.append('../../src')
from display import *
import base64
from io import BytesIO

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/print-plot')
def plot_png():

   board = Dartboard('Darboard', '#282C34', '#F9DFBC', '#E3292E', '#309F6A')   

   # fig = plt.Figure()
   # axis = fig.add_subplot(1, 1, 1)
   # xs = np.random.rand(100)
   # ys = np.random.rand(100)
   # axis.plot(xs, ys)
   # output = io.BytesIO()

   buf = BytesIO()
   board.getFig().savefig(buf, format="png", transparent=True, bbox_inches='tight', pad_inches=0, dpi=300)

   # Embed the result in the html output.
   data = base64.b64encode(buf.getbuffer()).decode("ascii")

   # return f"data:image/png;base64,{data}"

   # FigureCanvas(board.getFig()).print_png(output)
   return Response(buf.getvalue(), mimetype='image/png')


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()