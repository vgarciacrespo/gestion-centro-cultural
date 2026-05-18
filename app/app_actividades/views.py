from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F
from .models import Actividad, Usuario, Monitor, Sala
from .forms import ActividadForm, UsuarioForm, MonitorForm, SalaForm, InscripcionForm


def home(request):
    total_actividades = Actividad.objects.count()
    total_usuarios = Usuario.objects.count()
    total_monitores = Monitor.objects.count()
    total_salas = Sala.objects.count()
    actividades_recientes = Actividad.objects.select_related('monitor').order_by('-id')[:5]
    return render(request, 'app_actividades/home.html', {
        'total_actividades': total_actividades,
        'total_usuarios': total_usuarios,
        'total_monitores': total_monitores,
        'total_salas': total_salas,
        'actividades_recientes': actividades_recientes,
    })



def lista_actividades(request):
    tipo = request.GET.get('tipo', '')
    monitor = request.GET.get('monitor', '')
    actividades = Actividad.objects.select_related('monitor').all()
    if tipo:
        actividades = actividades.filter(tipo__icontains=tipo)
    if monitor:
        actividades = actividades.filter(monitor__id=monitor)
    monitores = Monitor.objects.all()
    return render(request, 'app_actividades/actividades/lista_actividades.html', {
        'actividades': actividades,
        'monitores': monitores,
        'filtro_tipo': tipo,
        'filtro_monitor': monitor,
    })

def nueva_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_actividades')
    else:
        form = ActividadForm()
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Nueva Actividad', 'volver': 'lista_actividades'})

def detalle_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    return render(request, 'app_actividades/actividades/detalle_actividad.html', {'actividad': actividad})

def editar_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            return redirect('detalle_actividad', id=id)
    else:
        form = ActividadForm(instance=actividad)
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Editar Actividad', 'volver': 'lista_actividades'})

def eliminar_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    if request.method == 'POST':
        actividad.delete()
        return redirect('lista_actividades')
    return render(request, 'app_actividades/confirmar_eliminar.html', {'objeto': actividad, 'tipo': 'actividad', 'volver': 'lista_actividades'})



def lista_usuarios(request):
    actividad_id = request.GET.get('actividad', '')
    usuarios = Usuario.objects.prefetch_related('actividades').all()
    actividades = Actividad.objects.all()
    if actividad_id:
        usuarios = usuarios.filter(actividades__id=actividad_id)
    return render(request, 'app_actividades/usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
        'actividades': actividades,
        'filtro_actividad': actividad_id,
    })

def nuevo_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Nuevo Usuario', 'volver': 'lista_usuarios'})

def detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    return render(request, 'app_actividades/usuarios/detalle_usuario.html', {'usuario': usuario})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('detalle_usuario', id=id)
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Editar Usuario', 'volver': 'lista_usuarios'})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'app_actividades/confirmar_eliminar.html', {'objeto': usuario, 'tipo': 'usuario', 'volver': 'lista_usuarios'})



def lista_monitores(request):
    monitores = Monitor.objects.all()
    return render(request, 'app_actividades/monitores/lista_monitores.html', {'monitores': monitores})

def nuevo_monitor(request):
    if request.method == 'POST':
        form = MonitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_monitores')
    else:
        form = MonitorForm()
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Nuevo Monitor', 'volver': 'lista_monitores'})

def detalle_monitor(request, id):
    monitor = get_object_or_404(Monitor, pk=id)
    actividades = monitor.actividades.all()
    return render(request, 'app_actividades/monitores/detalle_monitor.html', {'monitor': monitor, 'actividades': actividades})

def editar_monitor(request, id):
    monitor = get_object_or_404(Monitor, pk=id)
    if request.method == 'POST':
        form = MonitorForm(request.POST, instance=monitor)
        if form.is_valid():
            form.save()
            return redirect('detalle_monitor', id=id)
    else:
        form = MonitorForm(instance=monitor)
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Editar Monitor', 'volver': 'lista_monitores'})

def eliminar_monitor(request, id):
    monitor = get_object_or_404(Monitor, pk=id)
    if request.method == 'POST':
        monitor.delete()
        return redirect('lista_monitores')
    return render(request, 'app_actividades/confirmar_eliminar.html', {'objeto': monitor, 'tipo': 'monitor', 'volver': 'lista_monitores'})


def lista_salas(request):
    salas = Sala.objects.select_related('responsable').all()
    return render(request, 'app_actividades/salas/lista_salas.html', {'salas': salas})

def nueva_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_salas')
    else:
        form = SalaForm()
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Nueva Sala', 'volver': 'lista_salas'})

def detalle_sala(request, id):
    sala = get_object_or_404(Sala, pk=id)
    return render(request, 'app_actividades/salas/detalle_sala.html', {'sala': sala})

def editar_sala(request, id):
    sala = get_object_or_404(Sala, pk=id)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            return redirect('detalle_sala', id=id)
    else:
        form = SalaForm(instance=sala)
    return render(request, 'app_actividades/formulario.html', {'form': form, 'titulo': 'Editar Sala', 'volver': 'lista_salas'})

def eliminar_sala(request, id):
    sala = get_object_or_404(Sala, pk=id)
    if request.method == 'POST':
        sala.delete()
        return redirect('lista_salas')
    return render(request, 'app_actividades/confirmar_eliminar.html', {'objeto': sala, 'tipo': 'sala', 'volver': 'lista_salas'})




def inscripciones_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    usuarios = actividad.usuarios_inscritos.all()
    return render(request, 'app_actividades/inscripciones/inscripciones_actividad.html', {
        'actividad': actividad,
        'usuarios': usuarios,
    })

def inscribir_usuario(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            if actividad.usuarios_inscritos.filter(pk=usuario.pk).exists():
                messages.error(request, f'{usuario.nombre} ya está inscrito en esta actividad.')
                return redirect('inscripciones_actividad', id=id)
            actividad.refresh_from_db()
            if actividad.plazas_disponibles <= 0:
                messages.error(request, 'No quedan plazas disponibles en esta actividad.')
                return redirect('inscripciones_actividad', id=id)
            actividad.usuarios_inscritos.add(usuario)
            Actividad.objects.filter(pk=id).update(plazas_disponibles=F('plazas_disponibles') - 1)

            messages.success(request, f'{usuario.nombre} inscrito correctamente.')
            return redirect('inscripciones_actividad', id=id)
    else:
        form = InscripcionForm()
    return render(request, 'app_actividades/formulario.html', {
        'form': form,
        'titulo': f'Inscribir usuario en {actividad.nombre}',
        'volver': 'lista_actividades',
    })

def cancelar_inscripcion(request, actividad_id, usuario_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        actividad.usuarios_inscritos.remove(usuario)

        Actividad.objects.filter(pk=actividad_id).update(plazas_disponibles=F('plazas_disponibles') + 1)

        messages.success(request, f'Inscripción de {usuario.nombre} cancelada.')
        return redirect('inscripciones_actividad', id=actividad_id)
    return render(request, 'app_actividades/confirmar_eliminar.html', {
        'objeto': usuario,
        'tipo': 'inscripción',
        'volver': 'lista_actividades',
        'mensaje_extra': f'de la actividad "{actividad.nombre}"',
    })
