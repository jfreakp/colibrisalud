
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Area(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, blank=True, help_text="Teléfono principal del área")
    icono = models.CharField(max_length=50, blank=True, help_text="Nombre del icono Material Symbols")
    color = models.CharField(max_length=20, blank=True, help_text="Clase de color Tailwind, ej: bg-primary/20")
    descripcion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Áreas'

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    movil = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField(default=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = 'Pacientes'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('atendida', 'Atendida'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['fecha', 'hora']
        verbose_name_plural = 'Citas'
    
    def __str__(self):
        return f"Cita de {self.paciente} - {self.fecha} {self.hora}"


class NumeroNotificacion(models.Model):
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True, related_name='numeros')
    numero = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, help_text="Ej: WhatsApp principal, SMS emergencias, etc.")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = 'Números de Notificación'

    def __str__(self):
        desc = f" - {self.descripcion}" if self.descripcion else ""
        return f"{self.numero}{desc}"


class Mensaje(models.Model):
    TIPO_CHOICES = [
        ('confirmacion', 'Confirmación de cita'),
        ('recordatorio', 'Recordatorio'),
        ('cancelacion', 'Cancelación'),
        ('cambio', 'Cambio de cita'),
        ('otro', 'Otro'),
    ]
    
    titulo = models.CharField(max_length=100)
    contenido = models.TextField(help_text="Contenido del mensaje a enviar")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='otro')
    activo = models.BooleanField(default=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = 'Mensajes'
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"


class Notificacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('fallida', 'Fallida'),
        ('entregada', 'Entregada'),
    ]
    
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='notificaciones')
    numero = models.ForeignKey(NumeroNotificacion, on_delete=models.SET_NULL, null=True, related_name='notificaciones')
    mensaje = models.ForeignKey(Mensaje, on_delete=models.SET_NULL, null=True, related_name='notificaciones')
    
    numero_destinatario = models.CharField(max_length=20, help_text="Número del paciente a notificar")
    numero_origen = models.CharField(max_length=20, blank=True, help_text="Número desde el cual se envía")
    
    fecha_programada = models.DateTimeField(help_text="Fecha y hora de la notificación")
    fecha_enviada = models.DateTimeField(null=True, blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    response_whatsapp = models.JSONField(default=dict, blank=True, help_text="Respuesta de la API de WhatsApp")
    mensaje_error = models.TextField(blank=True, help_text="Mensaje de error si la notificación falló")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_programada']
        verbose_name_plural = 'Notificaciones'
    
    def clean(self):
        """Validar que no se notifique de fechas pasadas"""
        if self.fecha_programada:
            # Comparar solo la fecha, no la hora exacta
            fecha_hoy = timezone.now().date()
            fecha_notificacion = self.fecha_programada.date()
            
            if fecha_notificacion < fecha_hoy:
                raise ValidationError({
                    'fecha_programada': 'No se puede programar notificaciones para fechas pasadas. La cita ya no está disponible para notificar.'
                })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Notificación para {self.numero_destinatario} - {self.fecha_programada.strftime('%d/%m/%Y %H:%M')}"
