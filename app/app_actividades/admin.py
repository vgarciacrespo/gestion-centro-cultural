from django.contrib import admin
from .models import Actividad, Usuario, Monitor, Sala

class ActividadAdmin(admin.ModelAdmin):
    filter_horizontal = ('salas_secundarias',)

admin.site.register(Actividad, ActividadAdmin)
admin.site.register(Usuario)
admin.site.register(Monitor)
admin.site.register(Sala)