from imutils import paths
import face_recognition
import numpy as np
import pickle
import base64
import json
import cv2

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import UserAndEncodingDetail


class generateImageEncoding(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        print(request.FILES)
        data=request.FILES['encoding']
        name=request.data['name']
        imagebits=data.read()

        image=np.fromstring(imagebits,np.uint8)
        image= cv2.imdecode(image, cv2.IMREAD_COLOR)
       
        rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        boxes=face_recognition.face_locations(rgb,model='hog')
        encodings=face_recognition.face_encodings(rgb,boxes)
        
        for encoding in encodings:
            np_array_to_list=list(np.asarray(encoding))
            json_encoded_list=json.dumps(np_array_to_list)
            user_encoding=json_encoded_list
            user_name=name

        store_in_db=UserAndEncodingDetail.objects.create(owner=request.user,encoding=user_encoding,person_name=user_name)
        
        if store_in_db is not None:
            return Response({'success':True})
        else:
            return Response({'success':False})
     
    def get(self,request):
        return render(request,'surveillance/encoding.html',{})