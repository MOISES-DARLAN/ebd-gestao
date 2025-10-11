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
    oferta_do_dia = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    visitantes = models.PositiveIntegerField(default=0) # Este é o total de visitantes da turma
    observacoes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('turma', 'data')

    def __str__(self):
        return f"Chamada da turma '{self.turma.nome}' em {self.data.strftime('%d/%m/%Y')}"

class RegistroAlunoChamada(models.Model):
    class Participacao(models.TextChoices):
        NADA = 'NADA', 'Nada'
        MEDIANO = 'MEDIANO', 'Mediano'
        MUITO = 'MUITO', 'Muito'

    chamada = models.ForeignKey(Chamada, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    
    presente = models.BooleanField(default=False)
    trouxe_biblia = models.BooleanField(default=False)
    trouxe_revista = models.BooleanField(default=False)
    contribuiu = models.BooleanField(default=False)
    levou_visitante = models.BooleanField(default=False)
    participacao = models.CharField(
        max_length=10,
        choices=Participacao.choices,
        default=Participacao.NADA
    )

    class Meta:
        unique_together = ('chamada', 'aluno')

    @property
    def pontos(self):
        total = 0
        if self.presente: total += 15
        if self.contribuiu: total += 10
        if self.participacao == self.Participacao.MUITO: total += 10
        elif self.participacao == self.Participacao.MEDIANO: total += 5
        if self.trouxe_biblia: total += 5
        if self.trouxe_revista: total += 5
        if self.levou_visitante: total += 20
        return total