from django.db import models
from django.contrib.auth.models import User
from artistasApp.models import Artista, Album

class PerfilFan(models.Model):
    # Vinculamos este perfil al usuario normal de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_fan')
    
    # Un fan puede tener muchos artistas favoritos, y un artista muchos fans
    artistas_favoritos = models.ManyToManyField(Artista, blank=True, related_name='seguidores')
    
    # Un fan puede guardar muchos álbumes
    albumes_guardados = models.ManyToManyField(Album, blank=True, related_name='guardados_por')

    # 👇 ¡AQUÍ ESTÁ EL CAMPO QUE FALTABA! 👇
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    # 👇 ¡Y AQUÍ FALTABA EL @property! 👇
    @property
    def imagen_url(self):
        if not self.foto_perfil:
            return "/static/artistasApp/images/default.png"
        
        img_str = str(self.foto_perfil)
        if img_str.startswith('http'):
            return img_str
        if not '/' in img_str and not '\\' in img_str:
            return f"/static/artistasApp/images/{img_str}"
        try:
            return self.foto_perfil.url
        except ValueError:
            return f"/media/{img_str}"

    def __str__(self):
        return f"Perfil de Fan: {self.usuario.username}"

    class Meta:
        db_table = 'perfiles_fans'


class Notificacion(models.Model):
    # A quién va dirigida la notificación
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Opcional: un enlace para que al hacer clic los lleve al álbum o artista nuevo
    enlace_destino = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        estado = "Leída" if self.leida else "Nueva"
        return f"Notificación para {self.usuario.username} ({estado})"

    class Meta:
        db_table = 'notificaciones_fans'
        ordering = ['-fecha_creacion'] # Las más nuevas primero