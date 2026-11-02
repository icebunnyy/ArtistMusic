from django import forms
from django.contrib.auth.models import User
from .models import PerfilFan

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-500', 'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-500', 'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-emerald-500', 'placeholder': 'correo@ejemplo.com'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico'
        }

class EditarPerfilFanForm(forms.ModelForm):
    class Meta:
        model = PerfilFan
        fields = ['foto_perfil']
        widgets = {
            'foto_perfil': forms.FileInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-2 focus:outline-none focus:border-emerald-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-emerald-500/20 file:text-emerald-400 hover:file:bg-emerald-500/30'
            })
        }
        labels = {
            'foto_perfil': 'Cambiar Foto de Perfil'
        }