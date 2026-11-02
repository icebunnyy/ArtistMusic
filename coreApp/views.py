import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group  # <-- AQUÍ IMPORTAMOS USER Y GROUP
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from artistasApp.models import HistorialMovimiento, Artista
from fansApp.models import PerfilFan
from .forms import RegistroUsuarioForm, SolicitarCodigoForm, ValidarCodigoForm, NuevaPasswordForm


def registrar_accion(usuario, accion):
    HistorialMovimiento.objects.create(usuario=usuario, accion=accion)


# --- PORTADA GENERAL ---

def index_general(request):
    artistas_destacados = Artista.objects.all()[:4]
    return render(request, 'core/index_general.html', {'artistas': artistas_destacados})


# --- AUTENTICACIÓN ---

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            nombre_rol = form.cleaned_data['rol']
            try:
                grupo = Group.objects.get(name=nombre_rol)
                user.groups.add(grupo)
            except Group.DoesNotExist:
                pass

            if nombre_rol == 'Usuario':
                PerfilFan.objects.create(
                    usuario=user,
                    foto_perfil=form.cleaned_data.get('foto_perfil')
                )

            login(request, user)
            registrar_accion(user, f'Registro de nuevo usuario con rol {nombre_rol}')
            messages.success(request, f'¡Bienvenido/a, {user.username}! Tu cuenta ha sido creada.')
            
            if nombre_rol == 'Artista':
                return redirect('dashboard_artista')
            return redirect('dashboard_fan')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'core/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                registrar_accion(user, 'Inicio de sesión exitoso')
                messages.success(request, f'Sesión iniciada como {username}.')
                
                if user.is_superuser or user.groups.filter(name='Administrador').exists():
                    return redirect('dashboard_admin')
                elif user.groups.filter(name='Artista').exists():
                    return redirect('dashboard_artista')
                else:
                    return redirect('inicio_artistas')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        registrar_accion(request.user, 'Cierre de sesión')
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


# --- RECUPERACIÓN DE CONTRASEÑA ---

def solicitar_codigo_view(request):
    if request.method == 'POST':
        form = SolicitarCodigoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            
            if user:
                codigo = str(random.randint(100000, 999999))
                
                request.session['reset_user_id'] = user.id
                request.session['reset_code'] = codigo
                request.session['reset_verified'] = False

                asunto = "Código de recuperación de contraseña - ArtistMusic"
                mensaje = f"Hola {user.username},\n\nTu código de verificación para restablecer la contraseña es: {codigo}\n\nSi no solicitaste este cambio, ignora este mensaje."
                
                send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [email])
                
                messages.success(request, f"Hemos enviado un código de 6 dígitos a {email}.")
                return redirect('validar_codigo')
            else:
                messages.error(request, "No existe ninguna cuenta asociada a este correo electrónico.")
    else:
        form = SolicitarCodigoForm()

    return render(request, 'core/solicitar_codigo.html', {'form': form})


def validar_codigo_view(request):
    if 'reset_user_id' not in request.session or 'reset_code' not in request.session:
        messages.error(request, "Sesión inválida o expirada. Solicita un nuevo código.")
        return redirect('recuperar_password')

    if request.method == 'POST':
        form = ValidarCodigoForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo']
            codigo_guardado = request.session.get('reset_code')

            if codigo_ingresado == codigo_guardado:
                request.session['reset_verified'] = True
                messages.success(request, "Código verificado correctamente. Ingresa tu nueva contraseña.")
                return redirect('nueva_password')
            else:
                messages.error(request, "El código ingresado es incorrecto.")
    else:
        form = ValidarCodigoForm()

    return render(request, 'core/validar_codigo.html', {'form': form})


def nueva_password_view(request):
    if not request.session.get('reset_verified') or 'reset_user_id' not in request.session:
        messages.error(request, "Acceso no autorizado. Primero debes validar tu código.")
        return redirect('recuperar_password')

    if request.method == 'POST':
        form = NuevaPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session['reset_user_id']
            user = User.objects.get(id=user_id)
            
            nueva_pass = form.cleaned_data['password']
            user.set_password(nueva_pass)
            user.save()

            registrar_accion(user, 'Restablecimiento de contraseña mediante correo electrónico')

            del request.session['reset_user_id']
            del request.session['reset_code']
            del request.session['reset_verified']

            messages.success(request, "¡Tu contraseña ha sido actualizada con éxito! Ya puedes iniciar sesión.")
            return redirect('login')
    else:
        form = NuevaPasswordForm()

    return render(request, 'core/nueva_password.html', {'form': form})