from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pacientes/', views.pacientes_lista, name='pacientes_lista'),
    path('pacientes/import/', views.pacientes_import, name='pacientes_import'),
    path('pacientes/descargar-plantilla/', views.descargar_plantilla_excel, name='descargar_plantilla'),
    path('pacientes/<int:pk>/toggle/', views.paciente_toggle, name='paciente_toggle'),
    path('citas/', views.citas_lista, name='citas_lista'),
    path('citas/import/', views.citas_import, name='citas_import'),
    path('citas/descargar-plantilla/', views.descargar_plantilla_citas, name='descargar_plantilla_citas'),
    path('numeros/', views.numeros_lista, name='numeros_lista'),
    path('numeros/crear/', views.numero_crear, name='numero_crear'),
    path('numeros/<int:pk>/editar/', views.numero_editar, name='numero_editar'),
    path('numeros/<int:pk>/eliminar/', views.numero_eliminar, name='numero_eliminar'),
    path('numeros/<int:pk>/toggle/', views.numero_toggle, name='numero_toggle'),
    path('mensajes/', views.mensajes_lista, name='mensajes_lista'),
    path('mensajes/crear/', views.mensaje_crear, name='mensaje_crear'),
    path('mensajes/<int:pk>/editar/', views.mensaje_editar, name='mensaje_editar'),
    path('mensajes/<int:pk>/eliminar/', views.mensaje_eliminar, name='mensaje_eliminar'),
    path('mensajes/<int:pk>/toggle/', views.mensaje_toggle, name='mensaje_toggle'),
    path('notificaciones/', views.notificaciones_lista, name='notificaciones_lista'),
    path('notificaciones/crear/', views.notificacion_crear, name='notificacion_crear'),
    path('notificaciones/<int:pk>/editar/', views.notificacion_editar, name='notificacion_editar'),
    path('notificaciones/<int:pk>/eliminar/', views.notificacion_eliminar, name='notificacion_eliminar'),
    path('notificaciones/<int:pk>/enviar/', views.notificacion_enviar, name='notificacion_enviar'),
]
