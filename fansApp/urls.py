from django.urls import path
from . import views
from fansApp import views as fans_views

urlpatterns = [
    path('mi-musica/', views.dashboard_fan, name='dashboard_fan'),
    path('seguir/<str:artista_id>/', views.seguir_artista, name='seguir_artista'),
    path('guardar-album/<int:album_id>/', views.guardar_album, name='guardar_album'),
    path('fans/configuracion/', fans_views.configuracion_fan, name='configuracion_fan'),
]