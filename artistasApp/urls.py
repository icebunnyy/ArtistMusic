from django.urls import path
from . import views

urlpatterns = [
    # Galería principal de artistas
    path('', views.inicio_artistas, name='inicio_artistas'),

    # Panel propio del Artista
    path('dashboard/', views.dashboard_artista, name='dashboard_artista'),

    # CRUD Artistas
    path('crear/', views.crear_artista, name='crear_artista'),
    path('editar/<str:artista_id>/', views.editar_artista, name='editar_artista'),
    path('eliminar/<str:artista_id>/', views.eliminar_artista, name='eliminar_artista'),

    # CRUD Álbumes
    path('album/crear/', views.crear_album, name='crear_album'),
    path('album/eliminar/<int:album_id>/', views.eliminar_album, name='eliminar_album'),

    # CRUD Eventos
    path('evento/crear/', views.crear_evento, name='crear_evento'),

    # Detalle público del artista
    path('<str:artista_id>/', views.detalle_artista, name='detalle_artista'),
]