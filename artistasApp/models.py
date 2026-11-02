from django.db import models
from django.contrib.auth.models import User

# Opciones de colores amigables para las etiquetas de géneros
OPCIONES_COLOR = [
    ('text-indigo-400 border-indigo-500/30 bg-indigo-500/10', 'Azul / Índigo'),
    ('text-pink-400 border-pink-500/30 bg-pink-500/10', 'Rosa / Magenta'),
    ('text-purple-400 border-purple-500/30 bg-purple-500/10', 'Púrpura / Violeta'),
    ('text-emerald-400 border-emerald-500/30 bg-emerald-500/10', 'Verde / Esmeralda'),
    ('text-amber-400 border-amber-500/30 bg-amber-500/10', 'Amarillo / Ámbar'),
    ('text-rose-400 border-rose-500/30 bg-rose-500/10', 'Rojo / Rosa Intenso'),
]

class Artista(models.Model):
    # Forzamos el cotejamiento directamente en el campo de texto principal
    id = models.CharField(max_length=50, primary_key=True, db_collation='utf8mb4_unicode_ci')
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='perfil_artista')
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50, blank=True, null=True)
    tag_color = models.CharField(
        max_length=150, 
        choices=OPCIONES_COLOR, 
        default='text-indigo-400 border-indigo-500/30 bg-indigo-500/10'
    )
    imagen = models.ImageField(upload_to='artistas/', blank=True, null=True)
    oyentes_mensuales = models.CharField(max_length=20, blank=True, null=True, default='0')
    pais = models.CharField(max_length=50, blank=True, null=True, default='Chile')
    biografia = models.TextField(blank=True, null=True)

    @property
    def imagen_url(self):
        if not self.imagen:
            return "/static/artistasApp/images/default.png"
        
        img_str = str(self.imagen)
        
        # 1. Si es un enlace externo de internet (http...)
        if img_str.startswith('http'):
            return img_str
            
        # 2. Si es SOLO el nombre del archivo sin carpetas
        if not '/' in img_str and not '\\' in img_str:
            return f"/static/artistasApp/images/{img_str}"
            
        # 3. Si en el texto ya viene la ruta de static
        if 'artistasApp' in img_str:
            return f"/static/{img_str}"
            
        # 4. Si tiene subcarpetas, significa que fue subida desde el formulario
        try:
            return self.imagen.url
        except ValueError:
            return f"/media/{img_str}"

    @property
    def albumes(self):
        lista_albumes = []
        for alb in self.albumes_set.all():
            canciones_list = alb.canciones.split(',') if alb.canciones else []
            lista_albumes.append({
                'id': alb.id,
                'titulo': alb.titulo,
                'lanzamiento': alb.lanzamiento,
                'portada': alb.portada_url,  # <-- Usamos la nueva propiedad inteligente del álbum
                'canciones': [c.strip() for c in canciones_list]
            })
        return lista_albumes

    @property
    def eventos(self):
        return self.eventos_set.all()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'artistas'


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, db_column='artista_id', related_name='albumes_set')
    titulo = models.CharField(max_length=100)
    lanzamiento = models.CharField(max_length=10, blank=True, null=True)
    portada = models.ImageField(upload_to='albumes/', blank=True, null=True)
    canciones = models.TextField(blank=True, null=True)

    @property
    def portada_url(self):
        if not self.portada:
            return "/static/artistasApp/images/default_album.png"
        
        img_str = str(self.portada)
        
        # 1. Si es un enlace externo de internet (http...)
        if img_str.startswith('http'):
            return img_str
            
        # 2. Si es SOLO el nombre del archivo sin carpetas
        if not '/' in img_str and not '\\' in img_str:
            return f"/static/artistasApp/images/{img_str}"
            
        # 3. Si en el texto ya viene la ruta de static
        if 'artistasApp' in img_str:
            return f"/static/{img_str}"
            
        # 4. Si fue subida desde el panel
        try:
            return self.portada.url
        except ValueError:
            return f"/media/{img_str}"

    def __str__(self):
        return f"{self.titulo} - {self.artista.nombre}"

    class Meta:
        db_table = 'albumes'


class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE, db_column='artista_id', related_name='eventos_set')
    lugar = models.CharField(max_length=150, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True, default='Entradas Disponibles')

    def __str__(self):
        return f"{self.lugar} - {self.artista.nombre}"

    class Meta:
        db_table = 'eventos'


class HistorialMovimiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.accion} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"

    class Meta:
        db_table = 'historial_movimientos'