from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from .models import Paciente
import io


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'home/dashboard.html')


@login_required(login_url='login')
def pacientes_import(request):
    """Vista para importar pacientes desde Excel"""
    if request.method == 'POST':
        if 'archivo' not in request.FILES:
            messages.error(request, 'Por favor selecciona un archivo')
            return redirect('pacientes_import')
        
        archivo = request.FILES['archivo']
        
        try:
            # Leer el archivo Excel
            contenido = archivo.read()
            workbook = load_workbook(io.BytesIO(contenido))
            worksheet = workbook.active
            
            importados = 0
            actualizados = 0
            errores = 0
            errores_detalles = []
            
            # Iterar desde la fila 2 (fila 1 es encabezado)
            for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
                try:
                    nombre = row[0]
                    apellido = row[1]
                    movil = row[2]
                    
                    if not all([nombre, apellido, movil]):
                        errores += 1
                        errores_detalles.append(f"Fila {row_idx}: Faltan datos obligatorios")
                        continue
                    
                    # Limpiar y validar el móvil
                    movil = str(movil).strip()
                    
                    # Crear o actualizar paciente
                    paciente, creado = Paciente.objects.update_or_create(
                        movil=movil,
                        defaults={
                            'nombre': str(nombre).strip(),
                            'apellido': str(apellido).strip(),
                            'activo': True
                        }
                    )
                    
                    if creado:
                        importados += 1
                    else:
                        actualizados += 1
                        
                except Exception as e:
                    errores += 1
                    errores_detalles.append(f"Fila {row_idx}: {str(e)}")
            
            # Mensaje de éxito
            mensaje = f"✓ Importación completada: {importados} nuevos, {actualizados} actualizados, {errores} errores"
            messages.success(request, mensaje)
            
            if errores_detalles:
                for detalle in errores_detalles[:5]:  # Mostrar primeros 5 errores
                    messages.warning(request, detalle)
                if len(errores_detalles) > 5:
                    messages.warning(request, f"... y {len(errores_detalles) - 5} errores más")
            
            return redirect('pacientes_lista')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')
            return redirect('pacientes_import')
    
    return render(request, 'home/pacientes_import.html')


@login_required(login_url='login')
def pacientes_lista(request):
    """Vista para listar pacientes"""
    pacientes = Paciente.objects.all()
    
    # Filtros
    filtro_estado = request.GET.get('estado', '')
    if filtro_estado:
        pacientes = pacientes.filter(activo=filtro_estado == 'activo')
    
    busqueda = request.GET.get('q', '')
    if busqueda:
        pacientes = pacientes.filter(
            nombre__icontains=busqueda) | pacientes.filter(
            apellido__icontains=busqueda) | pacientes.filter(
            movil__icontains=busqueda
        )
    
    contexto = {
        'pacientes': pacientes,
        'total': Paciente.objects.count(),
        'activos': Paciente.objects.filter(activo=True).count(),
        'inactivos': Paciente.objects.filter(activo=False).count(),
    }
    
    return render(request, 'home/pacientes_lista.html', contexto)


@login_required(login_url='login')
def paciente_toggle(request, pk):
    """Toggle para activar/desactivar paciente"""
    try:
        paciente = Paciente.objects.get(pk=pk)
        paciente.activo = not paciente.activo
        paciente.save()
        
        estado = "activado" if paciente.activo else "desactivado"
        messages.success(request, f'Paciente {estado} correctamente')
    except Paciente.DoesNotExist:
        messages.error(request, 'Paciente no encontrado')
    
    return redirect('pacientes_lista')


@login_required(login_url='login')
def descargar_plantilla_excel(request):
    """Descargar plantilla Excel para importar pacientes"""
    # Crear workbook
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Pacientes"
    
    # Configurar encabezados
    headers = ['Nombre', 'Apellido', 'Móvil']
    header_fill = PatternFill(start_color="0C6E68", end_color="0C6E68", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    for col_num, header in enumerate(headers, 1):
        cell = worksheet.cell(row=1, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Agregar ejemplos
    ejemplos = [
        ['Juan', 'Pérez', '+593991234567'],
        ['María', 'González', '+593992345678'],
        ['Carlos', 'López', '+593993456789'],
    ]
    
    for row_num, ejemplo in enumerate(ejemplos, 2):
        for col_num, valor in enumerate(ejemplo, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = valor
            cell.alignment = Alignment(horizontal="left", vertical="center")
    
    # Ajustar ancho de columnas
    worksheet.column_dimensions['A'].width = 25
    worksheet.column_dimensions['B'].width = 25
    worksheet.column_dimensions['C'].width = 20
    
    # Guardar en memoria
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="plantilla_pacientes.xlsx"'
    
    workbook.save(response)
    return response

