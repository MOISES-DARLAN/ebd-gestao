from django.db import models
from django.contrib.auth.models import User

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    nome_responsavel = models.CharField(max_length=255, blank=True, null=True)
    telefone_contato = models.CharField(max_length=20, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    codigo_acesso = models.CharField(max_length=50, help_text="Senha para o professor acessar a turma.")
    alunos = models.ManyToManyField(Aluno, blank=True)

    def __str__(self):
        return self.nome

class Chamada(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    alunos_presentes = models.ManyToManyField(Aluno, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('turma', 'data')

    def __str__(self):
        return f"Chamada da turma '{self.turma.nome}' em {self.data.strftime('%d/%m/%Y')}"