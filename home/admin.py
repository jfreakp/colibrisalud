from django.contrib import admin
from .models import Paciente, Cita, NumeroNotificacion, Mensaje, Notificacion


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'movil', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre', 'apellido', 'movil')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'hora', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha', 'fecha_creacion')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'paciente__movil')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    date_hierarchy = 'fecha'


@admin.register(NumeroNotificacion)
class NumeroNotificacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'descripcion', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('numero', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'activo', 'fecha_creacion')
    list_filter = ('tipo', 'activo', 'fecha_creacion')
    search_fields = ('titulo', 'contenido')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('numero_destinatario', 'cita', 'estado', 'fecha_programada', 'fecha_enviada')
    list_filter = ('estado', 'fecha_programada', 'fecha_enviada', 'fecha_creacion')
    search_fields = ('numero_destinatario', 'cita__paciente__nombre', 'cita__paciente__movil')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'response_whatsapp')
    date_hierarchy = 'fecha_programada'
    
    fieldsets = (
        ('Información de Cita', {
            'fields': ('cita', 'numero_destinatario', 'numero_origen')
        }),
        ('Configuración de Notificación', {
            'fields': ('numero', 'mensaje', 'fecha_programada')
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_enviada', 'mensaje_error')
        }),
        ('WhatsApp API', {
            'fields': ('response_whatsapp',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
