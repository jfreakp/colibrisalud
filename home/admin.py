from django.contrib import admin
from .models import Paciente, Cita


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
