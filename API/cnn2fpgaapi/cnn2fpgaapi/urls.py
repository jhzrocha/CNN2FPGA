from django.urls import path, include
from components import views

urlpatterns = [
    # path('musics/', views.MusicList.as_view(), name='music-list'),
    path('componentCreator/', views.component, name='component'),
    path('createComponent/', views.createComponent, name='createComponent'),
]
