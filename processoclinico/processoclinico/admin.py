from django.contrib import admin

from processoclinico.models import Agente, Receita, Utente, Consulta, Pessoa, Stock, Medicamento

# Register your models here.

admin.site.register(Agente)
admin.site.register(Receita)
admin.site.register(Utente)
admin.site.register(Consulta)
admin.site.register(Pessoa)
admin.site.register(Stock)
admin.site.register(Medicamento)