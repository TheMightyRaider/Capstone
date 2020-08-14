from websocket import create_connection
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import base64
import time
import numpy as np
import cv2
import json


ws=create_connection("ws://127.0.0.1:8000/ws/livestream/")
print('Sending Frame')

vs = VideoStream(src=0).start()
time.sleep(1.0)
fps = 1
timecount=0
fps=FPS().start()
# for i in range(60):
while True:
    frame=vs.read()
    frame = imutils.resize(frame, width=450)
    start=time.time()
    _, bts = cv2.imencode('.jpeg', frame)
    end=time.time()
    print(end-start)
    bts = bts.tostring()
    base64_format=base64.b64encode(bts)
    obj={
        'id':3,
        'base64':list(base64_format)
    }
    json_value=json.dumps(obj)
    ws.send(json_value)
    timecount=timecount+(end-start)
    time.sleep(0.1)
    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))