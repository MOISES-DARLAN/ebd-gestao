from django.contrib import admin
from .models import Aluno, Turma, Chamada

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

@admin.register(Chamada)
class ChamadaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'data')
    list_filter = ('turma', 'data')
    filter_horizontal = ('alunos_presentes',)