from django import forms
from django.contrib.auth.models import User

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
    # NUEVO: Campo para la foto de perfil
    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-2 focus:outline-none focus:border-indigo-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
        }),
        label="Foto de Perfil (Opcional)"
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

class SolicitarCodigoForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500',
            'placeholder': 'correo@ejemplo.com'
        }),
        label="Correo Electrónico Registrado"
    )

class ValidarCodigoForm(forms.Form):
    codigo = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-center font-mono text-2xl tracking-widest rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500',
            'placeholder': '123456',
            'maxlength': '6'
        }),
        label="Código de 6 dígitos"
    )

class NuevaPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500',
            'placeholder': '••••••••'
        }),
        label="Nueva Contraseña"
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500',
            'placeholder': '••••••••'
        }),
        label="Confirmar Nueva Contraseña"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data