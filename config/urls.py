from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

def home_general(request):
    return render(request, 'core/index_general.html')
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_general, name='home'),             # La raíz general 
    # Rutas globales y autenticación (coreApp)
    path('', include('coreApp.urls')),
    # Catálogo público y panel del artista (artistasApp)
    path('artistas/', include('artistasApp.urls')),
    # Panel exclusivo de administración (panelAdminApp)
    path('panel-admin/', include('panelAdminApp.urls')),
    path('fans/', include('fansApp.urls')),

]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)