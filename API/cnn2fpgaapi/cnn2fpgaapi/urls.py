from django.contrib import admin
from django.urls import path, include
from components import views

urlpatterns = [
    path('musics/', views.MusicList.as_view(), name='music-list'),
]
