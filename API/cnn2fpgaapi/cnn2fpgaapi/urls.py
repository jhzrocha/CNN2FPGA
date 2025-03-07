from django.urls import path, include
from components import views
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('component')  # Redireciona para 'componentCreator/'

urlpatterns = [
    path('', home_redirect, name='home'),
    path('componentCreator/', views.component, name='component'),
    path('createComponent/', views.createComponent, name='createComponent'),
]
