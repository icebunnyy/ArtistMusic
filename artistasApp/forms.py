from django import forms
from django.contrib.auth.models import User
from .models import Artista, Album, Evento, OPCIONES_COLOR


# Formulario de Registro de Usuarios
class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500',
            'placeholder': '••••••••'
        }),
        label="Contraseña"
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500',
            'placeholder': '••••••••'
        }),
        label="Confirmar Contraseña"
    )
    rol = forms.ChoiceField(
        choices=[('Usuario', 'Usuario Normal'), ('Artista', 'Artista')],
        widget=forms.Select(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500'
        }),
        label="Tipo de Cuenta"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'usuario123'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'correo@ejemplo.com'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'Apellido'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


# Formulario Mantenedor Artista
class ArtistaForm(forms.ModelForm):
    tag_color = forms.ChoiceField(
        choices=OPCIONES_COLOR,
        label="Color Distintivo del Género",
        widget=forms.Select(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500'
        })
    )

    class Meta:
        model = Artista
        fields = ['id', 'nombre', 'genero', 'tag_color', 'imagen', 'oyentes_mensuales', 'pais', 'biografia']
        labels = {
            'id': 'ID Único / Slug (ej: nicki-minaj)',
            'nombre': 'Nombre del Artista',
            'genero': 'Género Musical',
            'imagen': 'Subir Foto de Perfil',
            'oyentes_mensuales': 'Oyentes Mensuales (ej: 45.2M)',
            'pais': 'País de Origen',
            'biografia': 'Biografía'
        }
        widgets = {
            'id': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: nicki-minaj'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'Nombre artístico'}),
            'genero': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: Hip-Hop / Pop'}),
            'imagen': forms.FileInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-300 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-500'}),
            'oyentes_mensuales': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: 65.4M'}),
            'pais': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: Chile'}),
            'biografia': forms.Textarea(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'rows': 3, 'placeholder': 'Escribe una breve reseña...'}),
        }


# Formulario Mantenedor Álbum
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artista', 'titulo', 'lanzamiento', 'portada', 'canciones']
        labels = {
            'artista': 'Artista Pertinente',
            'titulo': 'Título del Álbum',
            'lanzamiento': 'Año de Lanzamiento',
            'portada': 'Subir Portada del Álbum',
            'canciones': 'Lista de Canciones (Separadas por comas)'
        }
        widgets = {
            'artista': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500'}),
            'titulo': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'Nombre del álbum'}),
            'lanzamiento': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': '2026'}),
            'portada': forms.FileInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-300 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-pink-600 file:text-white hover:file:bg-pink-500'}),
            'canciones': forms.Textarea(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'rows': 3, 'placeholder': 'Canción 1, Canción 2, Canción 3...'}),
        }


# Formulario Mantenedor Evento
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['artista', 'lugar', 'ciudad', 'fecha', 'estado']
        labels = {
            'artista': 'Artista Pertinente',
            'lugar': 'Lugar / Recinto',
            'ciudad': 'Ciudad',
            'fecha': 'Fecha del Evento',
            'estado': 'Estado de Entradas'
        }
        widgets = {
            'artista': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500'}),
            'lugar': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: Movistar Arena'}),
            'ciudad': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: Santiago'}),
            'fecha': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: 15 de Noviembre 2026'}),
            'estado': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500', 'placeholder': 'ej: Entradas Disponibles'}),
        }