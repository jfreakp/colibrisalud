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
]
