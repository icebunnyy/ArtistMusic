from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PerfilFan, Notificacion
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from artistasApp.models import Artista, Album
from .forms import EditarUsuarioForm, EditarPerfilFanForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from artistasApp.models import HistorialMovimiento

@login_required
@login_required
def dashboard_fan(request):
    # Buscamos o creamos el perfil del usuario logueado
    perfil, created = PerfilFan.objects.get_or_create(usuario=request.user)
    
    # Extraemos sus datos
    artistas_fav = perfil.artistas_favoritos.all()
    albumes_guardados = perfil.albumes_guardados.all()
    
    # Pasamos 'perfil' al HTML para poder usar perfil.imagen_url
    return render(request, 'fans/dashboard_fan.html', {
        'perfil': perfil,
        'artistas_fav': artistas_fav,
        'albumes_guardados': albumes_guardados,
    })

@login_required
def seguir_artista(request, artista_id):
    # Buscamos o creamos el perfil del fan
    perfil, created = PerfilFan.objects.get_or_create(usuario=request.user)
    artista = get_object_or_404(Artista, id=artista_id)
    
    # Si ya lo sigue, lo quitamos. Si no, lo agregamos.
    if artista in perfil.artistas_favoritos.all():
        perfil.artistas_favoritos.remove(artista)
        messages.success(request, f"Dejaste de seguir a {artista.nombre}.")
    else:
        perfil.artistas_favoritos.add(artista)
        messages.success(request, f"¡Ahora sigues a {artista.nombre}!")
    
    # Devuelve al usuario a la página anterior
    return redirect(request.META.get('HTTP_REFERER', 'inicio_artistas'))

@login_required
def guardar_album(request, album_id):
    perfil, created = PerfilFan.objects.get_or_create(usuario=request.user)
    album = get_object_or_404(Album, id=album_id)
    
    if album in perfil.albumes_guardados.all():
        perfil.albumes_guardados.remove(album)
        messages.success(request, f"Quitaste '{album.titulo}' de tu biblioteca.")
    else:
        perfil.albumes_guardados.add(album)
        messages.success(request, f"¡'{album.titulo}' guardado en tu biblioteca!")
        
    return redirect(request.META.get('HTTP_REFERER', 'inicio_artistas'))


@login_required
def configuracion_fan(request):
    # Buscamos el perfil del usuario logueado (y si no tiene por error, se lo crea)
    perfil, created = PerfilFan.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        # Verificamos si el usuario hizo clic en el botón de "Guardar Perfil"
        if 'guardar_perfil' in request.POST:
            usuario_form = EditarUsuarioForm(request.POST, instance=request.user)
            perfil_form = EditarPerfilFanForm(request.POST, request.FILES, instance=perfil)
            password_form = PasswordChangeForm(request.user) # Lo instanciamos vacío para el contexto

            if usuario_form.is_valid() and perfil_form.is_valid():
                usuario_form.save()
                perfil_form.save()
                messages.success(request, '¡Tu perfil ha sido actualizado con éxito! ✨')
                return redirect('configuracion_fan')
            else:
                messages.error(request, 'Hubo un error al actualizar tu perfil. Revisa los datos.')

        # Verificamos si el usuario hizo clic en el botón de "Cambiar Contraseña"
        elif 'cambiar_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            usuario_form = EditarUsuarioForm(instance=request.user)
            perfil_form = EditarPerfilFanForm(instance=perfil)

            if password_form.is_valid():
                user = password_form.save()
                # update_session_auth_hash evita que se cierre la sesión al cambiar la clave
                update_session_auth_hash(request, user)
                messages.success(request, '¡Tu contraseña ha sido actualizada con éxito! 🔒')
                return redirect('configuracion_fan')
            else:
                messages.error(request, 'Hubo un error al cambiar la contraseña. Revisa los datos.')
                
    else:
        # Si entra a la página por primera vez (GET), cargamos los formularios con sus datos actuales
        usuario_form = EditarUsuarioForm(instance=request.user)
        perfil_form = EditarPerfilFanForm(instance=perfil)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'fans/configuracion.html', {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
        'password_form': password_form,
        'perfil': perfil, # Para poder mostrar su foto actual en la pantalla
    })
def registrar_accion(usuario, accion):
    HistorialMovimiento.objects.create(usuario=usuario, accion=accion)

@login_required
def configuracion_fan(request):
    perfil, created = PerfilFan.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        if 'guardar_perfil' in request.POST:
            usuario_form = EditarUsuarioForm(request.POST, instance=request.user)
            perfil_form = EditarPerfilFanForm(request.POST, request.FILES, instance=perfil)
            password_form = PasswordChangeForm(request.user)

            if usuario_form.is_valid() and perfil_form.is_valid():
                usuario_form.save()
                perfil_form.save()
                
                # Registramos el movimiento en la BD
                registrar_accion(request.user, 'Actualización de datos personales / foto de perfil')
                
                messages.success(request, '¡Tu perfil ha sido actualizado con éxito! ✨')
                return redirect('configuracion_fan')
            else:
                messages.error(request, 'Hubo un error al actualizar tu perfil. Revisa los datos.')

        elif 'cambiar_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            usuario_form = EditarUsuarioForm(instance=request.user)
            perfil_form = EditarPerfilFanForm(instance=perfil)

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                
                # Registramos el cambio de clave en la BD
                registrar_accion(request.user, 'Cambio de contraseña de usuario')
                
                messages.success(request, '¡Tu contraseña ha sido actualizada con éxito! 🔒')
                return redirect('configuracion_fan')
            else:
                messages.error(request, 'Hubo un error al cambiar la contraseña. Revisa los datos.')
                
    else:
        usuario_form = EditarUsuarioForm(instance=request.user)
        perfil_form = EditarPerfilFanForm(instance=perfil)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'fans/configuracion.html', {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
        'password_form': password_form,
        'perfil': perfil,
    })