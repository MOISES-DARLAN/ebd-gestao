from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Turma, Chamada, Aluno
from datetime import date

def home_page(request):
    return render(request, 'ebd/home.html')

@login_required
def teacher_dashboard(request):
    try:
        turma = Turma.objects.get(professor=request.user)
    except Turma.DoesNotExist:
        return render(request, 'ebd/no_turma.html')

    hoje = date.today()
    
    if request.method == 'POST':
        ids_alunos_presentes = request.POST.getlist('presentes')
        chamada, created = Chamada.objects.get_or_create(turma=turma, data=hoje)
        
        chamada.alunos_presentes.clear()
        
        for aluno_id in ids_alunos_presentes:
            aluno = Aluno.objects.get(id=aluno_id)
            chamada.alunos_presentes.add(aluno)
        
        messages.success(request, 'Chamada salva com sucesso!')
        return redirect('teacher_dashboard')

    alunos_da_turma = turma.alunos.all().order_by('nome_completo')
    chamada_de_hoje = Chamada.objects.filter(turma=turma, data=hoje).first()
    ids_presentes_hoje = []
    if chamada_de_hoje:
        ids_presentes_hoje = chamada_de_hoje.alunos_presentes.values_list('id', flat=True)

    context = {
        'turma': turma,
        'alunos': alunos_da_turma,
        'ids_presentes_hoje': ids_presentes_hoje
    }
    return render(request, 'ebd/teacher_dashboard.html', context)