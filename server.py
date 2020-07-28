# import the necessary packages
from flask import Flask, render_template, Response
from camera import VideoCamera


app = Flask(__name__, template_folder="templates")

cam = VideoCamera()

@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen2(camera):
    while True:
        #get camera frame
        avatar = camera.get_frame()[1]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + avatar + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/avatar')
def avatar():
    return Response(gen2(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0', port='5000', debug=True)
