from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from imutils.video import FPS
import face_recognition
import numpy as np
import datetime
import base64
import json
import cv2
import time

from .models import UserAndEncodingDetail,LogDetail
from .emailtask import send_email_task
from threading import Thread
from decouple import config
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone


mailsent=False
sent_time=None
send_a_mail_again=None
process_this_frame=True

db_encoding=UserAndEncodingDetail.objects.values_list('encoding',flat=True)
encoded_user_name=UserAndEncodingDetail.objects.values_list('person_name',flat=True)
encoding_array=[]
encoded_user_array=list(encoded_user_name)

for encoding in db_encoding:
    json_to_list=json.loads(encoding)
    encoding_array.append(json_to_list)

class LiveStreamConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'livestream'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        global process_this_frame,mailsent,send_a_mail_again,sent_time
        obj={'recognised_name':'None'}

        pi_data=json.loads(text_data)
        user_id=pi_data['id']
        frames=bytes(pi_data['base64'])
        
        bts_again=base64.b64decode(frames)
        buff = np.fromstring(bts_again, np.uint8)
       
        img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        small_image = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)
        rgb_small_image = small_image[:, :, ::-1]

        start=time.time()

        if process_this_frame==5:
            face_locations=face_recognition.face_locations(rgb_small_image)
            encodings = face_recognition.face_encodings(rgb_small_image, face_locations)
            names=[]

            for encoding in encodings:
                matches = face_recognition.compare_faces(encoding_array,encoding)
                name='Unknown'
                if True in matches:
                    matchedIdxs=[i for (i,b) in enumerate(matches) if b ]
                    counts={}

                    for i in matchedIdxs:
                        name=encoded_user_name[i]
                        counts[name]=counts.get(name,0)+1

                    name=max(counts,key=counts.get)
                print(name)
                names.append(name)
                obj['recognised_name']=names
                obj['timestamp']=timezone.now()
                obj['intruder_frame']=frames
                obj['user_id']=user_id

            process_this_frame = 0 

        process_this_frame= process_this_frame + 1 

        sendmail(obj)

        # Send message to room 
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'image',
                'message': str(frames),
            }
        )
       
    # Receive message from room group
    def image(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
        }))

def sendmail(obj):
    global sent_time,mailsent,send_a_mail_again

    if "Unknown" in obj['recognised_name']:
        if (mailsent is False and sent_time is None) or obj['timestamp']>=send_a_mail_again:
            sent_time=obj['timestamp']
            mailsent=True

            user=User.objects.filter(id=obj['user_id'])
            adding_to_log=LogDetail.objects.create(owner_id=obj['user_id'],encoding=obj['intruder_frame'],timestamp=obj['timestamp'])

            send_a_mail_again=sent_time+datetime.timedelta(minutes=10)
            sent_at=sent_time.ctime()
            send_email_task.delay(sent_at)
            
        else:
            print('Sent Mail at :',sent_time)
            print('Time Now:',datetime.datetime.now())
            print('Sending again at:',send_a_mail_again)