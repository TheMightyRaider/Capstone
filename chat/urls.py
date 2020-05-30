from django.urls import path,include
from . import views,encodingview

urlpatterns = [
    path('index', views.index, name='index'),
    path('register',views.register,name='register'),
    path('', include('django.contrib.auth.urls')),
    path('encoding',encodingview.generateImageEncoding.as_view(),name='encodings'),
    path('livestream/', views.room, name='room'),
    path('log',encodingview.generateLog.as_view(),name='logging')
]