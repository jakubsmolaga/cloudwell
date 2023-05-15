import cv2
import flask
from detector import Detector

detector = Detector()
camera = cv2.VideoCapture("rtsp://10.141.6.2:8080/")
app = flask.Flask(__name__)


def make_stream():
    while True:
        _, frame = camera.read()
        detector.run(frame)
        _, jpeg = cv2.imencode(".jpg", frame)
        jpegBytes: bytes = jpeg.tobytes()
        yield (b"--frame\r\n")
        yield (b"Content-Type: image/jpeg\r\n\r\n" + jpegBytes + b"\r\n")


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/stream")
def stream():
    mimetype = "multipart/x-mixed-replace; boundary=frame"
    return flask.Response(make_stream(), mimetype=mimetype)


app.run(host="0.0.0.0", port=5000)
