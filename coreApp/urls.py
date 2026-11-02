from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_general, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('recuperar-password/', views.solicitar_codigo_view, name='recuperar_password'),
    path('validar-codigo/', views.validar_codigo_view, name='validar_codigo'),
    path('nueva-password/', views.nueva_password_view, name='nueva_password'),
]