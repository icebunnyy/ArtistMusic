import os
import django

# Cargar la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group

# Definición de los 3 perfiles requeridos por la pauta
grupos = ['Administrador', 'Artista', 'Usuario']

for nombre_grupo in grupos:
    grupo, created = Group.objects.get_or_create(name=nombre_grupo)
    if created:
        print(f'✅ Grupo "{nombre_grupo}" creado con éxito.')
    else:
        print(f'ℹ️ El grupo "{nombre_grupo}" ya existía.')