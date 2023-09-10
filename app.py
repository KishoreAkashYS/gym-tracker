from flask import Flask,render_template,request,url_for,redirect,Response
from model.capture import *

app = Flask(__name__)

#handles home route
@app.route('/')
def home():
    stop_camera()
    return render_template("index.html")

#handles training page route
@app.route('/training')
def training():
    stop_camera()
    return render_template("train.html")

#handles capture page route
@app.route('/capture/<string:workout>',methods=['GET','POST'])
def capture(workout):
    if request.method == "POST":
        start_camera()
        sets = request.form['sets']
        reps = request.form['reps']
        return render_template("capture.html", meta_data=[workout,sets,reps],workout=workout)
    return render_template("capture.html",workout=workout)

#Stop camera route
@app.route('/stop')
def stop():
    stop_camera()
    return redirect('training')

#Ajax video request
@app.route('/video/<string:workout>/<int:sets>/<int:reps>')
def video(workout,sets,reps):
    start_camera()
    return Response(generate_frames(workout,sets,reps), mimetype='multipart/x-mixed-replace; boundary=frame')

#error handler
@app.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html'), 500

if __name__== '__main__':
    app.run(debug=True)