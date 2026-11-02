from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from fansApp.models import PerfilFan
from .models import Artista, Album, Evento, HistorialMovimiento
from .forms import ArtistaForm, AlbumForm, EventoForm


def es_admin(user):
    return user.is_authenticated and (user.groups.filter(name='Administrador').exists() or user.is_superuser)

def es_artista(user):
    return user.is_authenticated and user.groups.filter(name='Artista').exists()

def registrar_accion(usuario, accion):
    HistorialMovimiento.objects.create(usuario=usuario, accion=accion)


# --- VISTAS PÚBLICAS Y BÚSQUEDA ---

def inicio_artistas(request):
    query = request.GET.get('q', '')
    if query:
        artistas = Artista.objects.filter(
            Q(nombre__icontains=query) | Q(genero__icontains=query)
        )
    else:
        artistas = Artista.objects.all()
        
    return render(request, 'artistas/inicio.html', {'artistas': artistas, 'query': query})


def detalle_artista(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    
    lo_sigue = False
    albumes_guardados = []
    
    if request.user.is_authenticated and not request.user.groups.filter(name='Administrador').exists():
        perfil, created = PerfilFan.objects.get_or_create(usuario=request.user)
        
        # Extraemos los IDs puros y comparamos en Python para evitar el error de MySQL
        artistas_fav_ids = list(perfil.artistas_favoritos.values_list('id', flat=True))
        lo_sigue = str(artista.id) in [str(aid) for aid in artistas_fav_ids]
        
        albumes_guardados = list(perfil.albumes_guardados.values_list('id', flat=True))

    return render(request, 'artistas/detalle.html', {
        'artista': artista,
        'lo_sigue': lo_sigue,
        'albumes_guardados': albumes_guardados
    })
# --- DASHBOARD DE ARTISTA ---

@login_required
@user_passes_test(es_artista)
def dashboard_artista(request):
    try:
        mi_artista = request.user.perfil_artista
    except (Artista.DoesNotExist, AttributeError):
        mi_artista = None

    albumes = mi_artista.albumes_set.all() if mi_artista else []
    eventos = mi_artista.eventos_set.all() if mi_artista else []

    return render(request, 'artistas/dashboard_artista.html', {
        'mi_artista': mi_artista,
        'albumes': albumes,
        'eventos': eventos
    })


# --- MANTENEDOR DE ARTISTAS ---

@login_required
def crear_artista(request):
    if es_artista(request.user) and hasattr(request.user, 'perfil_artista') and request.user.perfil_artista:
        messages.info(request, 'Ya tienes un perfil de artista registrado.')
        return redirect('dashboard_artista')

    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES)
        if form.is_valid():
            artista = form.save(commit=False)
            if es_artista(request.user):
                artista.usuario = request.user
            artista.save()
            
            registrar_accion(request.user, f'Creó la ficha de artista: {artista.nombre}')
            messages.success(request, 'Perfil de artista creado con éxito.')
            return redirect('dashboard_artista' if es_artista(request.user) else 'inicio_artistas')
    else:
        form = ArtistaForm()
    return render(request, 'artistas/form_generico.html', {'form': form, 'titulo': 'Crear Ficha de Artista'})


@login_required
def editar_artista(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    
    if not (es_admin(request.user) or artista.usuario == request.user):
        messages.error(request, 'No tienes permiso para modificar este artista.')
        return redirect('inicio_artistas')

    if request.method == 'POST':
        form = ArtistaForm(request.POST, request.FILES, instance=artista)
        if form.is_valid():
            form.save()
            registrar_accion(request.user, f'Modificó los datos del artista: {artista.nombre}')
            messages.success(request, 'Artista actualizado correctamente.')
            return redirect('dashboard_artista' if es_artista(request.user) else 'inicio_artistas')
    else:
        form = ArtistaForm(instance=artista)
    return render(request, 'artistas/form_generico.html', {'form': form, 'titulo': f'Editar Artista: {artista.nombre}'})


@login_required
def eliminar_artista(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    
    if not (es_admin(request.user) or artista.usuario == request.user):
        messages.error(request, 'No tienes permiso para eliminar este artista.')
        return redirect('inicio_artistas')

    nombre = artista.nombre
    artista.delete()
    registrar_accion(request.user, f'Eliminó al artista: {nombre}')
    messages.success(request, f'El artista {nombre} ha sido eliminado.')
    return redirect('inicio_artistas')


# --- MANTENEDOR DE ÁLBUMES ---

@login_required
def crear_album(request):
    try:
        mi_artista = request.user.perfil_artista
    except (Artista.DoesNotExist, AttributeError):
        mi_artista = None

    if es_artista(request.user) and not mi_artista and not es_admin(request.user):
        messages.warning(request, 'Primero debes registrar tu ficha de artista.')
        return redirect('crear_artista')

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        
        if mi_artista and not es_admin(request.user):
            form.fields['artista'].queryset = Artista.objects.filter(id=mi_artista.id)

        if form.is_valid():
            album = form.save(commit=False)
            if mi_artista and not es_admin(request.user):
                album.artista = mi_artista
            album.save()
            
            registrar_accion(request.user, f'Añadió el álbum: {album.titulo}')
            messages.success(request, 'Álbum publicado exitosamente.')
            return redirect('dashboard_artista' if es_artista(request.user) else 'inicio_artistas')
    else:
        form = AlbumForm()
        
        if mi_artista and not es_admin(request.user):
            form.fields['artista'].queryset = Artista.objects.filter(id=mi_artista.id)
            form.fields['artista'].empty_label = None
            form.fields['artista'].initial = mi_artista

    return render(request, 'artistas/form_generico.html', {'form': form, 'titulo': 'Añadir Nuevo Álbum'})


@login_required
def eliminar_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    
    if not (es_admin(request.user) or (hasattr(request.user, 'perfil_artista') and album.artista == request.user.perfil_artista)):
        messages.error(request, 'No tienes permiso para eliminar este álbum.')
        return redirect('inicio_artistas')

    titulo = album.titulo
    album.delete()
    registrar_accion(request.user, f'Eliminó el álbum: {titulo}')
    messages.success(request, f'Álbum "{titulo}" eliminado.')
    return redirect('dashboard_artista' if es_artista(request.user) else 'inicio_artistas')


# --- MANTENEDOR DE EVENTOS ---

@login_required
def crear_evento(request):
    try:
        mi_artista = request.user.perfil_artista
    except (Artista.DoesNotExist, AttributeError):
        mi_artista = None

    if es_artista(request.user) and not mi_artista and not es_admin(request.user):
        messages.warning(request, 'Primero debes registrar tu ficha de artista.')
        return redirect('crear_artista')

    if request.method == 'POST':
        form = EventoForm(request.POST)
        
        if mi_artista and not es_admin(request.user):
            form.fields['artista'].queryset = Artista.objects.filter(id=mi_artista.id)

        if form.is_valid():
            evento = form.save(commit=False)
            if mi_artista and not es_admin(request.user):
                evento.artista = mi_artista
            evento.save()
            
            registrar_accion(request.user, f'Creó evento en {evento.lugar}')
            messages.success(request, 'Evento/Concierto publicado exitosamente.')
            return redirect('dashboard_artista' if es_artista(request.user) else 'inicio_artistas')
    else:
        form = EventoForm()
        
        if mi_artista and not es_admin(request.user):
            form.fields['artista'].queryset = Artista.objects.filter(id=mi_artista.id)
            form.fields['artista'].empty_label = None
            form.fields['artista'].initial = mi_artista

    return render(request, 'artistas/form_generico.html', {'form': form, 'titulo': 'Añadir Nuevo Concierto/Evento'})