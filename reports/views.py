from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ebd.models import Turma, Chamada

@login_required
def attendance_history(request, turma_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado. Por favor, insira o código da turma.')
        return redirect('ebd:acesso_turma', turma_id=turma_id)

    turma = get_object_or_404(Turma, id=turma_id)
    historico = Chamada.objects.filter(turma=turma).order_by('-data')
    
    context = {
        'turma': turma,
        'historico': historico,
    }
    return render(request, 'reports/attendance_history.html', context)


@login_required
def chamada_detalhes(request, chamada_id):
    chamada = get_object_or_404(Chamada, id=chamada_id)

    if chamada.turma.id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado.')
        return redirect('ebd:dashboard')

    alunos_da_turma = chamada.turma.alunos.all().order_by('nome_completo')
    
    context = {
        'chamada': chamada,
        'alunos_da_turma': alunos_da_turma,
        'ids_presentes': chamada.alunos_presentes.values_list('id', flat=True),
        'ids_com_biblia': chamada.alunos_com_biblia.values_list('id', flat=True),
        'ids_com_licao': chamada.alunos_com_licao.values_list('id', flat=True),
    }
    return render(request, 'reports/chamada_detalhes.html', context)