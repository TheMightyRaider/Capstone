from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, ):
    return render(request, 'chat/videostream.html', {
        'room_name_json':'data'
    })