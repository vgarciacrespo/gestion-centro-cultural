from django import forms
from .models import Actividad, Usuario, Monitor, Sala

from django.db.models import Q
from datetime import timedelta

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'tipo', 'horario_inicio', 'descripcion', 'duracion', 'plazas_disponibles', 'monitor', 'sala_principal', 'salas_secundarias']
        widgets = {
            'horario_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        horario_inicio = cleaned_data.get('horario_inicio')
        duracion = cleaned_data.get('duracion')
        sala_principal = cleaned_data.get('sala_principal')
        salas_secundarias = cleaned_data.get('salas_secundarias')

        if not horario_inicio or not duracion:
            return cleaned_data

        horario_fin = horario_inicio + timedelta(minutes=duracion)
        overlap_query = Q(horario_inicio__lt=horario_fin, horario_fin__gt=horario_inicio)
        
        if self.instance and self.instance.pk:
            overlap_query &= ~Q(pk=self.instance.pk)

        if sala_principal:
            q_sala = Q(sala_principal=sala_principal) | Q(salas_secundarias=sala_principal)
            if Actividad.objects.filter(overlap_query, q_sala).exists():
                self.add_error('sala_principal', f'La sala principal "{sala_principal.nombre}" ya está ocupada en ese horario.')

        if salas_secundarias:
            for sala in salas_secundarias:
                q_sala = Q(sala_principal=sala) | Q(salas_secundarias=sala)
                if Actividad.objects.filter(overlap_query, q_sala).exists():
                    self.add_error('salas_secundarias', f'La sala secundaria "{sala.nombre}" ya está ocupada en ese horario.')
                    break

        return cleaned_data

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'edad', 'email', 'telefono']  

class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = '__all__'

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'

class InscripcionForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), required=True, label="Seleccionar Usuario a Inscribir")
