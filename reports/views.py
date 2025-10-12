from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ebd.models import Turma, Chamada

@login_required
def attendance_history(request):
    try:
        turma = Turma.objects.get(professor=request.user)
    except Turma.DoesNotExist:
        return render(request, 'ebd/no_turma.html')
    
    historico = Chamada.objects.filter(turma=turma).order_by('-data')
    
    context = {
        'turma': turma,
        'historico': historico,
    }
    return render(request, 'reports/attendance_history.html', context)


@login_required
def chamada_detalhes(request, chamada_id):
    chamada = get_object_or_404(Chamada, id=chamada_id, turma__professor=request.user)
    
    alunos_da_turma = chamada.turma.alunos.all()
    alunos_presentes = chamada.alunos_presentes.all()
    
    alunos_ausentes = alunos_da_turma.difference(alunos_presentes)
    
    context = {
        'chamada': chamada,
        'alunos_presentes': alunos_presentes,
        'alunos_ausentes': alunos_ausentes,
    }
    return render(request, 'reports/chamada_detalhes.html', context)