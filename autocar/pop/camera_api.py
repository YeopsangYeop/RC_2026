# video 카메라 정보가 나오는 것
# flask로 서버를 열 것
# jpg 압축 60%해서 데이터 보내기
# 5000번 포트로 api 열기
# 스레드 사용
import cv2
from pop import Util
import threading
import time
from flask import Flask, Response

app = Flask(__name__)

output_frame = None
lock = threading.Lock()

cam = Util.gstrmer(width=640, height=480, fps=30, flip=0)
cap = cv2.VideoCapture(cam, cv2.CAP_GSTREAMER)

def capture_frames():
    global output_frame, cap
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        with lock:
            output_frame = frame.copy()
        time.sleep(0.03)

def generate_frames():
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None:
                continue
            frame = output_frame.copy()
        
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        if not ret:
            continue
            
        jpg_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    t = threading.Thread(target=capture_frames)
    t.daemon = True
    t.start()
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)