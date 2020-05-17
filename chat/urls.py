from django.urls import path

from . import views,encodingview

urlpatterns = [
    path('', views.index, name='index'),
    path('encoding',encodingview.generateImageEncoding.as_view(),name='encodings'),
    path('livestream/', views.room, name='room'),
]