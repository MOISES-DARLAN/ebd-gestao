from django.contrib import admin
from .models import Aluno, Turma, Chamada, RegistroAlunoChamada

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'data_nascimento', 'nome_responsavel', 'data_cadastro')
    search_fields = ('nome_completo', 'nome_responsavel')
    list_filter = ('data_nascimento',)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_acesso')
    search_fields = ('nome',)
    filter_horizontal = ('alunos',)

class RegistroAlunoChamadaInline(admin.TabularInline):
    model = RegistroAlunoChamada
    extra = 1
    autocomplete_fields = ['aluno']

@admin.register(Chamada)
class ChamadaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'data', 'oferta_do_dia', 'visitantes')
    list_filter = ('turma', 'data')
    inlines = [RegistroAlunoChamadaInline]
    search_fields = ('turma__nome', 'data') # Linha adicionada

@admin.register(RegistroAlunoChamada)
class RegistroAlunoChamadaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'chamada', 'presente', 'pontos')
    list_filter = ('aluno', 'chamada__data', 'presente')
    autocomplete_fields = ['aluno', 'chamada']