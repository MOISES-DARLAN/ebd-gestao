from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ebd.models import Turma, Chamada, RegistroAlunoChamada
from django.db.models import Count, Q

@login_required
def attendance_history(request, turma_id):
    if turma_id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado.')
        return redirect('ebd:acesso_turma', turma_id=turma_id)

    turma = get_object_or_404(Turma, id=turma_id)
    
    # A lógica de contagem foi movida para cá usando .annotate()
    historico = Chamada.objects.filter(turma=turma).order_by('-data').annotate(
        presentes_count=Count('registroalunochamada', filter=Q(registroalunochamada__presente=True))
    )
    
    context = { 'turma': turma, 'historico': historico }
    return render(request, 'reports/attendance_history.html', context)

@login_required
def chamada_detalhes(request, chamada_id):
    chamada = get_object_or_404(Chamada, id=chamada_id)

    if chamada.turma.id not in request.session.get('turmas_autorizadas', []):
        messages.warning(request, 'Acesso negado.')
        return redirect('ebd:dashboard')

    registros = RegistroAlunoChamada.objects.filter(chamada=chamada).select_related('aluno').order_by('aluno__nome_completo')
    
    context = { 'chamada': chamada, 'registros': registros }
    return render(request, 'reports/chamada_detalhes.html', context)