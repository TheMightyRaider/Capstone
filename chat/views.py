from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login as auth_login

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated

import json

# Create your views here.

def index(request):
    return render(request, 'surveillance/index.html', {})

def register(request):
    if request.method == 'POST':

        form= UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save() # Creates a new user
            user = authenticate(username= form.cleaned_data['username'], password= form.cleaned_data['password1'])
            auth_login(request,user)
            return redirect('encodings')

    else:
        form=UserCreationForm()

    context={'form':form}
    return render(request,'registration/register.html',context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room(request):
    return render(request, 'surveillance/videostream.html', {
        'room_name_json':'data'
    })

def login(request):
    return render(request,'surveillance/login.html',{})