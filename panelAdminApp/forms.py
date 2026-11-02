from django import forms
from django.contrib.auth.models import User, Group
from fansApp.models import PerfilFan

class AdminUsuarioForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        empty_label="Sin rol asignado",
        widget=forms.Select(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-amber-500'
        }),
        label="Rol de la Cuenta"
    )

    # NUEVO: Campo para que el admin modifique la foto
    foto_perfil = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-2 focus:outline-none focus:border-amber-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-amber-500/20 file:text-amber-400 hover:file:bg-amber-500/30'
        }),
        label="Cambiar Foto de Perfil"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-amber-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-amber-500'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-amber-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-800 text-slate-100 text-sm rounded-xl px-4 py-3 focus:outline-none focus:border-amber-500'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-500 bg-slate-900 border-slate-800 rounded focus:ring-amber-500'}),
        }
        labels = {
            'is_active': '¿Usuario Activo? (Si se desmarca, no podrá iniciar sesión)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.groups.exists():
            self.initial['rol'] = self.instance.groups.first()
        
        # Cargar foto existente en la vista previa
        if self.instance.pk and hasattr(self.instance, 'perfil_fan'):
            self.initial['foto_perfil'] = self.instance.perfil_fan.foto_perfil