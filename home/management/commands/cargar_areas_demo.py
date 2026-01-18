from django.core.management.base import BaseCommand
from home.models import Area

class Command(BaseCommand):
    help = 'Crea 10 áreas de ejemplo para pruebas'

    def handle(self, *args, **kwargs):
        ejemplos = [
            dict(nombre='Cardiología', telefono='+593991234567', icono='favorite', color='#f87171', descripcion='Área de cardiología'),
            dict(nombre='Emergencias', telefono='+593998765432', icono='emergency', color='#fbbf24', descripcion='Atención de emergencias'),
            dict(nombre='Pediatría', telefono='+593997654321', icono='child_care', color='#60a5fa', descripcion='Área pediátrica'),
            dict(nombre='Laboratorio', telefono='+593995432187', icono='science', color='#34d399', descripcion='Laboratorio clínico'),
            dict(nombre='Rayos X', telefono='+593994321876', icono='radiology', color='#a78bfa', descripcion='Servicio de rayos X'),
            dict(nombre='Farmacia', telefono='+593993218765', icono='local_pharmacy', color='#f472b6', descripcion='Farmacia interna'),
            dict(nombre='Ginecología', telefono='+593992187654', icono='pregnant_woman', color='#facc15', descripcion='Área de ginecología'),
            dict(nombre='Traumatología', telefono='+593991876543', icono='accessible', color='#38bdf8', descripcion='Traumatología y ortopedia'),
            dict(nombre='Oncología', telefono='+593991765432', icono='healing', color='#f472b6', descripcion='Área de oncología'),
            dict(nombre='UCI', telefono='+593991654321', icono='monitor_heart', color='#f87171', descripcion='Unidad de cuidados intensivos'),
        ]
        for e in ejemplos:
            Area.objects.update_or_create(nombre=e['nombre'], defaults=e)
        self.stdout.write(self.style.SUCCESS('10 áreas de ejemplo creadas o actualizadas.'))
