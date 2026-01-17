from django.db import models


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
