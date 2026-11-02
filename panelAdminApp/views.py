from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group  # <-- AQUÍ IMPORTAMOS GROUP
from django.db.models import Q                     # <-- AQUÍ IMPORTAMOS Q
from django.contrib import messages
from artistasApp.models import Artista, Album, Evento, HistorialMovimiento
from fansApp.models import PerfilFan
from .forms import AdminUsuarioForm

def es_admin(user):
    return user.is_authenticated and (user.groups.filter(name='Administrador').exists() or user.is_superuser)

@login_required
@user_passes_test(es_admin)
def dashboard_admin(request):
    artistas = Artista.objects.all()
    albumes = Album.objects.all()
    eventos = Evento.objects.all()
    usuarios = User.objects.all()
    historial = HistorialMovimiento.objects.all().order_by('-fecha')[:20]

    return render(request, 'panelAdmin/dashboard_admin.html', {
        'artistas': artistas,
        'albumes': albumes,
        'eventos': eventos,
        'usuarios': usuarios,
        'historial': historial
    })

@login_required
@user_passes_test(es_admin)
def lista_usuarios(request):
    query = request.GET.get('q', '').strip()
    rol_filtro = request.GET.get('rol', '').strip()
    
    usuarios = User.objects.all().order_by('-date_joined')
    
    # Filtrar por texto (Username, Email, Nombre o Apellido)
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        
    # Filtrar por Rol (Grupo)
    if rol_filtro:
        usuarios = usuarios.filter(groups__name=rol_filtro)
        
    grupos = Group.objects.all()

    return render(request, 'panelAdmin/lista_usuarios.html', {
        'usuarios': usuarios,
        'query': query,
        'rol_filtro': rol_filtro,
        'grupos': grupos,
    })

@login_required
@user_passes_test(es_admin)
def editar_usuario(request, user_id):
    usuario_editar = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = AdminUsuarioForm(request.POST, request.FILES, instance=usuario_editar)
        if form.is_valid():
            user_guardado = form.save()
            
            # Actualizar Rol
            rol_nuevo = form.cleaned_data.get('rol')
            user_guardado.groups.clear()
            if rol_nuevo:
                user_guardado.groups.add(rol_nuevo)
            
            # Actualizar foto en PerfilFan
            nueva_foto = form.cleaned_data.get('foto_perfil')
            if nueva_foto:
                perfil, _ = PerfilFan.objects.get_or_create(usuario=user_guardado)
                perfil.foto_perfil = nueva_foto
                perfil.save()
                
            HistorialMovimiento.objects.create(
                usuario=request.user, 
                accion=f'Edición de usuario/foto desde panel Admin: {user_guardado.username}'
            )
            
            messages.success(request, f'¡Usuario {user_guardado.username} actualizado correctamente!')
            return redirect('lista_usuarios')
    else:
        form = AdminUsuarioForm(instance=usuario_editar)
        
    return render(request, 'panelAdmin/editar_usuario.html', {
        'form': form, 
        'usuario_editar': usuario_editar
    })

@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, user_id):
    usuario_eliminar = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username_borrado = usuario_eliminar.username
        usuario_eliminar.delete()
        
        HistorialMovimiento.objects.create(
            usuario=request.user, 
            accion=f'Eliminación de usuario: {username_borrado}'
        )
        
        messages.success(request, f'El usuario {username_borrado} ha sido eliminado.')
        return redirect('lista_usuarios')
        
    return render(request, 'panelAdmin/eliminar_usuario.html', {'usuario_eliminar': usuario_eliminar})